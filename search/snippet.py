# search/snippet.py
import re
from bs4 import BeautifulSoup
from indexer.tokenizer import tokenize

def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(" ")
    return " ".join(text.split())

def highlight(text, words):
    """
    Highlight matching words in snippet using <mark>.
    Case-insensitive.
    """
    for w in words:
        pattern = re.compile(re.escape(w), re.IGNORECASE)
        text = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
    return text

def generate_snippet(path, query, max_length=250):
    """
    Reads HTML -> extracts text -> finds a snippet around query words.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
    except FileNotFoundError:
        return "(Document missing)"

    text = extract_visible_text(html)
    if not text:
        return "(No preview available)"

    query_words = [w.lower() for w in tokenize(query, do_stem=False)]
    if not query_words:
        return text[:max_length] + "..."

    # Find first occurrence of any query term
    pos = -1
    for word in query_words:
        pos = text.lower().find(word)
        if pos != -1:
            break

    if pos == -1:
        snippet = text[:max_length]
    else:
        start = max(0, pos - max_length // 3)
        end = min(len(text), start + max_length)
        snippet = text[start:end]

    # highlight query words
    snippet = highlight(snippet, query_words)

    return snippet + "..."
