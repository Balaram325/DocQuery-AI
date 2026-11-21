# ResearchPaper AI — RAG PDF Question Answering

A Python/Streamlit research PDF assistant combining page-aware retrieval with optional **Gemini** or local **Ollama** answer generation. No OpenAI key is required.

## Features
- Upload multiple searchable PDFs in Streamlit
- Extract page text with pypdf, split into overlapping chunks
- Embed with Sentence Transformers and search with ChromaDB
- Generate answers from retrieved passages with Gemini API (default) or Ollama
- Inspect source filename, page number and retrieved excerpts
- Retrieval-only mode, even without any LLM key

## Install on Windows (VS Code terminal)
Requires Python 3.10+.

```powershell
git clone https://github.com/Balaram325/RAG_ALL_WORKS.git
cd RAG_ALL_WORKS
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open the **local** `.env` and set `GEMINI_API_KEY=your_real_key`. Never paste your key into GitHub, public screenshots, issues or chat.

Start the app:

```powershell
streamlit run app.py
```

Upload a searchable PDF, click **Index uploaded PDFs**, choose **Gemini**, and ask a question. The embedding model downloads on first use.

## Gemini model selection
The default `GEMINI_MODEL=gemini-2.5-flash` requires a Gemini API key with access to that model. Available model IDs and quotas vary by account and may change; if the API returns 404 or a quota/access error, check model availability in [Google AI Studio](https://aistudio.google.com/) and update `GEMINI_MODEL` in your local `.env`. Google Gemini requests send the retrieved PDF passages to Google's API; avoid sensitive PDFs.

## Other modes
- **Retrieval only:** no API key needed; shows source passages without generated answers.
- **Ollama:** install Ollama, run `ollama pull llama3.2:1b`, keep its server running, select **Ollama**. No cloud API key needed.

## Test
```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## Limitations and safety
- Scanned/image-only PDFs require OCR, not included here.
- Citation markers refer to retrieved snippets, not independently verified truth; review their source pages.
- Do not commit `.env`, keys, confidential PDFs or local vector stores.
- This is an educational RAG prototype, not a validated deployed service or autonomous agent.
- Integration behavior, accuracy and latency should be verified locally before making portfolio claims.

## Portfolio summary
Python RAG PDF assistant with Streamlit, pypdf, Sentence Transformers, ChromaDB and optional Gemini API generation; displays source pages for answer checking.
