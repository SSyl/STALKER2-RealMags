# Real Mags

A S.T.A.L.K.E.R. 2: Heart of Chornobyl (2.0+) mod that gives the guns the magazine sizes of the real firearms they're
based on. It only changes capacities. Damage, recoil, prices and everything else stay vanilla, and it adds no new
items.

## What it changes

Names are the in-game names, with the real gun in parentheses. Counts are rounds in the magazine, not counting the
one in the chamber. Every value below was checked in game on 2026-11-03.

### Pistols

| Gun | Vanilla | Real Mags | Why |
|---|---|---|---|
| UDP Compact (HK USP Tactical .45), Deadeye (USP Match .45) | 15 / 20 | 12 / 17 | The .45 USP holds 12. The extended magazine is a common +5 extension that matches the in-game model. |
| Gambit (USP SD, 9mm) | 15 / 20 | 15 / 21 | The 9mm USP holds 15. It shares the UDP's magazines, so a hidden +25% upgrade scales them for 9mm. |
| APSB (Stechkin APB), Encourage | 18 / 30 | 20 / 30 | The APS/APB magazine holds 20. |
| PTM (Makarov PM), Skif's Pistol, Labyrinth IV, PTM Monolith, Star's pistol (named PTM in game) | 8 / 12 | 8 / 10 | The extended magazine is the common 10-round PM extension. The 12-round PMM magazine does not fit a PM. |

### Submachine guns

| Gun | Vanilla | Real Mags | Why |
|---|---|---|---|
| Integral-A (KRISS Vector), Riemann, 9mm | 20 / 30 | 17 / 40 | The standard magazine is a Glock 17 (17). The extended model is a Glock 17 with a KRISS MagEx2 sleeve (40). |
| Integral-A, Riemann, after the .45 conversion | 20 / 30 | 13 / 30 | A Glock 21 holds 13, and the MagEx2 for .45 gives 30. The conversion upgrade carries a -25% capacity effect. |
| Zubr-19 (PP-19 Bizon, 9x19) | 50 / 64 | 53 / 64 | The 9x19 Bizon magazine holds 53. The extended magazine has "64" written on it in marker. |
| Rat Killer (PP-19 Bizon, 9x18) | 50 / 64 | 48 / 64 | The real 9x18 Bizon magazine holds 64, sized for four 16-round ammo boxes. The extended magazine has "64" written on it in marker, so it stays 64. Setting the standard to 64 as well would make the extended magazine pointless, so the standard drops by one box of 16, to 48. |
| Spitfire (AKS-74U) | 40 | 45 | The closest real magazine is the RPK-74's 45. |
| Fora-230 (Fort-230) | 20 / 40 | 20 / 50 | The standard is the factory 20. The extended model is a box with a drum below it, like the 50-round Glock and Uzi drums. |

### Rifles and machine guns

