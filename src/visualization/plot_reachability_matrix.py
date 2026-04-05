from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path("results/reachability_matrix_threshold_0_72.csv")
OUTPUT_PATH = Path("assets/reachability_matrix.png")


def main() -> None:
    """
    Plot the reachability matrix as a heatmap-style image.
    """
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH, index_col=0)

    plt.figure(figsize=(6.5, 5.4))
    plt.imshow(df.values, aspect="equal")
    plt.xticks(range(len(df.columns)), df.columns, rotation=45, ha="right")
    plt.yticks(range(len(df.index)), df.index)
    plt.title("Reachability Matrix (Threshold = 0.72)")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
