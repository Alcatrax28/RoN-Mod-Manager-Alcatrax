#!/usr/bin/env python3

import curses
import re
import shutil
import sys
from pathlib import Path

TARGET = Path("/mnt/ssd/SteamLibrary/steamapps/common/Ready Or Not/ReadyOrNot/Content/Paks")

# Quand compilé en onefile PyInstaller, l'exe se trouve dans BASE_DIR
# et les données embarquées sont extraites dans sys._MEIPASS
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
    VANILLA_MANIFEST = Path(sys._MEIPASS) / ".vanilla_manifest"
else:
    BASE_DIR = Path(__file__).resolve().parent
    VANILLA_MANIFEST = BASE_DIR / ".vanilla_manifest"

PAKS_DIR = BASE_DIR / "paks"

GREEN   = "\033[0;32m"
RED     = "\033[0;31m"
YELLOW  = "\033[1;33m"
CYAN    = "\033[0;36m"
RESET   = "\033[0m"
KEY_HL  = "\033[1;30;47m"  # gras noir sur fond blanc

BANNER = """\
:----::::::::::::::::------=+++=-+*###+=+====+******###*++-=--=-:=++=:::::::--------:--------:::::::
:::--::::::::::::::::::::.-+===:==**+-==++++**+++++**##+++-::::---==+=:::::::::::::::--------:::::::
:::::::::::::::::::::::..:+*===---=+****************+###*+=:::::==-==*-:::::----::-----------::--:::
-----::::::::::::::::::::=*==--+******************#***##+++-:--:--:.-==::::::::::::----------::::::-
------::::-------::::::::==-:=+***###*****#########%*+**+++--+*=-=---=++-::::::::::---:::=---::-::::
::::::::::::::::---:::::=-:::-=****#****###########%#**++++=--**-===---==+-:::-------:--=----::::-::
---:::--::::::::--:::::--:-:---+*********+=-======+*****++++-+**--=-=---==+-::::::---:::::---:::::::
:::--:--:::::--::::::::=--=--==+***+++=+*############*++==-=:::-:-:.::::-==+--:------:::-:---:::::::
==-::::-:::::::::::-+:-*+---:-:=+++-=*#%%%%%%%%%%%%%#####*++=-:::--:::::-====--------:::-::--:::::::
::---:::::::::::::-*+**==----::-=-=#%%%%%%%%%%%%%%%%%%%#####*+==----::-::-=-+-------::-:-:---:::::::
::::::::::::--::::=*==+=--:::-::=*#%%%%#**+++++*##%%%%%%######-::-++::-==--===--------::-:::::-----:
----:::::::::-::::-+--==:---::=*##%%%*--*****##***-===*#######=::-=::-===--===+--===-:::-::::---:::-
-=---::::::::--::::==:-=====:=*#%%##++=*###########**##*+++*#****--++::--==-===-:--:-=---:::::--::::
:::::::-==-=-:::::::--:---==-=#%#***#*#**#######%%%%#**##++=*****+-::=:.:-===-=-::-===----::::::::::
:::::--:-=:-=---::::::+-==-:=##=:*##*******##%%%%@@%##+=+++=*##**+-:::-::::-==--::--.:::::::::::::::
::::--:::++--=::::::::+===--*-:::*##**++++##%%@%@%%@##########%%%*-::-++----=+=--:-:....::::..::::::
:::=:::.::==--=:.:::::==--:-+=::-=*##**+**++##%%%%%%%%%%##%%%#%%%#=-+#**+**=+=.:--+.................
...:=:::.::==--=:.....-=::-++*-:-+###**%####%%%#%%%%%#%%%%%@%%%%%=--%%%###*+.:--==:.................
::..:-:::.::---=-.....:==-=*#*+==+%%%%#*%%%%%%%%%%%%#*#%%%%%%*++=--=*%%%%%#+--==--:.:::.......:::...
.....:-.::::-=--=-....:===*##*#*==+#%%%%##%%%%#+==+++=++++*+++-:-===%#%%%#=:-=..:::.:..........:....
......:=...::-=--=-...-*--%#**##==+*=+#%%#=+=======++++++===+++--#+=%%%%+-:-*#:..............:::....
........-:::.:-=--=:..=:.+%%**+=*+=:+=-=+==========---+++==--::+#*==#*=--=+#*##-...............:....
........:-:...:-=---:.*:.#%%*##+.:=+------======--------===:--==++----+*##***###-.............::....
..........=-:..:-=--=*#=.*#%%**+++++=-::--------=----------+*=----::=#*-:-*#-+##*...................
...........:-:-::=+--*##=+##%%**=====-=++:::-==--==-=---====+:--:--==++*:*%#+=:##-..................
....:::-:...:-::::-=-:+##++*#####%%%%#++*=-----=--======-===-=-:---=+++*#%%****#%#:.................
......:::.....-=-::==-=+=--=%++**#*%%%+:%#=--------=======---:--:-=+*#%%%%#+*#+=+*:.................
...::::::.......:=:-+=--+==--+...:-:#%#%*+-:::-:-=-======---::---+#######*#*++*****-................
...::::::........:=:-+=--=:..:-:::=**##--+=::::-----=======--=#%#######*++++=--+**#*+-.:..:...:-....
..................--::-:::::::::::=+*#*-++:::::-----====++=-=+-::*#*=::......--==++**+#+-.....::....
.......:..........:=::::--*-:::::-+*#*===-::::-::-:--=+#%@@%:.:-===-:......:-=::-==+++=++=..........
..................--:::::.:::::::-+#+:::::=-::--::::-#@@@@@@%+----::::------+***---=++==++..........
.................---::::::.:-:::::-=::::::----::--::=%@@@@@@@#---::-===---:=+###*=.:-==++...........
.................--::::::::-#*::::::-+=---======:::::+@@@@@@@@*-:----=---=+#%%%%%#=--===::==:.......
.................:=-:::::::::+=::::--------==-=--:::::#@@@@@@@%+::::---:-*####%%#**+=---+++++:......
...................--::::::::-=-::::-------====---::::=%@@@@@@@%=::::-+++######%%##*+-=+++++*=......
...................:-:::::::-=-=-=-----::::::::::--:.::*@@@@@@@%%=::++*###########:=+:======+*::....
............::::..:+*::::::::=+-=-----==-----=+++=--::-=%@@%#+==-##*-*+****#****##=-:.::-:-====.....
...........=:::-----=:::-:::::--+==-----========----=-::++====-==+#%#+#########*#***+:::-=-=--=-....
...........=::::::::::::-::::::==+==---:-------------::::=-=++=-=-+##+-+==-*###*=**#*=:-=-=====:....
...........-:::::::::::::::--:::+==::::..:-++==+==----:::---+--::==*##=-++*##*#****+==--=-+=--=-....
...........=::::::::::::::::::::::-=--:::=#+--++++--:::::::-::=+*#**###*-*#*+*+*###*+=-==---=-=:....
.............-*===--::::::::::::::-:--:::::+-:-+++:-++*+-.-=:*+##*##*##**#*****+*###*+---+=--=:.....
............-+======-.:::::=-::::::-:--::---=-:-=+-=+++==+*=*#######+*++++++*+++=#***+-:-----=......
..........++==++===:..::..:=+=::-:::----:--::--:-=-=+=+****+########*+++++++****==****+=----=.......
.........-=++=+***##***+-.::==-::-::::--:::::--::--=+--+***++*###*##*+++++++*#*#+::+**+=----=.......
.........-====-********+=--:::=:::-::::--:::::--::--=---***++++*#***-=++++++*#**+---=++++::--.......
........=++++++++**+*#*+=====:::::::::::--:::::-----==--:=*++++++***+*******##*+*=---=-=+--===+**+:.
.......-+=++++======-.:--------::::::::-:-:::::---::-=---=-=++*##************#*+++===--=--------=+:.
........-=-====+====-::::---:-----:::::::::::::.::::-=----====+++++++**********++*+====--:::-:::-=:.
........:--===+===-::::::--::---++-.:::::::..:....:::-----=*::-++++++**********++*+====--:::::::-=:.\
"""

