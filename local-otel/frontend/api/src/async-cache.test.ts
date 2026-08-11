import { strict as assert } from "node:assert";
import test from "node:test";

import { AsyncCache } from "./async-cache.js";

function deferred<T>(): { promise: Promise<T>; resolve: (value: T) => void; reject: (error: Error) => void } {
    let resolve!: (value: T) => void;
    let reject!: (error: Error) => void;
    const promise = new Promise<T>((res, rej) => {
        resolve = res;
        reject = rej;
    });
    return { promise, resolve, reject };
}

test("concurrent calls for the same key run the loader once", async () => {
    const cache = new AsyncCache<number>({ ttlMs: 1000 });
    const gate = deferred<number>();
    let calls = 0;
    const loader = () => {
        calls += 1;
        return gate.promise;
    };

    const first = cache.load("a", loader);
    const second = cache.load("a", loader);
    gate.resolve(7);

    assert.equal(await first, 7);
    assert.equal(await second, 7);
    assert.equal(calls, 1);
});

test("different keys do not share cached values", async () => {
    const cache = new AsyncCache<string>({ ttlMs: 1000 });
    const oneHour = await cache.load("1h|repo-a", async () => "1h|repo-a");
    const sixHours = await cache.load("6h|repo-a", async () => "6h|repo-a");
    const otherRepo = await cache.load("1h|repo-b", async () => "1h|repo-b");

    assert.equal(oneHour, "1h|repo-a");
    assert.equal(sixHours, "6h|repo-a");
    assert.equal(otherRepo, "1h|repo-b");
    assert.equal(cache.size, 3);
});

test("cached values are reused until the ttl expires", async () => {
    let clock = 0;
    const cache = new AsyncCache<number>({ ttlMs: 100, now: () => clock });
    let calls = 0;
    const loader = async () => {
        calls += 1;
        return calls;
    };

    assert.equal(await cache.load("k", loader), 1);
    clock = 50;
    assert.equal(await cache.load("k", loader), 1);
    clock = 101;
    assert.equal(await cache.load("k", loader), 2);
    assert.equal(calls, 2);
});

test("rejected loads are not cached", async () => {
    const cache = new AsyncCache<number>({ ttlMs: 1000 });
    let calls = 0;
    const loader = async () => {
        calls += 1;
        if (calls === 1) {
            throw new Error("prometheus unavailable");
        }
        return 42;
    };

    await assert.rejects(() => cache.load("k", loader), /prometheus unavailable/);
    assert.equal(await cache.load("k", loader), 42);
    assert.equal(calls, 2);
});

test("force refresh replaces a cached value but joins an in-flight load", async () => {
    let clock = 0;
    const cache = new AsyncCache<number>({ ttlMs: 1000, now: () => clock });
    let calls = 0;
    const loader = async () => {
        calls += 1;
        return calls;
    };

    assert.equal(await cache.load("k", loader), 1);
    assert.equal(await cache.load("k", loader, true), 2);
    assert.equal(calls, 2);

    const gate = deferred<number>();
    const slowLoader = () => {
        calls += 1;
        return gate.promise;
    };
    const first = cache.load("k", slowLoader, true);
    const second = cache.load("k", slowLoader, true);
    gate.resolve(99);
    assert.equal(await first, 99);
    assert.equal(await second, 99);
    assert.equal(calls, 3);
});

test("invalidate clears one key or the whole cache", async () => {
    const cache = new AsyncCache<number>({ ttlMs: 1000 });
    let calls = 0;
    const loader = async () => {
        calls += 1;
        return calls;
    };

    await cache.load("a", loader);
    await cache.load("b", loader);
    cache.invalidate("a");
    assert.equal(cache.size, 1);

    cache.invalidate();
    assert.equal(cache.size, 0);
});
