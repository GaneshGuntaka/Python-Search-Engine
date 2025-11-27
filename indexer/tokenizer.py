# indexer/tokenizer.py
import re
import nltk

# try to download resources if missing
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

# Precompile regex to remove non-alphanumeric characters (keep apostrophes optionally)
_NON_ALNUM = re.compile(r"[^a-z0-9']+")

_STEMMER = SnowballStemmer("english")
_STOPWORDS = set(stopwords.words("english"))

def normalize(text: str) -> str:
    """Lowercase and strip unwanted characters."""
    text = text.lower()
    # replace non-alphanumeric with spaces
    text = _NON_ALNUM.sub(" ", text)
    return text

def tokenize(text: str, do_stem: bool = True, remove_stopwords: bool = True) -> list:
    """
    Tokenize the input text into a list of normalized tokens.
    
    Args:
        text: raw text
        do_stem: whether to apply stemming
        remove_stopwords: whether to remove stopwords

    Returns:
        list of tokens (strings)
    """
    if not text:
        return []

    text = normalize(text)
    tokens = word_tokenize(text)
    # filter out tokens that are pure numbers or single-character (optional)
    tokens = [t for t in tokens if len(t) > 1 and not t.isdigit()]

    if remove_stopwords:
        tokens = [t for t in tokens if t not in _STOPWORDS]

    if do_stem:
        tokens = [_STEMMER.stem(t) for t in tokens]

    return tokens