| Gun | Vanilla | Real Mags | Why |
|---|---|---|---|
| GP37 (HK G36), drum | 90 | 100 | The Beta C-Mag twin drum holds 100. |
| AKM-9B (AK-9), Cost of Hope | 30 / 45 / paired 30 | 20 / 30 / paired 20 | The real AK-9 magazine holds 20. The AKM-9B shares the AKM-74S's magazines, but a 9x39 round is much fatter than a 5.45, since it uses the wider 7.62x39 case. The standard magazine's model is about the size of a real 20-round AK-9 magazine, and the extended (the AKM-74S's 45-round magazine) is about the size of the 30-round 9x39 magazine used by the SR-3M, AS Val and VSS. A hidden -33% upgrade gives 20 / 30 / paired 20, the closest match possible without new models. The AKM-74S keeps 30 / 45 / 30. |
| RPM-74 (PKM) | 150 / 250 / 350 | 100 / 200 / 250 | PKM ammunition boxes hold 100, 200 and 250. |
| Glutton (PKM) | 500 | 250 | The largest real PKM box. |

### Shotguns

| Gun | Vanilla | Real Mags | Why |
|---|---|---|---|
| Guardian (Saiga-12K), Cost of Hope | 14 | 12 | Its magazine looks roughly the same size as the regular Saiga-12K's 12-round box (it may be a recolor), so it gets the common 12-round Saiga box capacity. |

Every other gun keeps its vanilla capacity. Either it already matches a real magazine, or its in-game magazine is a
made-up part with no real counterpart.

The AKM-9B and Guardian changes need the Cost of Hope expansion. Without it, the mod still loads and everything
else still applies. That was tested with Cost of Hope uninstalled.

The Deluxe and Ultimate edition guns, like the Riemann, use the base game's magazines and upgrades. If you own those
editions, they change along with their base guns.

## Installing

1. Download `RealMags-<version>.zip`.
2. Extract the `RealMags` folder into `<game folder>\Stalker2\Content\Paks\~mods\`, so the file ends up at
   `~mods\RealMags\RealMagsStalker2-Windows-OverrideContent.pak`. Create `~mods` if it doesn't exist.
3. Start the game.

To uninstall, delete the `~mods\RealMags` folder.

A magazine that's already loaded may keep its old count until you unload and reload it. A gun spawned from the
console shows the vanilla capacity in its tooltip until its first reload.

The Gambit and the AKM-9B get their capacity from a hidden upgrade, which applies to guns you find or buy after
installing. Whether it also applies to a gun that was already in your save hasn't been tested.

Other mods that change the same magazines will conflict. The same goes for mods that change the Integral-A's .45
conversion upgrade, or the Gambit's or AKM-9B's preinstalled upgrades. `table.toml` lists everything this mod
patches.

## How it was made

1. A script, now `tools/extract_capacities.py`, read the game's weapon, magazine, upgrade and effect tables,
   including Cost of Hope and the Deluxe, Ultimate and pre-order packs, and followed each gun to its magazines and
   upgrades. That showed three things. No vanilla upgrade changes capacity. Extended magazines are separate items.
   Caliber conversions keep the same capacity.
2. Each gun was matched to the real gun it's based on, using the names from Real Weapon Names Renewed. Then its
   factory and common aftermarket magazines were looked up.
3. The values were picked gun by gun, using the in-game magazine model as the guide. If the model looks like a real
   magazine, the gun gets that magazine's real, commonly used capacity. If it's a made-up part, it keeps the
   game's capacity. A caliber a gun never had in real life keeps its magazine's value.
4. Some magazines are shared by guns that need different capacities, like the Gambit and the AKM-9B, or need a
   different capacity after a caliber conversion, like the Integral-A. Those use the game's AmmoCapacity effects,
   either on a hidden preinstalled upgrade or on the conversion upgrade itself. The percentages were chosen so the
   game's rounding gives exactly the wanted counts.
5. Every gun was spawned in game and its magazines counted.

## Building from source

You need Python 3.11 or newer, [ZonePak](https://github.com/SSyl/ZonePak) set up as its README describes, and the
Cost of Hope expansion installed. ZonePak reads the expansion's tables from its pak, and it stops with "DLC1 is not
a DLC folder in the game install" if the expansion is missing.

`table.toml` holds the values. `tools/generate.py` turns them into the cfg patches in `cfg/`, and ZonePak checks and
packs them:

```
python tools/generate.py
python -m zonepak --project <path to RealMags> check
python -m zonepak --project <path to RealMags> build
```

Run the ZonePak commands from the ZonePak folder. `build` writes `build/RealMags/` and `build/RealMags-<version>.zip`.

`check` prints three warnings, and all three are expected. Two say the Cost of Hope entries aren't checked, because
the Lesser Zone Kit has no Cost of Hope data. The third says the Gambit's preinstalled upgrade list is inherited.

## Re-checking after a game update

`tools/extract_capacities.py` reads the weapon, magazine, upgrade and effect tables straight from your installed
game, including Cost of Hope and the Deluxe, Ultimate and pre-order packs you have. It writes every gun's
magazines, their capacities and the upgrades that touch them to a JSON file:

```
python tools/extract_capacities.py weapons.json
```

It uses ZonePak's config for the game and repak paths, and looks for ZonePak next to this folder. Pass
`--zonepak <folder>` if yours is somewhere else. Compare the output with `table.toml` to see whether a game update
changed any magazine this mod patches.

## Credits

- [joric](https://github.com/joric/stalker) for `tools/bin2cfg.py`, which decodes the game's binary tables. It's
  released under the Unlicense and included unchanged.

## License

The code and docs are MIT, except `tools/bin2cfg.py` (see Credits). See `LICENSE`.
