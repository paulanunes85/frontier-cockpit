---
name: ms-demo-video-editor
description: "Edit Microsoft demo screen recordings into professional short MP4 films using the ms-identity identity. Use for demo videos, screen recordings, MOV or MP4 editing, trimming mistakes, one-minute or two-minute cuts, lower thirds, cover and end cards, highlights, punch-ins, crossfades, demo reels, agent demos, legacy versus modernized app demos, and editorial video assembly."
---

# Microsoft Demo Video Editor

Use this skill to transform raw screen recordings of demos, terminals, VS Code, web apps, or agents running into short editorial MP4 videos under the `ms-identity` identity.

Do not use this skill for synthetic video generation from scratch or for recordings that require complex spoken-audio editing.

## First Step

Read [references/gotchas.md](references/gotchas.md) before cutting video. Then identify:

- Source files and desired duration.
- Whether the recording has audio.
- Target story, audience, and title.
- Whether the output should be continuous or beat-based.
- Required output folder. Use the user-provided folder, or a repository media folder such as `demos-modernization/`.

## Pipeline

### 1. Probe Sources

```bash
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=codec_type,width,height,r_frame_rate -of default=nw=1 SRC.mov
```

Record duration, resolution, fps, and audio presence. macOS screen recordings can arrive at 120 to 240 fps and very high resolution, which changes extraction strategy.

### 2. Map the Content

```bash
python scripts/map_video.py SRC.mov --fps-frac 5
python scripts/map_video.py SRC.mov --transitions
```

Review contact sheets and transition diffs. Mark screens, mistakes, retakes, dead time, static sections, and black frames.

### 3. Verify Cut Boundaries

For every cut point, extract the frame and confirm no wrong command, error state, or typing leak remains:

```bash
ffmpeg -y -v error -ss 48.4 -i SRC.mov -frames:v 1 chk.png
```

Cut on static frames when possible.

### 4. Choose Composition Mode

| Mode | Use when | Pattern |
| --- | --- | --- |
| Continuous | One clean demo flow | Full recording in frame, timed lower thirds by chapter. |
| Beats | Long or multi-source material | Short 6 to 11 second slices, each framed with lower third, joined with crossfades. |

Multi-source films should use beats. A single one-minute tour can use continuous mode.

### 5. Generate Brand Assets

```bash
python scripts/brand_assets.py \
  --kicker "SIFAP // SISTEMA MODERNIZADO" \
  --title "SIFAP 2.0" \
  --subtitle "Next.js 15 · Spring Boot 3.3 · PostgreSQL" \
  --end-line1 "Mesmos dados. Mesmas regras." \
  --end-line2 "Novo sistema."
```

This creates `cover.png`, `endcard.png`, and `framebg.png`. Read [references/visual-spec.md](references/visual-spec.md) before changing the visual identity.

### 6. Apply Effects Sparingly

- Highlight: use Microsoft yellow for short, verified windows.
- Punch-in: use Ken Burns style via `zoompan`, not dynamic crop expressions.
- Speed-up: use only for long scrolling or typing, typically 1.25x to 1.5x.
- Lower thirds: keep visible for 3 to 6 seconds, aligned to verified screen moments.

### 7. Assemble

```bash
python scripts/assemble.py plan.json
```

The plan controls cards, beats, lower thirds, highlights, continuous windows, and final MP4 assembly. Start from [references/plan-example.json](references/plan-example.json).

## Rhythm

- Target 1 minute: 50 to 60 seconds.
- Target 2 minutes: 105 to 120 seconds.
- Beat duration: 6 to 11 seconds.
- Cover card: 4 to 4.5 seconds.
- End card: 4.5 to 5 seconds.
- Crossfade: about 0.4 seconds.

## Identity

- Use the `ms-identity` identity and Microsoft 4-color palette.
- Author line: `Frontier Cockpit Team | Software Global Black Belt`.
- Co-brand: `Microsoft · GitHub` when appropriate.
- Fonts: Inter and JetBrains Mono.
- Do not use personal social handles or personal palette colors.

## QA Before Delivery

1. Generate a contact sheet of the final video:

   ```bash
   python scripts/map_video.py FINAL.mp4 --fps-frac 8
   ```

2. Verify cover, lower thirds, highlights, key screens, and end card.
3. Decode-check the MP4:

   ```bash
   ffmpeg -v error -i FINAL.mp4 -f null -
   ```

4. Confirm QuickTime opens the final file.
5. Store the final MP4 in the requested workspace folder.

## References

| File | Use when |
| --- | --- |
| [references/gotchas.md](references/gotchas.md) | Before editing any source video. |
| [references/visual-spec.md](references/visual-spec.md) | When changing visual identity, lower thirds, cards, or frame treatment. |
| [references/plan-example.json](references/plan-example.json) | When creating or editing the assembly plan. |