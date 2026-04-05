from __future__ import annotations

import json
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from gensim.models import Word2Vec


FACTORS_PATH = Path("config/factors.json")
RESULTS_DIR = Path("results")


def main() -> None:
    """
    Build the factor-level asymmetric similarity matrix.

    The design follows the original project logic:
    - define keyword groups for each factor
    - train a Word2Vec model on those keyword groups
    - compute pairwise cross-factor similarity
    - keep the top-3 cross-keyword similarities
    - apply a nonlinear amplification step
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    factor_items = json.loads(FACTORS_PATH.read_text(encoding="utf-8"))
    factor_names = [item["name_en"] for item in factor_items]
    factor_codes = [item["code"] for item in factor_items]
    factor_keywords = [item["keywords"] for item in factor_items]

    model = Word2Vec(
        sentences=factor_keywords,
        vector_size=100,
        window=5,
        min_count=1,
        workers=1,
        sg=1,
        seed=42,
    )

    alpha = 5.0
    matrix = np.zeros((len(factor_keywords), len(factor_keywords)), dtype=float)

    for i, keywords_i in enumerate(factor_keywords):
        for j, keywords_j in enumerate(factor_keywords):
            if i == j:
                matrix[i, j] = 1.0
                continue

            keyword_scores = []
            for word_i in keywords_i:
                sims = []
                for word_j in keywords_j:
                    sims.append(model.wv.similarity(word_i, word_j))
                sims = sorted(sims, reverse=True)[:3]
                keyword_scores.append(float(np.mean(sims)))

            score = float(np.mean(keyword_scores))
            matrix[i, j] = np.exp(alpha * score) - 1.0

    matrix /= matrix.max()

    matrix_df = pd.DataFrame(matrix, index=factor_codes, columns=factor_codes)
    matrix_df.to_csv(RESULTS_DIR / "factor_similarity_matrix.csv", encoding="utf-8")
    print(matrix_df.round(4).to_string())


if __name__ == "__main__":
    main()
