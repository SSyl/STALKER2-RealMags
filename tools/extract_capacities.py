"""Lists every gun's magazines, their capacities and the upgrades that touch them, from the installed game.

Usage: python tools/extract_capacities.py <out.json> [--zonepak <ZonePak folder>]

Reads the weapon, magazine, upgrade and effect tables straight from the game's paks, including Cost of Hope and the
Deluxe, Ultimate and pre-order packs when they're installed. The game and repak paths come from ZonePak's
config.toml, and ZonePak is looked for next to this repo unless --zonepak names it.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLES = {
    'item': 'ItemPrototypes',
    'upgrade': 'UpgradePrototypes',
    'effect': 'EffectPrototypes',
    'setup': 'WeaponData/WeaponGeneralSetupPrototypes',
}


def load_tables(config, gametables, cfg):
    tables = {name: {} for name in TABLES}
    for part in gametables.PARTS:
        for name, table in TABLES.items():
            for node in gametables.table(config, part, table):
                if isinstance(node, cfg.Struct):
                    sid = node.find('SID')
                    tables[name][sid.value if isinstance(sid, cfg.Value) else node.name] = node
    return tables


def survey(tables, names, cfg):
    def get(table, sid, key, depth=0):
        node = tables[table].get(sid)
        if node is None or depth > 20:
            return None
        hit = node.find(key)
        if hit is not None:
            return hit
        parent = node.flags.get('refkey')
        if parent and not parent.startswith('['):
            return get(table, parent, key, depth + 1)
        return None

    def val(table, sid, key):
        hit = get(table, sid, key)
        return hit.value if isinstance(hit, cfg.Value) else None

    def children(struct):
        return [c for c in struct.children if not isinstance(c, cfg.Unknown)] if isinstance(struct, cfg.Struct) else []

    def list_values(struct):
        return [c.value for c in children(struct) if isinstance(c, cfg.Value)]

    def effect_info(sid):
        return {'sid': sid, 'type': val('effect', sid, 'Type'), 'min': val('effect', sid, 'ValueMin'),
                'max': val('effect', sid, 'ValueMax'), 'caliber': val('effect', sid, 'Caliber')}

    tree_upgrades = {u for s in tables['setup'] for u in list_values(get('setup', s, 'UpgradePrototypeSIDs'))}

    def upgrade_info(sid):
        effects = [effect_info(e) for e in list_values(get('upgrade', sid, 'EffectPrototypeSIDs'))]
        return {'sid': sid,
                'capacity': [e for e in effects if e['type'] == 'EEffectType::AmmoCapacity'],
                'caliber': [e['caliber'] for e in effects if e['caliber']],
                'attaches': list_values(get('upgrade', sid, 'AttachPrototypeSIDs')),
                'requires': list_values(get('upgrade', sid, 'RequiredUpgradePrototypeSIDs')),
                'hidden': sid not in tree_upgrades}

    def mag_ammo(sid):
        mag = get('item', sid, 'Magazine')
        if not isinstance(mag, cfg.Struct):
            return None
        hit = mag.find('MaxAmmo')
        if hit is None:
            parent = tables['item'][sid].flags.get('refkey')
            return mag_ammo(parent) if parent and parent in tables['item'] else None
        return hit.value

    out = []
    for sid in tables['item']:
        setup = val('item', sid, 'GeneralWeaponSetup')
        key = f"sid_items_{val('item', sid, 'LocalizationSID') or sid}_name"
        if setup is None or setup not in tables['setup'] or key not in names:
            continue
        mags = []
        for attachment in children(get('setup', setup, 'CompatibleAttachments')):
            if not isinstance(attachment, cfg.Struct):
                continue
            attach = attachment.find('AttachPrototypeSID')
            if attach is None or mag_ammo(attach.value) in (None, '0'):
                continue
            mags.append({'sid': attach.value, 'max': mag_ammo(attach.value),
                         'requires': list_values(attachment.find('RequiredUpgradeIDs'))})
        preinstalled = []
        for entry in children(get('item', sid, 'PreinstalledUpgrades')):
            value = entry.value if isinstance(entry, cfg.Value) else None
            if isinstance(entry, cfg.Struct):
                field = entry.find('UpgradePrototypeSID') or entry.find('UpgradeSID')
                value = field.value if isinstance(field, cfg.Value) else None
            if value:
                preinstalled.append(upgrade_info(value))
        tree = [upgrade_info(u) for u in list_values(get('setup', setup, 'UpgradePrototypeSIDs'))]
        out.append({'sid': sid, 'key': key, 'name': names[key], 'refkey': tables['item'][sid].flags.get('refkey'),
                    'setup': setup, 'caliber': val('setup', setup, 'AmmoCaliber'),
                    'setup_max': val('setup', setup, 'MaxAmmo'), 'mags': mags,
                    'upgrades': [u for u in tree if u['capacity'] or u['caliber'] or
                                 any(m['sid'] in u['attaches'] for m in mags) or
                                 any(u['sid'] in m['requires'] for m in mags)],
                    'preinstalled': preinstalled})
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('out', type=Path)
    parser.add_argument('--zonepak', type=Path)
    args = parser.parse_args()
    candidates = [args.zonepak] if args.zonepak else [ROOT.parent / 'ZonePak', ROOT.parent / 'STALKER2-ZonePak']
    args.zonepak = next((c for c in candidates if (c / 'zonepak' / '__init__.py').is_file()), None)
    if args.zonepak is None:
        sys.exit(f'ZonePak not found in {" or ".join(map(str, candidates))}. Pass --zonepak <its folder>.')
    sys.path.insert(0, str(args.zonepak))
    from zonepak import cfg, gametables, tools
    from zonepak.build import game_text
    from zonepak.fetch import FetchError
    from zonepak.project import load_config

    try:
        config = load_config()
        tables = load_tables(config, gametables, cfg)
        weapons = survey(tables, game_text(config).culture('en'), cfg)
        args.out.write_text(json.dumps(weapons, indent=1, ensure_ascii=False), encoding='utf-8')
    except (FetchError, tools.ToolError, ValueError, OSError) as e:
        sys.exit(f'error: {e}')
    print(f'{len(weapons)} guns -> {args.out}')


if __name__ == '__main__':
    main()
