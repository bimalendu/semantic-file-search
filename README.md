# 📁 Semantic File Search (with SQLite + FAISS)

This is a Streamlit application for semantic file name search across multiple folders using vector embeddings, FAISS, and persistent SQLite storage.
You can index file names from folders, search them semantically, and visualize file distribution using word clouds.

## 🚀 Features

- 🔍 Semantic Search — Search files by meaning using `sentence-transformers`
- 🗂️ Multi-folder Input — Enter multiple folder paths
- 🔁 Recursive File Indexing — Scans all subfolders
- 💾 SQLite Storage — Stores file metadata and embeddings
- ⚡ FAISS Integration — Fast vector similarity search
- 📊 Word Cloud Visualization
  - All indexed file names
  - Search results
- 📋 File Metadata Display
  - Filename
  - Human-readable file size
  - Date modified
  - Full path
- ➕ "Load More" Pagination


## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/semantic-file-search.git
cd semantic-file-search
````

### 2. Install Python Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, use:

```bash
pip install streamlit sentence-transformers faiss-cpu matplotlib wordcloud python-magic
```

---

## ▶️ Usage

Start the Streamlit app:

```bash
streamlit run app.py
```

### In the App:

1. Enter one or more folder paths in the sidebar, one per line
2. Click "Index Files" to scan and embed filenames
3. Enter a semantic search query (e.g. `project report`, `budget summary`)
4. View:

   * Search results with file metadata
   * Word cloud of all files
   * Word cloud of search results
   * Load more results dynamically

## 📦 File Structure

```
semantic-file-search/
├── app.py              # Main Streamlit application
├── data/
│   └── index.db        # SQLite database for files and embeddings
├── requirements.txt    # Python package requirements
└── README.md           # Project documentation
```

## 📄 Example Output

### 🔍 Query: `"project budget"`

```
📄 budget_report_2023.xlsx — 45.2 KB — Modified: 2023-11-01 — /users/you/docs/finance/
📄 Q4_financials.pdf — 112 KB — Modified: 2023-10-30 — /users/you/reports/
```

### ☁️ Word Cloud:

* Visualizes common words in file names
* Helps identify themes in directories or search results

---

## 💡 Future Improvements

* 🧾 Full-text indexing (TXT, PDF, DOCX)
* 🔄 Auto-refresh index on file changes
* 📂 File type filtering
* ☁️ Deploy to Streamlit Community Cloud or Hugging Face Spaces
* 💾 Save/load FAISS index for persistence

---

## 🧾 Requirements

You can paste this into `requirements.txt`:

```
streamlit
sentence-transformers
faiss-cpu
matplotlib
wordcloud
python-magic
```

To install:

```bash
pip install -r requirements.txt
```

---

## 🛡️ License

This project is licensed under the **GPL3 License**. Feel free to use, modify, and distribute it.

---

## 🙋 Author

Built with ❤️ by [Bimal](https://github.com/bimalendu)
