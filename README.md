# DepthsGuard

Anti-xray and anti-invis-particle setup for The Depths SMP (Paper 1.21.11).

| Piece | Stops | Where |
|---|---|---|
| Server resource pack | Xray **resource packs** and invis-particle packs (Obvious Invisibility Particles, InvisAlert+) | `pack/` |
| Paper anti-xray (engine-mode 2) | **All** xray: packs, mods, hacked clients | `server-config/` |
| DepthsGuard plugin | Kicks players who decline/fail the pack. Optional `hide-invisibility-particles` (off by default: vanilla faint particles) | `src/` |

## Resource pack
`python pack/build_pack.py [version]` reads the vanilla client jar
(`%APPDATA%/.minecraft/versions/<version>/<version>.jar`, default 1.21.11) and writes
`pack/DepthsGuard-pack.zip` + `pack/DepthsGuard-pack.sha1`. Every file in it is untouched vanilla.
A server pack always loads above the player's own packs and can't be moved, so these copies win.

- `pack/blocks.txt`: blocks forced to vanilla (blockstate + models incl. parents + textures).
- `pack/extra.txt`: other paths: effect particles, particle/block atlases, all core shaders.
- Side effect: players' own packs can't restyle those blocks, the effect particles, or core shaders.

## Real server setup
1. `server.properties`:
   ```
   resource-pack=https://raw.githubusercontent.com/lrdrandomplayz/depths-pack/main/pack/DepthsGuard-pack.zip
   resource-pack-sha1=<contents of pack/DepthsGuard-pack.sha1>
   require-resource-pack=true
   resource-pack-prompt={"text":"The Depths SMP needs this pack to block xray and invis-particle packs.","color":"gray"}
   ```
2. `config/paper-world-defaults.yml`: replace the whole `anti-xray:` block under `anticheat:` with
   `server-config/anti-xray-overworld.yml`.
3. Copy `server-config/world_nether-paper-world.yml` to `world_nether/paper-world.yml` and
   `server-config/world_the_end-paper-world.yml` to `world_the_end/paper-world.yml`
   (merge by hand if those files already have settings).
4. Put `build/libs/DepthsGuard-1.0.1.jar` in `plugins/`, restart.

When the pack changes, rebuild, upload under a **new** URL/tag and update the sha1, or clients keep the cached copy.

## Tested (local server in `run/`, 2026-09-30)
- Invisibility via /effect with hide-invisibility-particles: true: observer receives no effect particles; a control Speed effect still does.
- Default (false): invisibility keeps its vanilla faint particles; the pack keeps their textures vanilla.
- Anti-xray: client saw ~41k diamond ores in a 64x64 area; 0 of 25 sampled were real.
- Declining the pack: kicked with the required-pack message.