def clean_name(filename: str) -> str:
    name = filename.removesuffix(".pak")
    return re.sub(r"^pakchunk\d+-", "", name)


def checkbox_select(files: list[str], title: str) -> list[str] | None:
    """Sélection interactive : ↑↓ naviguer, ESPACE cocher, A tout/rien, ENTRÉE valider, Q annuler."""
    selected = [False] * len(files)
    cursor = 0

    def draw(stdscr):
        nonlocal cursor
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN,   -1)
        curses.init_pair(2, curses.COLOR_GREEN,  -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_RED,    -1)

        while True:
            stdscr.erase()
            h, w = stdscr.getmaxyx()

            # En-tête
            stdscr.addstr(0, 0, f" {title}", curses.color_pair(1) | curses.A_BOLD)
            count_sel = sum(selected)
            stdscr.addstr(1, 0, f"  {count_sel}/{len(files)} sélectionné(s)", curses.color_pair(3))
            hint = " ↑↓ naviguer   SPC cocher   A tout/rien   ↵ valider   Q annuler"
            stdscr.addstr(2, 0, hint[:w - 1])
            stdscr.addstr(3, 0, "─" * min(w - 1, 60))

            start = 4
            visible = h - start - 1
            offset = max(0, cursor - visible + 1)

            for i, (fname, is_sel) in enumerate(zip(files, selected)):
                if not (offset <= i < offset + visible):
                    continue
                row = start + i - offset
                box  = "[✔]" if is_sel else "[ ]"
                line = f"  {box} {clean_name(fname)}"[:w - 1]

                if i == cursor:
                    stdscr.attron(curses.A_REVERSE)
                    stdscr.addstr(row, 0, line)
                    stdscr.attroff(curses.A_REVERSE)
                elif is_sel:
                    stdscr.addstr(row, 0, line, curses.color_pair(2))
                else:
                    stdscr.addstr(row, 0, line)

            stdscr.refresh()

            key = stdscr.getch()
            if key in (curses.KEY_UP, ord("k")):
                cursor = max(0, cursor - 1)
            elif key in (curses.KEY_DOWN, ord("j")):
                cursor = min(len(files) - 1, cursor + 1)
            elif key == ord(" "):
                selected[cursor] = not selected[cursor]
                cursor = min(len(files) - 1, cursor + 1)
            elif key in (ord("a"), ord("A")):
                val = not all(selected)
                selected[:] = [val] * len(files)
            elif key in (10, 13, curses.KEY_ENTER):
                return [f for f, s in zip(files, selected) if s]
            elif key in (ord("q"), ord("Q"), 27):
                return None

    return curses.wrapper(draw)


