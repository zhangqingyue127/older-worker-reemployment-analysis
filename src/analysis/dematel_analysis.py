from __future__ import annotations

from pathlib import Path

import pandas as pd


MATRIX_PATH = Path("results/factor_similarity_matrix.csv")
RESULTS_DIR = Path("results")


def main() -> None:
    """
    Compute DEMATEL dispatching degree, receiving degree, prominence, and relation.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    matrix_df = pd.read_csv(MATRIX_PATH, index_col=0)
    matrix = matrix_df.values

    dispatching_degree = matrix.sum(axis=1)
    receiving_degree = matrix.sum(axis=0)
    prominence = dispatching_degree + receiving_degree
    relation = dispatching_degree - receiving_degree

    results = pd.DataFrame(
        {
            "code": matrix_df.index,
            "dispatching_degree": dispatching_degree,
            "receiving_degree": receiving_degree,
            "prominence": prominence,
            "relation": relation,
            "factor_type": ["cause" if value > 0 else "effect" for value in relation],
        }
    )

    results.to_csv(RESULTS_DIR / "dematel_scores.csv", index=False, encoding="utf-8")
    print(results.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
