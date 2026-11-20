"""PDF text extraction, chunking, semantic indexing, and retrieval."""
from io import BytesIO
import hashlib
from pypdf import PdfReader

def split_text(text: str, size: int = 900, overlap: int = 150) -> list[str]:
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("size must be positive and overlap smaller than size")
    text = " ".join(text.split())
    if not text:
        return []
    parts = []
    for start in range(0, len(text), size - overlap):
        parts.append(text[start:start + size])
        if start + size >= len(text):
            break
    return parts

def pdf_chunks(data: bytes, filename: str) -> list[dict]:
    reader = PdfReader(BytesIO(data))
    chunks = []
    for page_no, page in enumerate(reader.pages, start=1):
        for idx, content in enumerate(split_text(page.extract_text() or "")):
            chunks.append({"id": hashlib.sha256(f"{filename}:{page_no}:{idx}:{content}".encode()).hexdigest(),
                           "text": content, "source": filename, "page": page_no})
    return chunks

def build_index(chunks: list[dict], embedding_model):
    import chromadb
    db = chromadb.EphemeralClient()
    collection = db.create_collection("research_papers_" + hashlib.sha1("".join(c["id"] for c in chunks).encode()).hexdigest()[:16])
    vectors = embedding_model.encode([c["text"] for c in chunks], normalize_embeddings=True).tolist()
    collection.add(ids=[c["id"] for c in chunks], documents=[c["text"] for c in chunks],
                   metadatas=[{"source": c["source"], "page": c["page"]} for c in chunks], embeddings=vectors)
    return collection

def retrieve(collection, embedding_model, question: str, k: int = 4):
    vector = embedding_model.encode([question], normalize_embeddings=True).tolist()[0]
    result = collection.query(query_embeddings=[vector], n_results=min(k, collection.count()),
                              include=["documents", "metadatas", "distances"])
    return [{"text": t, "source": m["source"], "page": m["page"], "distance": d}
            for t, m, d in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])]

def make_context(matches: list[dict]) -> str:
    return "\n\n".join(f"[{i}] {m['source']} page {m['page']}\n{m['text']}" for i, m in enumerate(matches, 1))
