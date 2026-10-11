"""Make portable clickable indexes for the report's local folder links."""

from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
folders = [
    ".",
    "report",
    "data",
    "data/session1",
    "data/session2",
    "analysis",
    "matlab",
    "hardware",
    "results",
    "scripts",
    "config",
    "calculations",
    "analysis/modules",
    "matlab/config",
    "matlab/identification",
    "matlab/design",
    "matlab/validation",
    "matlab/simulink",
]
for folder in folders:
    p = ROOT / folder
    links = []
    for f in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        if (
            f.name.startswith(".")
            or f.name == "__pycache__"
            or f.name == "index.html"
            or f.suffix
            in [".log", ".aux", ".toc", ".out", ".fls", ".fdb_latexmk", ".lof", ".lot"]
            or f.name == "main.pdf"
        ):
            continue
        target = quote(f.name) + ("/" if f.is_dir() else "")
        links.append(
            '<li><a href="'
            + target
            + '">'
            + escape(f.name)
            + ("/" if f.is_dir() else "")
            + "</a></li>"
        )
    if folder == ".":
        links.insert(
            0, '<li><a href="report/PTRJUN003_Lab2_Report.pdf">Compiled report</a></li>'
        )
    title = "EEE3094S Lab 2 / " + folder
    parent = (
        ""
        if folder == "."
        else '<p><a href="'
        + ("../" * len(Path(folder).parts))
        + 'index.html">Project home</a></p>'
    )
    html = (
        '<!doctype html><meta charset="utf-8"><title>'
        + escape(title)
        + "</title><style>body{font:16px system-ui;max-width:850px;margin:50px auto;padding:0 25px;color:#174c66}li{margin:12px 0}a{color:#176795}p{line-height:1.6}</style><h1>"
        + escape(title)
        + "</h1>"
        + parent
        + "<p>Supporting files for Junaid Allan Pieters, PTRJUN003. Open the report for measured results, model predictions and their limits.</p><ul>"
        + "".join(links)
        + "</ul>"
    )
    (p / "index.html").write_text(html)
print("Portable folder indexes created.")