def load_vanilla_manifest() -> set[str]:
    return {line.strip() for line in VANILLA_MANIFEST.read_text().splitlines() if line.strip()}


def get_loaded_mods(vanilla: set[str]) -> list[str]:
    return sorted(f.name for f in TARGET.iterdir() if f.is_file() and f.name not in vanilla)


def get_available_mods() -> list[str]:
    return sorted(
        f.name for f in PAKS_DIR.iterdir()
        if f.is_file() and not (TARGET / f.name).exists()
    )


def do_unload(vanilla: set[str]) -> None:
    mods = get_loaded_mods(vanilla)
    if not mods:
        print(f"\n{YELLOW}[INFO]{RESET} Aucun mod détecté dans Paks/ — déjà en vanilla.")
        return

    selection = checkbox_select(mods, f"Décharger des mods  ({len(mods)} chargé(s))")

    if selection is None:
        print("Annulé.")
        return
    if not selection:
        print(f"{YELLOW}[INFO]{RESET} Aucune sélection.")
        return

    print(f"\n{YELLOW}[DÉCHARGEMENT]{RESET} Suppression de {len(selection)} mod(s)...\n")
    errors = 0
    for fname in selection:
        try:
            (TARGET / fname).unlink()
            print(f"  {GREEN}✔{RESET} {clean_name(fname)}")
        except OSError as e:
            print(f"  {RED}✘{RESET} Échec : {fname}  ({e})")
            errors += 1

    print()
    if errors == 0:
        print(f"{GREEN}[OK]{RESET} Déchargement terminé.")
    else:
        print(f"{YELLOW}[ATTENTION]{RESET} {errors} fichier(s) n'ont pas pu être supprimés.")


def do_load() -> None:
    mods = get_available_mods()
    if not mods:
        print(f"\n{YELLOW}[INFO]{RESET} Aucun nouveau mod à charger.")
        return

    selection = checkbox_select(mods, f"Charger des mods  ({len(mods)} disponible(s))")

    if selection is None:
        print("Annulé.")
        return
    if not selection:
        print(f"{YELLOW}[INFO]{RESET} Aucune sélection.")
        return

    print(f"\n{GREEN}[CHARGEMENT]{RESET} Copie de {len(selection)} mod(s)...\n")
    errors = 0
    for fname in selection:
        try:
            shutil.copy2(PAKS_DIR / fname, TARGET / fname)
            print(f"  {GREEN}✔{RESET} {clean_name(fname)}")
        except OSError as e:
            print(f"  {RED}✘{RESET} Échec : {fname}  ({e})")
            errors += 1

    print()
    if errors == 0:
        print(f"{GREEN}[OK]{RESET} Chargement terminé.")
    else:
        print(f"{YELLOW}[ATTENTION]{RESET} {errors} fichier(s) n'ont pas pu être copiés.")


def main() -> None:
    print(f"{CYAN}{BANNER}{RESET}")
    print(f"{CYAN}         Ready Or Not — Mod Manager{RESET}")
    print()

    if not TARGET.is_dir():
        print(f"{RED}[ERREUR]{RESET} Dossier cible introuvable :\n  {TARGET}")
        sys.exit(1)

    if not VANILLA_MANIFEST.exists():
        print(f"{RED}[ERREUR]{RESET} Manifeste vanilla introuvable : {VANILLA_MANIFEST}")
        sys.exit(1)

    if not PAKS_DIR.is_dir():
        print(f"{RED}[ERREUR]{RESET} Dossier paks/ introuvable :\n  {PAKS_DIR}")
        sys.exit(1)

    vanilla = load_vanilla_manifest()

    print("Que veux-tu faire ?\n")
    print(f"    {KEY_HL} 1 {RESET}  Décharger les mods  {YELLOW}(supprimer de Paks/){RESET}")
    print()
    print(f"    {KEY_HL} 2 {RESET}  Charger les mods    {YELLOW}(copier vers Paks/){RESET}")
    print()
    print(f"    {KEY_HL} q {RESET}  Quitter")
    print()

    choice = input("  Ton choix : ").strip().lower()
    print()

    match choice:
        case "1": do_unload(vanilla)
        case "2": do_load()
        case "q": print("Annulé.")
        case _:
            print(f"{RED}[ERREUR]{RESET} Choix invalide.")
            sys.exit(1)

    print()


if __name__ == "__main__":
    main()
