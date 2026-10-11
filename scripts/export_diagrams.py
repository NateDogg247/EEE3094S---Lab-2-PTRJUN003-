"""Export the report's exact TikZ/Circuitikz diagrams as vector PDF and PNG."""

from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "report/figures"
SOURCE = ROOT / "report/sections/body.tex"
DIAGRAMS = [
    ("Forces and Differential Equation", "tikzpicture", "free_body_diagram"),
    ("Complete Signal Architecture", "tikzpicture", "system_block_diagram"),
    ("Step-Test Circuit and Recorded Input", "circuitikz", "identification_step_circuit"),
]


def export():
    source = SOURCE.read_text()
    preamble = r"""\documentclass[12pt,border=3mm]{standalone}
\usepackage{amsmath,xcolor,tikz,circuitikz}
\usetikzlibrary{arrows.meta,positioning,calc}
\definecolor{AngelBlue}{HTML}{8FC9E6}
\newcommand{\unit}[1]{\,\mathrm{#1}}
\begin{document}
"""
    with tempfile.TemporaryDirectory(prefix="lab2_diagrams_") as directory:
        work = Path(directory)
        for section, environment, name in DIAGRAMS:
            start = source.index(r"\begin{" + environment + "}", source.index(section))
            end_marker = r"\end{" + environment + "}"
            end = source.index(end_marker, start) + len(end_marker)
            diagram = source[start:end]
            (work / f"{name}.tex").write_text(preamble + diagram + "\n\\end{document}\n")
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{name}.tex"],
                cwd=work, check=True, stdout=subprocess.DEVNULL,
            )
            (FIGURES / f"{name}.pdf").write_bytes((work / f"{name}.pdf").read_bytes())
            subprocess.run(
                ["pdftocairo", "-singlefile", "-scale-to", "2400", "-png",
                 str(FIGURES / f"{name}.pdf"), str(FIGURES / name)], check=True,
            )
            print(f"Exported {name}.pdf and {name}.png")


if __name__ == "__main__":
    export()
