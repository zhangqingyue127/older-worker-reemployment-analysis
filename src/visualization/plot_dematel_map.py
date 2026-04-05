from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path("results/dematel_scores.csv")
OUTPUT_PATH = Path("assets/dematel_cause_effect_map.png")


def main() -> None:
    """
    Plot the DEMATEL prominence-relation map.
    """
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    plt.figure(figsize=(8, 6))
    for _, row in df.iterrows():
        plt.scatter(row["prominence"], row["relation"], s=50)
        plt.text(row["prominence"] + 0.01, row["relation"] + 0.005, row["code"], fontsize=9)

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.xlabel("Prominence (D + C)")
    plt.ylabel("Relation (D - C)")
    plt.title("DEMATEL Cause–Effect Map")
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
