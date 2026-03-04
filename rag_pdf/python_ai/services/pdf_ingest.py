from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from utils.text_splitter import split_text

# HuggingFace sentence-transformers model (free, works locally)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Dictionary to hold FAISS indices per thread
VECTOR_STORES = {}

def ingest_pdf(pdf_bytes: bytes, thread_id: str, filename: str):
    reader = PdfReader(pdf_bytes)
    pages = [p.extract_text() for p in reader.pages]
    text = "\n".join(pages)

    chunks = split_text(text)

    # Compute embeddings manually
    chunk_embeddings = embedding_model.encode(chunks)
    dim = chunk_embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatL2(dim)
    index.add(chunk_embeddings.astype("float32"))

    # Store index and chunks
    VECTOR_STORES[thread_id] = {
        "index": index,
        "chunks": chunks,
        "embeddings": chunk_embeddings.astype("float32"),
    }

    return {
        "filename": filename,
        "documents": len(pages),
        "chunks": len(chunks),
    }

def get_vectorstore(thread_id: str):
    return VECTOR_STORES.get(thread_id)