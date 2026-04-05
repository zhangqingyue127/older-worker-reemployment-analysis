from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


MATRIX_PATH = Path("results/factor_similarity_matrix.csv")
RESULTS_DIR = Path("results")
DEFAULT_THRESHOLD = 0.72


def derive_levels(reachability: np.ndarray, labels: List[str]) -> pd.DataFrame:
    """
    Recover ISM levels from a binary reachability matrix.
    """
    remaining = list(range(len(labels)))
    rows = []
    level_id = 1

    while remaining:
        current = []
        for i in remaining:
            reachable_set = {j for j in remaining if reachability[i, j] == 1}
            antecedent_set = {j for j in remaining if reachability[j, i] == 1}
            if reachable_set & antecedent_set == reachable_set:
                current.append(i)

        for idx in current:
            rows.append({"level": level_id, "code": labels[idx]})

        remaining = [idx for idx in remaining if idx not in current]
        level_id += 1

    return pd.DataFrame(rows)


def main(threshold: float = DEFAULT_THRESHOLD) -> None:
    """
    Convert the factor similarity matrix into a reachability matrix and recover levels.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    matrix_df = pd.read_csv(MATRIX_PATH, index_col=0)
    reachability = (matrix_df.values >= threshold).astype(int)

    reachability_df = pd.DataFrame(reachability, index=matrix_df.index, columns=matrix_df.columns)
    reachability_df.to_csv(
        RESULTS_DIR / f"reachability_matrix_threshold_{str(threshold).replace('.', '_')}.csv",
        encoding="utf-8",
    )

    levels_df = derive_levels(reachability, list(matrix_df.index))
    levels_df.to_csv(RESULTS_DIR / "ism_levels_from_reachability.csv", index=False, encoding="utf-8")

    print(reachability_df.to_string())
    print()
    print(levels_df.to_string(index=False))


if __name__ == "__main__":
    main()
