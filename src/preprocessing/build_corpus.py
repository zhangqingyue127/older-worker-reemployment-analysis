from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
SOURCE_FILES = {
    "bilibili": RAW_DIR / "bilibili_danmaku.txt",
    "weibo": RAW_DIR / "weibo_comments.txt",
    "policy": RAW_DIR / "policy_documents.txt",
}


def normalize_text(text: str) -> str:
    """
    Apply light normalization to Chinese text.

    The goal here is not aggressive cleaning, but readable normalization:
    - trim whitespace
    - remove BOM artifacts
    - collapse repeated spaces
    """
    text = text.replace("\ufeff", "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def load_lines(path: Path) -> List[str]:
    """
    Read a text file and return non-empty normalized lines.
    """
    content = path.read_text(encoding="utf-8")
    return [
        normalize_text(line)
        for line in content.splitlines()
        if normalize_text(line)
    ]


def build_corpus() -> pd.DataFrame:
    """
    Merge all raw sources into a single deduplicated dataframe.
    """
    rows = []
    for source_name, path in SOURCE_FILES.items():
        for line in load_lines(path):
            rows.append({"source": source_name, "text": line})

    df = pd.DataFrame(rows).drop_duplicates(subset=["text"]).reset_index(drop=True)
    return df


def main() -> None:
    """
    Build and export the merged corpus.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    corpus_df = build_corpus()
    corpus_df.to_csv(PROCESSED_DIR / "combined_corpus.csv", index=False, encoding="utf-8")
    (PROCESSED_DIR / "combined_corpus.txt").write_text(
        "\n".join(corpus_df["text"].tolist()),
        encoding="utf-8",
    )

    print(f"Saved {len(corpus_df)} unique text records.")


if __name__ == "__main__":
    main()
