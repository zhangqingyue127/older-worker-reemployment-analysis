from __future__ import annotations

from pathlib import Path
from typing import List

import jieba.posseg as pseg
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


CORPUS_PATH = Path("data/processed/combined_corpus.txt")
RESULTS_DIR = Path("results")


def extract_candidate_words(text: str) -> List[str]:
    """
    Keep only nouns and adjectives to obtain more interpretable keywords.
    """
    words = pseg.cut(text)
    return [
        word
        for word, flag in words
        if word.strip() and (flag.startswith("n") or flag.startswith("a"))
    ]


def main() -> None:
    """
    Compute TF-IDF scores over a single merged corpus document.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    text = CORPUS_PATH.read_text(encoding="utf-8")
    words = extract_candidate_words(text)
    processed_text = " ".join(words)

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([processed_text])
    scores = matrix.toarray()[0]
    vocabulary = vectorizer.get_feature_names_out()

    keyword_df = pd.DataFrame({"term": vocabulary, "tfidf": scores})
    keyword_df = keyword_df.sort_values("tfidf", ascending=False).reset_index(drop=True)
    keyword_df.to_csv(RESULTS_DIR / "tfidf_keywords.csv", index=False, encoding="utf-8")

    print(keyword_df.head(30).to_string(index=False))


if __name__ == "__main__":
    main()
