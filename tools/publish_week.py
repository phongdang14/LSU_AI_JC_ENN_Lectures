#!/usr/bin/env python3
"""Stage one week of course material for publication.

Usage:  python3 tools/publish_week.py N

Copies Lecture N's notes and notebook out of the working tree (../output) into
lectures/, copies Lecture N-1's solutions (the one-week delay), updates the
status table in README.md, and stages everything. It stops short of committing
so you can read the diff first.

N may be 6, meaning "publish Lecture 5's solutions only" -- the final week.
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


def copy(src: Path, dest_dir: Path) -> Path:
    """Copy one file into dest_dir, creating it, and return the destination."""
    if not src.exists():
        sys.exit(f"missing source file: {src}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    print(f"  + {dest.relative_to(REPO)}")
    return dest


def mark(readme: str, row: int, column: int) -> str:
    """Set one cell of the status table to a tick. Columns: 0 notes, 1 notebook, 2 solutions."""
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
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        sys.exit(__doc__)
    week = int(sys.argv[1])
    if not 1 <= week <= 6:
        sys.exit("week must be between 1 and 6")

    readme_path = REPO / "README.md"
    readme = readme_path.read_text()

    if week <= 5:
        print(f"Lecture {week}:")
        folder = REPO / "lectures" / SLUGS[week]
        copy(PDFS / f"lecture_{week:02d}_notes.pdf", folder)
        notebooks = sorted(NBS.glob(f"lecture_{week:02d}_*.ipynb"))
        if not notebooks:
            sys.exit(f"no notebook found for lecture {week}")
        for nb in notebooks:
            copy(nb, folder)
        readme = mark(readme, week, 0)
        readme = mark(readme, week, 1)

    previous = week - 1
    if previous >= 1:
        print(f"Lecture {previous} solutions (one-week delay):")
        copy(PDFS / f"lecture_{previous:02d}_solutions.pdf", REPO / "lectures" / SLUGS[previous])
        readme = mark(readme, previous, 2)

    readme_path.write_text(readme)
    print("  ~ README.md status table updated")

    subprocess.run(["git", "add", "-A"], cwd=REPO, check=True)
    print("\nStaged. Review and push with:\n")
    if week <= 5:
        msg = f"Publish Lecture {week}" + (f" and Lecture {previous} solutions" if previous >= 1 else "")
    else:
        msg = f"Publish Lecture {previous} solutions"
    print("  git -C . diff --cached --stat")
    print(f'  git commit -m "{msg}"')
    print("  git push\n")


if __name__ == "__main__":
    main()
