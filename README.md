# DepthsGuard

Anti-xray and anti-invis-particle setup for The Depths SMP (Paper 1.21.11).

| Piece | Stops | Where |
|---|---|---|
| Server resource pack | Xray **resource packs** and invis-particle packs (Obvious Invisibility Particles, InvisAlert+) | `pack/` |
| Orebfuscator 5.6.2 + ProtocolLib | **All** xray (packs, mods, hacked clients): ores, containers, base blocks, valuables, spawners, trial chambers and other structure blocks, at every height, including rooms and caves | `server-config/` |
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
2. Install **ProtocolLib** (dev-build from github.com/dmulloy2/ProtocolLib/releases/tag/dev-build; 5.4.0 is too old for 1.21.11)
   and **Orebfuscator 5.6.2** (modrinth.com/plugin/orebfuscator). Start once so Orebfuscator writes its config, stop.
3. Replace `plugins/Orebfuscator/config.yml` with `server-config/orebfuscator-config.yml`
   (or run `python server-config/orebfuscator_patch.py plugins/Orebfuscator/config.yml` on a fresh default config).
   If your worlds aren't named `world`, `world_nether`, `world_the_end`, fix the `worlds:` lists.
4. Keep Paper's own anti-xray **off** (`anticheat.anti-xray.enabled: false` in `config/paper-world-defaults.yml`,
   the default). Don't run both.
5. Put `build/libs/DepthsGuard-1.0.1.jar` in `plugins/`, restart.

When the pack changes, rebuild, upload under a **new** URL/tag and update the sha1, or clients keep the cached copy.

## Tested (local server in `run/`, 2026-09-30)
- Invisibility via /effect with hide-invisibility-particles: true: observer receives no effect particles; a control Speed effect still does.
- Default (false): invisibility keeps its vanilla faint particles; the pack keeps their textures vanilla.
- Paper anti-xray alone was NOT enough: containers other than chests, anything touching air (rooms, caves, bases),
  anything above y=64 and whole trial chambers were sent to the client as-is, and hidden chests still leaked their block entity.
- Orebfuscator (this config), xray bot never near the blocks: 46/50 test blocks hidden buried below y64, in a room,
  and buried at y100 (the only ones shown are oak planks, glass, obsidian, which are normal building blocks, plus rare random matches);
  nether 14/14 hidden; 0 of 20 client-seen ancient debris real; trial chamber from above: 0 of ~31k chamber blocks sent.
  No container data leaked in two full runs (one hidden trial spawner leaked its data once in an earlier run and did not reproduce).
- Legit play: standing in the base room the player sees all 14 base blocks; standing in the trial chamber the nearby
  spawner and walls appear. A player on the roof 10 blocks above (behind stone) sees 0/14.
- Once a player has seen a block it stays visible to them until the chunk is resent, which is normal Orebfuscator behaviour.
- Declining the pack: kicked with the required-pack message.
