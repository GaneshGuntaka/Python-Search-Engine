**Python Search Engine**
A mini search engine built using Python, Flask, TF-IDF, and inverted indexing.

🚀 **Features**

- Custom web crawler

- Text tokenizer with stopwords + stemming

- Inverted index generator

- TF-IDF ranking

- Snippet generation with highlighted query terms

- Web UI using Flask

- Google-like search interface

📁 **Project Structure**
PythonSearchEngine/
│
├── crawler/
│   ├── crawler.py
│   ├── downloader.py
│   └── url_manager.py
│
├── indexer/
│   ├── build_index.py
│   ├── tfidf_vectorizer.py
│   └── tokenizer.py
│
├── search/
│   ├── query_processor.py
│   ├── ranker.py
│   └── snippet.py
│
├── web/
│   ├── app.py
│   └── templates/
│       └── search.html
│
├── data/
│   ├── pages/
│   │   ├── page1.txt
│   │   ├── page2.html
│   │   ├── python_tutorial.txt
│   │   ├── ai_history.html
│   │   ├── website_homepage.txt
│   │   ├── blog_article1.txt
│   │   └── anything_you_crawled.txt
│   └── index.json
│
├── main.py
├── README.md
└── requirements.txt

▶ **How to Run**

**Install dependencies:**
pip install -r requirements.txt

**Build the index and start the server:**
python main.py

**Open your browser:**
http://127.0.0.1:5000/

🧠 **How It Works**

1. **Crawler**
Downloads webpages and saves them inside data/pages/.

2. **Indexer**
Reads all pages → tokenizes text → builds an inverted index → saves as data/index.json.

3. **Search Engine**
Processes user queries → computes TF-IDF scores → returns top results with snippets and highlighted keywords.

🎯 **Future Upgrades**

- Implement BM25 ranking for better relevance

- Multi-threaded crawling for faster indexing

- Caching frequently searched queries

- Auto-suggestions and search completion.