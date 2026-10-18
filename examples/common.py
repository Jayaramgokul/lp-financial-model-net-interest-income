"""Paths and plotting helpers shared by the examples."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
WORKBOOK = HERE.parent / "model" / "LP_financial_model_2013.xlsx"
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=120)
    plt.close(fig)
    print(f"  saved output/{name}")
