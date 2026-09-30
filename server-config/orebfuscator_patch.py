"""Extends Orebfuscator's default config: every ore, valuables, base blocks and
structure blocks, in every height, with ray-cast (line of sight) checks on.
Usage: python orebfuscator_patch.py plugins/Orebfuscator/config.yml"""
import re, sys

ORES = ['tag(minecraft:coal_ores)', 'tag(minecraft:copper_ores)', 'tag(minecraft:iron_ores)', 'tag(minecraft:gold_ores)',
        'tag(minecraft:redstone_ores)', 'tag(minecraft:lapis_ores)', 'tag(minecraft:diamond_ores)', 'tag(minecraft:emerald_ores)',
        'minecraft:raw_iron_block', 'minecraft:raw_copper_block', 'minecraft:raw_gold_block',
        'minecraft:amethyst_block', 'minecraft:budding_amethyst', 'minecraft:ancient_debris']
NETHER_ORES = ['minecraft:ancient_debris', 'minecraft:nether_gold_ore', 'minecraft:nether_quartz_ore', 'minecraft:gilded_blackstone']
BASE = ['minecraft:beacon', 'minecraft:conduit', 'minecraft:lodestone', 'minecraft:respawn_anchor', 'minecraft:jukebox',
        'minecraft:chiseled_bookshelf', 'minecraft:decorated_pot', 'minecraft:diamond_block', 'minecraft:emerald_block',
        'minecraft:gold_block', 'minecraft:iron_block', 'minecraft:netherite_block', 'minecraft:lapis_block',
        'minecraft:trial_spawner', 'minecraft:vault', 'minecraft:heavy_core', 'minecraft:end_portal_frame']
TUFF = ['tuff_bricks', 'chiseled_tuff', 'chiseled_tuff_bricks', 'polished_tuff', 'tuff_brick_slab', 'tuff_brick_stairs', 'tuff_brick_wall',
        'polished_tuff_slab', 'polished_tuff_stairs', 'polished_tuff_wall']
COPPER = [f'waxed_{o}{b}' for o in ['', 'exposed_', 'weathered_', 'oxidized_']
          for b in ['copper' if o else 'copper_block', 'cut_copper', 'chiseled_copper', 'copper_grate', 'copper_bulb',
                    'copper_door', 'copper_trapdoor', 'cut_copper_slab', 'cut_copper_stairs']]
STRUCTURES = ['minecraft:' + b for b in TUFF + COPPER + [
    'reinforced_deepslate', 'sculk_shrieker', 'sculk_sensor', 'sculk_catalyst',            # ancient city
    'mossy_stone_bricks', 'cracked_stone_bricks', 'chiseled_stone_bricks',                  # strongholds
    'infested_stone', 'infested_deepslate', 'infested_cobblestone', 'infested_stone_bricks',
    'infested_mossy_stone_bricks', 'infested_cracked_stone_bricks', 'infested_chiseled_stone_bricks',
    'mossy_cobblestone', 'spawner']]                                                        # dungeons
NETHER_STRUCTURES = ['minecraft:' + b for b in [
    'polished_blackstone_bricks', 'cracked_polished_blackstone_bricks', 'gilded_blackstone', 'gold_block',  # bastions
    'nether_bricks', 'nether_brick_fence', 'nether_brick_stairs', 'spawner']]                              # fortresses

ADD = {
    'obfuscation-overworld': ORES + STRUCTURES + BASE,
    'obfuscation-nether': NETHER_ORES + NETHER_STRUCTURES + BASE,
    'obfuscation-end': BASE,
    'proximity-overworld': ORES + STRUCTURES + BASE,
    'proximity-nether': NETHER_ORES + NETHER_STRUCTURES + BASE,
    'proximity-end': BASE + ['minecraft:purpur_block', 'minecraft:end_rod', 'minecraft:dragon_head'],
}

path = sys.argv[1]
text = open(path, encoding='utf-8').read()
parts = re.split(r'(?m)^(  (?:obfuscation|proximity)-[a-z]+:\n)', text)
out = [parts[0]]
for header, body in zip(parts[1::2], parts[2::2]):
    name = header.strip()[:-1]
    add = ADD.get(name, [])
    if name.startswith('proximity'):
        body = body.replace('    rayCastCheck:\n      enabled: false', '    rayCastCheck:\n      enabled: true')
        present = set(re.findall(r'(?m)^      ([^\s].*?): \{\}$', body))
        new = ''.join(f'      {b}: {{}}\n' for b in dict.fromkeys(add) if b not in present)
    else:
        present = set(re.findall(r'(?m)^    - (.*)$', body))
        new = ''.join(f'    - {b}\n' for b in dict.fromkeys(add) if b not in present)
    body = body.replace('    hiddenBlocks:\n', '    hiddenBlocks:\n' + new, 1)
    out += [header, body]
open(path, 'w', encoding='utf-8').write(''.join(out))
print('patched', path)
