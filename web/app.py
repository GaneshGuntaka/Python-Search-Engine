from flask import Flask, render_template, request
import json
import os
import sys

# Fix import paths (go 2 folders up: /PythonSearchEngine)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from search.query_processor import process_query
from search.ranker import rank_documents
from search.snippet import generate_snippet

app = Flask(__name__)

# Load index.json
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "index.json")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index_data = json.load(f)

DOCUMENTS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "pages")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")

    if query.strip() == "":
        return render_template("index.html", results=[], query=query)

    # Step 1 → Process Query (tokenize, clean)
    tokens = process_query(query)

    # Step 2 → Rank documents
    ranked_results = rank_documents(tokens, index_data)

    # Step 3 → Build result list with snippets
    results = []
    for doc_id, score in ranked_results[:10]:  # top 10 results
        doc_path = os.path.join(DOCUMENTS_PATH, doc_id)

        # Read original text for snippet generation
        try:
            with open(doc_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except:
            content = ""

        snippet = generate_snippet(content, tokens)

        results.append({
            "doc_id": doc_id,
            "score": round(score, 4),
            "snippet": snippet
        })

    return render_template("results.html", results=results, query=query)


if __name__ == "__main__":
    app.run(debug=True)
