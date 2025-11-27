# search/ranker.py
from .snippet import generate_snippet

class SearchRanker:
    """
    Takes (doc_id, score) pairs from QueryProcessor.search
    and converts them into final result objects:
       { "doc_id": ..., "score": ..., "snippet": ..., "path": ... }
    """

    def __init__(self, doc_paths):
        self.doc_paths = doc_paths

    def rank_results(self, results, query):
        """
        Add formatted snippet and document path info.
        """
        ranked = []
        for doc_id, score in results:
            path = self.doc_paths.get(doc_id, "")

            # Load text & generate snippet
            snippet = generate_snippet(path, query)

            ranked.append({
                "doc_id": doc_id,
                "score": round(score, 4),
                "path": path,
                "snippet": snippet
            })
        return ranked
