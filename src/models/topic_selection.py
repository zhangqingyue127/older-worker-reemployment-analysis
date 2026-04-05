from __future__ import annotations

import re
import string
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import jieba
from gensim import corpora
from gensim.models import LdaModel
import matplotlib.pyplot as plt


CORPUS_PATH = Path("data/processed/combined_corpus.txt")
STOPWORDS_PATH = Path("config/stopwords.txt")
RESULTS_DIR = Path("results")


def load_stopwords(path: Path) -> set[str]:
    """
    Load stopwords from a text file.
    """
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def tokenize_documents(lines: Sequence[str], stopwords: set[str]) -> List[List[str]]:
    """
    Segment Chinese text with `jieba` and remove very short or stop words.
    """
    punctuation = string.punctuation + "，。！？、：；“”‘’（）()【】[]《》"
    tokenized: List[List[str]] = []

    for line in lines:
        line = re.sub(rf"[{re.escape(punctuation)}]+", "", line)
        tokens = [
            token.strip()
            for token in jieba.cut(line, cut_all=False)
            if token.strip() and token not in stopwords and len(token.strip()) > 1
        ]
        if tokens:
            tokenized.append(tokens)

    return tokenized


def build_gensim_objects(tokenized_docs: List[List[str]]) -> Tuple[corpora.Dictionary, list]:
    """
    Build the dictionary and BoW corpus for gensim models.
    """
    dictionary = corpora.Dictionary(tokenized_docs)
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]
    return dictionary, corpus


def main() -> None:
    """
    Train multiple LDA models and compare topic counts with log perplexity.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    stopwords = load_stopwords(STOPWORDS_PATH)
    lines = [line for line in CORPUS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    tokenized_docs = tokenize_documents(lines, stopwords)
    dictionary, corpus = build_gensim_objects(tokenized_docs)

    topic_range = range(2, 16)
    scores: List[Tuple[int, float]] = []

    for num_topics in topic_range:
        model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=num_topics,
            random_state=42,
            passes=20,
        )
        scores.append((num_topics, model.log_perplexity(corpus)))
        print(f"num_topics={num_topics}, log_perplexity={scores[-1][1]:.4f}")

    # Save the comparison table.
    with (RESULTS_DIR / "lda_topic_selection.csv").open("w", encoding="utf-8") as file:
        file.write("num_topics,log_perplexity\n")
        for num_topics, score in scores:
            file.write(f"{num_topics},{score}\n")

    # Save the plot.
    plt.figure(figsize=(7.5, 4.5))
    plt.plot([x for x, _ in scores], [y for _, y in scores], marker="o")
    plt.xlabel("Number of topics")
    plt.ylabel("Log perplexity")
    plt.title("LDA topic-count comparison")
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "lda_topic_selection.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    main()
