# indexer/tfidf_vectorizer.py
import math
import json
from collections import Counter, defaultdict
from typing import List, Dict

from .tokenizer import tokenize

class TFIDFVectorizer:
    """
    Simple TF-IDF vectorizer.
    - fit(documents): documents is a list of raw text strings (HTML should be stripped before).
    - transform(doc) / transform_many(docs): produce sparse dict {term: weight}.
    - save/load: write vocabulary, idf, doc_norms, and optionally document vectors.
    """

    def __init__(self, min_df: int = 1, use_sublinear_tf: bool = False):
        self.min_df = min_df
        self.use_sublinear_tf = use_sublinear_tf
        self.vocab = {}               # term -> term_index
        self.idf = {}                 # term -> idf value
        self.df = {}                  # term -> document frequency
        self.N = 0                    # number of documents

    def fit(self, documents: List[str]):
        """
        Build vocabulary and idf from a list of raw texts.
        """
        self.N = len(documents)
        df_counts = Counter()

        # compute df
        for doc in documents:
            tokens = set(tokenize(doc))
            df_counts.update(tokens)

        # apply min_df filter
        vocab = {}
        idx = 0
        for term, df in df_counts.items():
            if df >= self.min_df:
                vocab[term] = idx
                idx += 1

        self.vocab = vocab
        self.df = {t: df_counts[t] for t in vocab.keys()}

        # idf with smoothing: idf = log( (N - df + 0.5) / (df + 0.5) ) OR classic idf
        # We'll use classic smoothed idf: log((N + 1) / (df + 1)) + 1
        self.idf = {}
        for term, df in self.df.items():
            self.idf[term] = math.log((self.N + 1) / (df + 1)) + 1.0

    def _tf(self, term, term_counts: Dict[str, int]) -> float:
        raw_tf = term_counts.get(term, 0)
        if raw_tf == 0:
            return 0.0
        if self.use_sublinear_tf:
            return 1.0 + math.log(raw_tf)
        return float(raw_tf)

    def transform(self, document: str) -> Dict[str, float]:
        """
        Transform a single document into sparse TF-IDF vector: {term: weight}
        Only includes terms in the learned vocabulary.
        """
        tokens = tokenize(document)
        term_counts = Counter(tokens)

        # compute tf-idf
        vec = {}
        for term in term_counts.keys():
            if term not in self.vocab:
                continue
            tf = self._tf(term, term_counts)
            vec[term] = tf * self.idf.get(term, 0.0)

        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vec.values()))
        if norm > 0:
            for term in list(vec.keys()):
                vec[term] = vec[term] / norm

        return vec

    def transform_many(self, documents: List[str]) -> List[Dict[str, float]]:
        return [self.transform(doc) for doc in documents]

    def save(self, path: str):
        """
        Save model to JSON (vocab, idf, df, N, min_df, use_sublinear_tf)
        """
        payload = {
            "min_df": self.min_df,
            "use_sublinear_tf": self.use_sublinear_tf,
            "N": self.N,
            "vocab": list(self.vocab.keys()),   # order matters only for human-readability
            "idf": self.idf,
            "df": self.df,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    @classmethod
    def load(cls, path: str):
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        obj = cls(min_df=payload.get("min_df", 1), use_sublinear_tf=payload.get("use_sublinear_tf", False))
        obj.N = payload.get("N", 0)
        # rebuild vocab mapping
        vocab_list = payload.get("vocab", [])
        obj.vocab = {t: i for i, t in enumerate(vocab_list)}
        obj.idf = payload.get("idf", {})
        obj.df = payload.get("df", {})
        return obj
