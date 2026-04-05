from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path("results/source_overview.csv")
OUTPUT_PATH = Path("assets/source_overview.png")


def main() -> None:
    """
    Plot a simple overview of source sizes.
    """
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    x = range(len(df))
    width = 0.38

    plt.figure(figsize=(9, 4.8))
    plt.bar([i - width / 2 for i in x], df["documents"], width=width, label="Documents")
    plt.bar([i + width / 2 for i in x], df["characters"], width=width, label="Characters")
    plt.xticks(list(x), df["source"])
    plt.ylabel("Count")
    plt.title("Source Overview")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
