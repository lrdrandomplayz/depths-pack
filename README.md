# DepthsGuard

Stops invisibility-particle packs (Obvious Invisibility Particles, InvisAlert+) on The Depths SMP (Paper 1.21.11).
No anti-xray: that's Orebfuscator's job (default config). The old block/shader overrides caused rendering
issues, FPS drops and broke fullbright, so they were removed in 1.1.0.

| Piece | Does | Where |
|---|---|---|
| Server resource pack | Forces the 8 vanilla effect-particle textures + `particles/entity_effect.json`. A server pack always loads above the player's own packs, so invis-particle packs can't change them. Nothing else is overridden. | `pack/` |
| DepthsGuard plugin | Kicks players who decline/fail the pack. Optional `hide-invisibility-particles` (off by default: vanilla faint particles) | `src/` |

## Resource pack
`python pack/build_pack.py [version]` copies the files in `pack/extra.txt` from the vanilla client jar
(`%APPDATA%/.minecraft/versions/<version>/<version>.jar`, default 1.21.11) into `pack/DepthsGuard-pack.zip`
and writes `pack/DepthsGuard-pack.sha1`.

## Server setup
1. `server.properties`:
   ```
   resource-pack=https://raw.githubusercontent.com/lrdrandomplayz/depths-pack/main/pack/DepthsGuard-pack.zip
   resource-pack-sha1=<contents of pack/DepthsGuard-pack.sha1>
   require-resource-pack=true
   resource-pack-prompt={"text":"The Depths SMP needs this small pack to block invisibility-particle packs.","color":"gray"}
   ```
2. Put `build/libs/DepthsGuard-1.1.0.jar` in `plugins/`, restart.

When the pack changes, rebuild, push and update the sha1, or clients keep the cached copy.
