"""Shared figure styling and PDF/PNG export."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE = "#508fac"
ORANGE = "#d26a28"
GREEN = "#2f7b62"
RED = "#ab4242"


def configure():
    plt.rcParams.update(
        {
            "font.size": 12,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 130,
            "savefig.bbox": "tight",
            "axes.grid": True,
            "grid.alpha": 0.22,
            "font.family": "serif",
            "font.serif": ["CMU Serif", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "axes.labelsize": 12,
        }
    )


def exporter(directory):
    directory.mkdir(parents=True, exist_ok=True)

    def save(figure, name):
        figure.savefig(directory / (name + ".pdf"))
        figure.savefig(directory / (name + ".png"), dpi=170)
        plt.close(figure)

    return save
