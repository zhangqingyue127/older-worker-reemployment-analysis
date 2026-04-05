from __future__ import annotations

import json
import re
import string
from pathlib import Path
from typing import List

import jieba
from gensim import corpora
from gensim.models import LdaModel


CORPUS_PATH = Path("data/processed/combined_corpus.txt")
STOPWORDS_PATH = Path("config/stopwords.txt")
RESULTS_DIR = Path("results")
NUM_TOPICS = 10


def load_stopwords() -> set[str]:
    """
    Load stopwords from the project configuration.
    """
    return {line.strip() for line in STOPWORDS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()}


def preprocess(lines: List[str], stopwords: set[str]) -> List[List[str]]:
    """
    Clean punctuation and segment Chinese text into tokens.
    """
    punctuation = string.punctuation + "，。！？、：；“”‘’（）()【】[]《》"
    tokenized_docs: List[List[str]] = []

    for line in lines:
        line = re.sub(rf"[{re.escape(punctuation)}]+", "", line)
        tokens = [
            token.strip()
            for token in jieba.cut(line, cut_all=False)
            if token.strip() and token not in stopwords and len(token.strip()) > 1
        ]
        if tokens:
            tokenized_docs.append(tokens)

    return tokenized_docs


def main() -> None:
    """
    Train the final LDA model and export top words for each topic.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    lines = [line for line in CORPUS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    stopwords = load_stopwords()
    tokenized_docs = preprocess(lines, stopwords)

    dictionary = corpora.Dictionary(tokenized_docs)
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=NUM_TOPICS,
        random_state=42,
        passes=20,
    )

    topic_rows = []
    for topic_id in range(NUM_TOPICS):
        words = lda_model.show_topic(topic_id, topn=12)
        topic_rows.append(
            {
                "topic_id": topic_id,
                "top_words": [word for word, _ in words],
                "weighted_terms": [{"word": word, "weight": float(weight)} for word, weight in words],
            }
        )
        print(f"Topic {topic_id}: " + ", ".join(word for word, _ in words))

    (RESULTS_DIR / "lda_topics.json").write_text(
        json.dumps(topic_rows, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
