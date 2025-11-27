# search/query_processor.py
import json
import math
from collections import Counter
from indexer.tokenizer import tokenize
from indexer.tfidf_vectorizer import TFIDFVectorizer

class QueryProcessor:
    """
    Loads:
    - index.json (inverted index + doc vectors + doc paths)
    - tfidf_model.json (vocab, idf)
    
    Converts user query → TF-IDF vector → list of matching documents.
    """

    def __init__(self, index_path="data/index.json", model_path="data/tfidf_model.json"):
        # load index
        with open(index_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.inverted_index = data["inverted_index"]
        self.doc_vectors = data["doc_vectors"]
        self.doc_paths = data["doc_paths"]
        self.doc_lengths = data["doc_lengths"]
        self.meta = data["meta"]

        # load tfidf model
        self.vectorizer = TFIDFVectorizer.load(model_path)

        # cache doc_ids
        self.doc_ids = list(self.doc_vectors.keys())

    def vectorize_query(self, query: str):
        """Convert the query into a TF-IDF vector (sparse dict)."""
        return self.vectorizer.transform(query)

    def get_candidate_docs(self, query_terms):
        """
        Return a set of doc_ids containing ANY of the query terms
        (OR search behavior).
        """
        candidates = set()
        for term in query_terms:
            if term in self.inverted_index:
                candidates.update(self.inverted_index[term].keys())
        return candidates

    def search(self, query, top_k=10):
        """
        Full search pipeline:
        1. Tokenize query
        2. Vectorize query (TF-IDF)
        3. Find candidate docs
        4. Score using cosine similarity
        5. Return sorted results
        """
        tokens = tokenize(query)
        if not tokens:
            return []

        q_vec = self.vectorize_query(query)
        candidate_docs = self.get_candidate_docs(tokens)

        results = []
        for doc_id in candidate_docs:
            d_vec = self.doc_vectors.get(doc_id, {})
            score = cosine_similarity(q_vec, d_vec)
            if score > 0:
                results.append((doc_id, score))

        # sort by score desc
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]


def cosine_similarity(v1, v2):
    """Manually compute cosine similarity for sparse dicts."""
    if not v1 or not v2:
        return 0.0

    # dot product
    dot = sum(v1.get(t, 0) * v2.get(t, 0) for t in v1.keys())

    # norms
    norm1 = math.sqrt(sum(v * v for v in v1.values()))
    norm2 = math.sqrt(sum(v * v for v in v2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)
