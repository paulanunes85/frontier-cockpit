// Promise-aware TTL cache for expensive Prometheus aggregates.
//
// A single dashboard refresh fans out into summary, sessions, and coach, and
// coach and planner rebuild aggregates the other endpoints already computed.
// Caching the in-flight promise (not just the settled value) collapses those
// concurrent calls into one Prometheus round trip. Failures are never cached,
// so a transient backend error cannot be pinned for the whole TTL.

interface CacheEntry<T> {
    promise: Promise<T>;
    // Set only once the promise resolves; an in-flight entry stays valid so
    // concurrent callers join it instead of starting a second load.
    expiresAt: number | null;
}

export interface AsyncCacheOptions {
    ttlMs: number;
    now?: () => number;
}

export class AsyncCache<T> {
    private readonly entries = new Map<string, CacheEntry<T>>();
    private readonly ttlMs: number;
    private readonly now: () => number;

    constructor(options: AsyncCacheOptions) {
        this.ttlMs = options.ttlMs;
        this.now = options.now ?? (() => Date.now());
    }

    get size(): number {
        return this.entries.size;
    }

    async load(key: string, loader: () => Promise<T>, forceRefresh = false): Promise<T> {
        const existing = this.entries.get(key);
        // A forced refresh still joins an in-flight load: the running request is
        // already as fresh as a new one, and joining avoids duplicate fan-out when
        // several clients hit Refresh at the same moment.
        const inFlight = existing?.expiresAt === null;
        const fresh = inFlight || (existing !== undefined && (existing.expiresAt ?? 0) > this.now());
        if (existing && (inFlight || (fresh && !forceRefresh))) {
            return existing.promise;
        }

        const entry: CacheEntry<T> = { promise: Promise.resolve().then(loader), expiresAt: null };
        this.entries.set(key, entry);
        try {
            const value = await entry.promise;
            if (this.entries.get(key) === entry) {
                entry.expiresAt = this.now() + this.ttlMs;
            }
            return value;
        } catch (error) {
            if (this.entries.get(key) === entry) {
                this.entries.delete(key);
            }
            throw error;
        }
    }

    invalidate(key?: string): void {
        if (key === undefined) {
            this.entries.clear();
            return;
        }
        this.entries.delete(key);
    }
}
