#!/usr/bin/python3

import argparse
import os
import pathlib
import subprocess

from colorize import Colorize


def main() -> None:
    """The main entry point to the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs=argparse.OPTIONAL, default=os.getcwd())
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    base = pathlib.Path(args.path).resolve()
    directories = [base.joinpath(entry) for entry in os.listdir(base)]
    directories = list(
        filter(
            lambda d: d.joinpath(".git").exists(),
            directories,
        )
    )

    print(f"Found {len(directories)} repositories:")

    for repository in directories:
        output = subprocess.check_output(
            ["git", "status"], cwd=repository
        ).decode(encoding="utf-8")

        if output.endswith("nothing to commit, working tree clean\n"):
            status = Colorize("OK").bold().color256(28)
            print(f"  {repository.name} {status}")
            continue
        else:
            status = Colorize("DIRTY").bold().color256(124)
            print(f"  {repository.name} {status}")

        if not args.verbose:
            # Optionally print additional information about each repository
            continue

        lines = output.splitlines()
        _ = lines.pop(0)  # The first line is always "On branch ~".

        i = 0
        while i < len(lines):
            line = lines[i]
            i += 1

            match line.strip():
                case "Changes to be committed:":
                    print(
                        "    "
                        + Colorize("Changes to be committed:").color256(245)
                    )
                    while i < len(lines) and (line := lines[i].strip()) != "":
                        i += 1

                        if line.startswith("("):
                            continue

                        action, file = [s.strip() for s in line.split(":")]
                        file = Colorize(file).color256(250)
                        letter = get_letter(action=action)
                        print(f"      {letter} {file}")
                case "Changes not staged for commit:":
                    print("    " + Colorize("Unstaged changes:").color256(245))
                    while i < len(lines) and (line := lines[i].strip()) != "":
                        i += 1

                        if line.startswith("("):
                            continue

                        action, file = [s.strip() for s in line.split(":")]
                        letter = get_letter(action=action)
                        file = Colorize(file).color256(250)
                        print(f"      {letter} {file}")
                case "Untracked files:":
                    print("    " + Colorize("Untracked files:").color256(245))
                    while i < len(lines) and (line := lines[i].strip()) != "":
                        i += 1

                        if line.startswith("("):
                            continue

                        letter = Colorize("U").color256(238).bold()
                        file = Colorize(line.strip()).color256(250)
                        print(f"      {letter} {file}")


def get_letter(action: str) -> Colorize:
    match action:
        case "new file":
            letter = Colorize("N").bold().color256(28)
        case "modified":
            letter = Colorize("E").bold().color256(3)
        case "deleted":
            letter = Colorize("D").bold().color256(88)
        case _:
            raise AssertionError("unreachable")

    return letter


if __name__ == "__main__":
    main()
