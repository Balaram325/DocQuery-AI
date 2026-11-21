"""Streamlit interface for research PDF retrieval and grounded Q&A."""
import os
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from rag_core import pdf_chunks, build_index, retrieve, make_context
from llm_client import answer

load_dotenv()
st.set_page_config(page_title="ResearchPaper AI", page_icon="📄", layout="wide")
st.title("📄 ResearchPaper AI")
st.caption("Upload research PDFs, search semantically, and optionally generate grounded answers.")
@st.cache_resource
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

with st.sidebar:
    st.header("Documents")
    files = st.file_uploader("Upload searchable PDFs", type=["pdf"], accept_multiple_files=True)
    # Public deployment defaults to retrieval-only to avoid exposing paid API usage.
    cloud_demo = os.getenv("RAG_PUBLIC_DEMO", "0") == "1"
    modes = ["Retrieval only"] if cloud_demo else ["OpenRouter", "Gemini", "Retrieval only", "Ollama"]
    provider = st.selectbox("Answer mode", modes, index=0 if cloud_demo else 0)
    if cloud_demo:
        st.caption("Public demo: semantic retrieval only. No LLM key is needed.")
    top_k = st.slider("Retrieved passages", 1, 8, 4)
    index_clicked = st.button("Index uploaded PDFs", type="primary")
    if provider == "OpenRouter" and not os.getenv("OPENROUTER_API_KEY"):
        st.warning("Set OPENROUTER_API_KEY in your local .env before using OpenRouter.")
    if provider == "Gemini" and not os.getenv("GEMINI_API_KEY"):
        st.warning("Set GEMINI_API_KEY in your local .env before using Gemini.")
    if provider == "Ollama":
        st.caption("Start Ollama locally and pull llama3.2 first.")

if index_clicked:
    if not files:
        st.warning("Choose one or more PDFs first.")
    else:
        chunks = []
        for uploaded in files:
            try:
                chunks.extend(pdf_chunks(uploaded.getvalue(), uploaded.name))
            except Exception as exc:
                st.error(f"Could not read {uploaded.name}: {exc}")
        if chunks:
            with st.spinner("Embedding and indexing text..."):
                try:
                    model = load_model()
                    collection = build_index(chunks, model)
                    st.session_state["collection"] = collection
                    st.session_state["chunk_count"] = len(chunks)
                    st.session_state["messages"] = []
                    st.success(f"Indexed {len(chunks)} chunks.")
                except Exception as exc:
                    st.error(f"Indexing failed: {exc}")
        else:
            st.error("No extractable text was found. Scanned PDFs require OCR, which is not included.")

if "collection" not in st.session_state:
    st.info("Upload searchable research PDFs and click 'Index uploaded PDFs' to begin.")
else:
    st.caption(f"Index contains {st.session_state.get('chunk_count', 0)} chunks. Upload changes require reindexing.")
    for msg in st.session_state.get("messages", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    question = st.chat_input("Ask about your uploaded papers")
    if question:
        st.chat_message("user").write(question)
        try:
            hits = retrieve(st.session_state["collection"], load_model(), question, top_k)
            if not hits:
                response = "No matching text found in the uploaded PDFs."
            elif provider == "Retrieval only":
                response = "Retrieval-only mode: see supporting passages below. Select an LLM provider to generate an answer."
            elif provider == "OpenRouter" and not os.getenv("OPENROUTER_API_KEY"):
                response = "OpenRouter API key not configured. Select Retrieval only or add OPENROUTER_API_KEY to .env."
            elif provider == "Gemini" and not os.getenv("GEMINI_API_KEY"):
                response = "Gemini API key not configured. Select Retrieval only or add GEMINI_API_KEY to .env."
            else:
                with st.spinner("Generating a grounded answer..."):
                    response = answer(question, make_context(hits), provider)
            with st.chat_message("assistant"):
                st.markdown(response)
                with st.expander("Retrieved sources"):
                    for i, hit in enumerate(hits, start=1):
                        st.markdown(f"**[{i}] {hit['source']} — page {hit['page']}**")
                        st.write(hit["text"])
            st.session_state.setdefault("messages", []).extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": response}])
        except Exception as exc:
            st.error(f"Question processing failed: {exc}")
