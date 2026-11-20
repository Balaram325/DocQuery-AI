# ResearchPaper AI — RAG PDF Question Answering

An educational **Retrieval-Augmented Generation** project for research PDFs.

## Features
- Upload multiple searchable PDF files using Streamlit
- Extract page-aware text with pypdf, split into overlapping chunks
- Semantic retrieval using Sentence Transformers and ChromaDB (in-memory index)
- Optional grounded LLM answers using local Ollama or OpenAI API
- Show retrieved source filename, page number, and supporting text
- Retrieval-only fallback when no LLM is configured

## Run locally
Requires Python 3.10+.

```bash
git clone https://github.com/Balaram325/RAG_ALL_WORKS.git
cd RAG_ALL_WORKS
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The embedding model downloads on first run.

## Choose an LLM
**Ollama (local):** Install Ollama, run `ollama pull llama3.2`, ensure its server is running, then select **Ollama** in the app.

**OpenAI:** Copy `.env.example` to `.env`, set `OPENAI_API_KEY`, and select **OpenAI**. OpenAI API usage is billed separately from ChatGPT subscriptions.

**Retrieval only:** Works without an LLM API. Shows supporting passages, not a synthesized answer.

## Test
```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

## Notes
- Scanned/image-only PDFs are unsupported (no OCR).
- Uploaded document excerpts sent to OpenAI are processed by that external provider. Ollama can run locally.
- PDFs and secrets should not be committed; do not upload confidential documents.
- Retrieved pages are supporting passages, not independently verified facts.
- This is a **RAG prototype**, not a finished autonomous Agentic AI system.
- No benchmark accuracy, latency, or reliability claims are made without testing.

## Portfolio description
Python PDF RAG prototype using pypdf, Sentence Transformers, ChromaDB and Streamlit for page-aware semantic retrieval, with optional LLM answer generation and displayed source references.
