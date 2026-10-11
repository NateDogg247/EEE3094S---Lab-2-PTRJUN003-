"""Create a complete source listing with an inventory and topic guide."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {".py", ".m", ".sh", ".tex", ".asc", ".sch", ".pro"}


def build():
    files = sorted(
        p
        for p in ROOT.rglob("*")
        if p.is_file() and (p.suffix in EXTENSIONS or p.name == "lab_parameters.json")
    )
    text = [
        "COMPLETE ORGANISED SOURCE CODE: PTRJUN003 LAB 2",
        "Read CODE_GUIDE.md and calculations/PTRJUN003_Lab2_Calculations.pdf first.",
        "Python generated the report. MATLAB source is supplied and was not executed here.",
        "",
        "SOURCE INVENTORY",
    ]
    text.extend(str(p.relative_to(ROOT)) for p in files)
    for path in files:
        text.extend(
            [
                "",
                "=" * 80,
                "FILE: " + str(path.relative_to(ROOT)),
                "=" * 80,
                path.read_text(),
            ]
        )
    (ROOT / "ALL_SOURCE_CODE.txt").write_text("\n".join(text) + "\n")
    print(f"Listed {len(files)} source files.")


if __name__ == "__main__":
    build()
