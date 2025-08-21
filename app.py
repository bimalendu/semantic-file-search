import os
import sqlite3
import streamlit as st
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import hashlib
import faiss

# --- Constants ---
EMBED_DIM = 384
MODEL_NAME = 'all-MiniLM-L6-v2'
DB_PATH = 'data/index.db'

# --- Init model & FAISS index ---
model = SentenceTransformer(MODEL_NAME)
faiss_index = faiss.IndexFlatL2(EMBED_DIM)

# --- DB Setup ---
os.makedirs("data", exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        name TEXT,
        size INTEGER,
        modified TEXT,
        hash TEXT,
        embedding BLOB
    )
''')
conn.commit()

# --- Helpers ---
def human_readable_size(size, decimal_places=2):
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024.0:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024.0

def get_file_info(path: Path):
    stat = path.stat()
    return {
        "path": str(path.resolve()),
        "name": path.name,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }

def hash_file(path: Path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def get_embedding(text: str):
    return model.encode([text])[0]

def serialize_embedding(embedding):
    return embedding.tobytes()

def deserialize_embedding(blob):
    return np.frombuffer(blob, dtype=np.float32)

def index_files(folder_paths):
    indexed = 0
    for folder in folder_paths:
        for path in Path(folder).rglob("*.*"):
            if not path.is_file():
                continue
            info = get_file_info(path)
            f_hash = hash_file(path)
            if not f_hash:
                continue
            # Check if already indexed
            c.execute("SELECT hash FROM files WHERE path=?", (info["path"],))
            row = c.fetchone()
            if row and row[0] == f_hash:
                continue  # Already indexed and unchanged
            # Embed and insert
            embedding = get_embedding(info["name"])
            c.execute('''
                INSERT OR REPLACE INTO files (path, name, size, modified, hash, embedding)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (info["path"], info["name"], info["size"], info["modified"], f_hash, serialize_embedding(embedding)))
            indexed += 1
    conn.commit()
    st.success(f"Indexed {indexed} new/updated files.")

def load_index_to_faiss():
    c.execute("SELECT embedding FROM files")
    rows = c.fetchall()
    vectors = [deserialize_embedding(row[0]) for row in rows]
    if vectors:
        faiss_index.add(np.array(vectors, dtype=np.float32))

def search_files(query, top_k=100):
    if faiss_index.ntotal == 0:
        return []
    q_vec = get_embedding(query).astype(np.float32).reshape(1, -1)
    D, I = faiss_index.search(q_vec, top_k)
    indices = I[0]
    placeholders = ','.join('?' * len(indices))
    c.execute(f"SELECT name, size, modified, path FROM files WHERE rowid IN ({placeholders})", list(indices))
    return c.fetchall()

def plot_wordcloud(words, title=""):
    if not words:
        st.info("No words to display in word cloud.")
        return
    text = " ".join(words)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# --- Streamlit App ---
st.set_page_config(page_title="Semantic File Search", layout="wide")
st.title("📁 Semantic File Search (with SQLite)")

# --- Sidebar ---
with st.sidebar:
    st.header("📂 Folder Paths")
    folder_input = st.text_area("Enter one folder path per line:")
    folders = [f.strip() for f in folder_input.splitlines() if f.strip()]
    if st.button("🔍 Index Files"):
        if folders:
            index_files(folders)
            load_index_to_faiss()
        else:
            st.error("Please enter folder paths.")

# --- Word Cloud of All Files ---
c.execute("SELECT name FROM files")
all_filenames = [row[0] for row in c.fetchall()]
if all_filenames:
    st.subheader("📊 Word Cloud of All Files")
    plot_wordcloud(all_filenames)

# --- Search ---
st.subheader("🔎 Semantic Search")
query = st.text_input("Search for files:")
if query:
    load_index_to_faiss()  # ensure loaded
    results = search_files(query)
    if results:
        st.subheader("📄 Results")
        load_count = st.session_state.get("load_count", 10)
        for file in results[:load_count]:
            name, size, modified, path = file
            st.write(f"**{name}** — {human_readable_size(size)} — Modified: {modified} — `{path}`")

        if load_count < len(results):
            if st.button("🔽 Load More"):
                st.session_state.load_count = load_count + 10

        st.subheader("☁️ Word Cloud of Search Results")
        plot_wordcloud([r[0] for r in results])
    else:
        st.info("No matching files found.")
