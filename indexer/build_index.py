# indexer/build_index.py
import os
import json
from collections import defaultdict, Counter
from bs4 import BeautifulSoup

from .tokenizer import tokenize
from .tfidf_vectorizer import TFIDFVectorizer

DATA_PAGES_DIR = os.path.join("data", "pages")
INDEX_FILE = os.path.join("data", "index.json")
TFIDF_MODEL_FILE = os.path.join("data", "tfidf_model.json")

def extract_text_from_html(html: str) -> str:
    """
    Extract visible text from HTML using BeautifulSoup.
    """
    soup = BeautifulSoup(html, "html.parser")
    # remove script and style elements
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    # collapse whitespace
    return " ".join(text.split())

def build_inverted_index(doc_texts: dict):
    """
    Build inverted index:
       term -> {doc_id: freq}
    and also produce doc_lengths (number of tokens) and doc_paths mapping.
    doc_texts: dict of doc_id -> raw_text
    """
    inverted = defaultdict(dict)
    doc_lengths = {}
    for doc_id, text in doc_texts.items():
        tokens = tokenize(text)
        doc_lengths[doc_id] = len(tokens)
        freqs = Counter(tokens)
        for term, freq in freqs.items():
            inverted[term][doc_id] = freq
    return inverted, doc_lengths

def build_index(pages_dir=DATA_PAGES_DIR, index_file=INDEX_FILE, tfidf_model_file=TFIDF_MODEL_FILE):
    """
    Main entrypoint to build index from HTML files saved in data/pages/.
    """
    # 1. read all html files
    doc_texts = {}
    doc_paths = {}
    files = sorted([f for f in os.listdir(pages_dir) if f.endswith(".html") or f.endswith(".htm")])
    if not files:
        print(f"No HTML files found in {pages_dir}. Place scraped pages there first.")
        return

    for fname in files:
        path = os.path.join(pages_dir, fname)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
        text = extract_text_from_html(html)
        doc_id = fname  # use filename as doc id
        doc_texts[doc_id] = text
        doc_paths[doc_id] = path

    # 2. build inverted index
    inverted_index, doc_lengths = build_inverted_index(doc_texts)

    # 3. build TF-IDF model
    documents_ordered = [doc_texts[d] for d in doc_texts.keys()]
    tfidf = TFIDFVectorizer(min_df=1, use_sublinear_tf=True)
    tfidf.fit(documents_ordered)

    # compute and store document vectors (sparse)
    doc_vectors = {}
    for doc_id, text in doc_texts.items():
        doc_vectors[doc_id] = tfidf.transform(text)

    # 4. prepare index payload and save
    index_payload = {
        "doc_paths": doc_paths,          # doc_id -> filepath
        "doc_lengths": doc_lengths,      # doc_id -> token count
        # inverted index: term -> {doc_id: freq}
        "inverted_index": {term: docs for term, docs in inverted_index.items()},
        # store document vectors directly (sparse)
        "doc_vectors": doc_vectors,
        "meta": {
            "num_docs": len(doc_texts),
        }
    }

    os.makedirs(os.path.dirname(index_file), exist_ok=True)
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_payload, f, indent=2)

    # save tfidf model separately
    tfidf.save(tfidf_model_file)

    print(f"Built index for {len(doc_texts)} documents.")
    print(f"Saved index -> {index_file}")
    print(f"Saved TF-IDF model -> {tfidf_model_file}")

if __name__ == "__main__":
    build_index()
