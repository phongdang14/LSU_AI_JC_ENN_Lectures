#!/usr/bin/env python3
"""Stage one week of course material for publication.

Usage:  python3 tools/publish_week.py N [--without-solutions] [--no-stage]

Copies Lecture N's notes, notebook and solutions out of the working tree
(../output) into lectures/, updates the status table in README.md, and stages
everything. It stops short of committing so you can read the diff first.

  --without-solutions  publish the notes and notebook only, and tick just those
                       two cells, so the README keeps telling the truth. Run the
                       command again without the flag when the solutions go out.
  --no-stage           skip "git add"; copy the files and leave staging to you.

Nothing is ever moved or removed from ../output -- this only reads from it.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

SLUGS = {
    1: "lecture-01-what-should-rotate",
    2: "lecture-02-features-have-geometric-types",
    3: "lecture-03-how-geometric-types-combine",
    4: "lecture-04-from-couplings-to-a-network",
    5: "lecture-05-build-a-physical-so3-enn",
}

REPO = Path(__file__).resolve().parent.parent
SRC = REPO.parent / "output"                      # the ENN working tree
PDFS = SRC / "pdf" / "so3_enn_series"
NBS = SRC / "notebooks" / "so3_enn_series"


def copy(src: Path, dest_dir: Path) -> None:
    """Copy one file into dest_dir, creating it if needed."""
    if not src.exists():
        sys.exit(f"missing source file: {src}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest_dir / src.name)
    print(f"  + {(dest_dir / src.name).relative_to(REPO)}")


def mark(readme: str, row: int, column: int) -> str:
    """Tick one cell of the status table. Columns: 0 notes, 1 notebook, 2 solutions."""
    lines = readme.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(rf"^\|\s*{row}\s*\|", line):
            cells = line.split("|")
            # cells[0] is empty, 1=number, 2=title, 3=question, 4..6 = status columns
            target = 4 + column
            if cells[target].strip() != "✅":
                cells[target] = " ✅ "
                lines[i] = "|".join(cells)
            return "".join(lines)
    sys.exit(f"no row for lecture {row} in the README status table")


def main() -> None:
    args = sys.argv[1:]
    with_solutions = "--without-solutions" not in args
    stage = "--no-stage" not in args
    args = [a for a in args if not a.startswith("--")]
    if len(args) != 1 or not args[0].isdigit():
        sys.exit(__doc__)
    week = int(args[0])
    if week not in SLUGS:
        sys.exit("week must be between 1 and 5")

    readme_path = REPO / "README.md"
    readme = readme_path.read_text()
    folder = REPO / "lectures" / SLUGS[week]

    print(f"Lecture {week}:")
    copy(PDFS / f"lecture_{week:02d}_notes.pdf", folder)
    notebooks = sorted(NBS.glob(f"lecture_{week:02d}_*.ipynb"))
    if not notebooks:
        sys.exit(f"no notebook found for lecture {week}")
    for nb in notebooks:
        copy(nb, folder)
    if with_solutions:
        copy(PDFS / f"lecture_{week:02d}_solutions.pdf", folder)
    else:
        print("  . solutions held back (--without-solutions)")

    for column in (0, 1, 2) if with_solutions else (0, 1):
        readme = mark(readme, week, column)
    readme_path.write_text(readme)
    print("  ~ README.md status table updated")

    subject = f"Publish Lecture {week}" + ("" if with_solutions else " notes and notebook")
    if stage:
        subprocess.run(["git", "add", "-A"], cwd=REPO, check=True)
        print("\nStaged. Review and push with:\n")
        print("  git diff --cached --stat")
    else:
        print("\nCopied, not staged. Review and push with:\n")
        print("  git add -A && git diff --cached --stat")
    print(f'  git commit -m "{subject}"')
    print("  git push\n")


if __name__ == "__main__":
    main()
