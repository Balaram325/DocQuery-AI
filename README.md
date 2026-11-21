# DocQuery AI — Research PDF Question Answering

**DocQuery AI** is a Python/Streamlit research PDF assistant combining page-aware retrieval with **OpenRouter** answer generation (default), optional **Gemini** or local **Ollama**. No OpenAI key is required.

## Live demo deployment

The app has a retrieval-only public demo mode that needs no LLM API key. Follow [DEPLOYMENT.md](DEPLOYMENT.md) to publish it on Streamlit Community Cloud. The live URL will be added **after** the deployment is completed and checked. The app is **not yet confirmed publicly deployed**.

## Features
- Upload multiple searchable PDFs in Streamlit
- Extract page text with pypdf, split into overlapping chunks
- Embed with Sentence Transformers and search with ChromaDB
- Generate answers from retrieved passages with OpenRouter (default), Gemini or Ollama
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

Open the **local** `.env` and set `OPENROUTER_API_KEY=your_real_key`. Never paste your key into GitHub, public screenshots, issues or chat.

Start the app:

```powershell
streamlit run app.py
```

Upload a searchable PDF, click **Index uploaded PDFs**, choose **OpenRouter**, and ask a question. The embedding model downloads on first use.

## OpenRouter setup
Set `OPENROUTER_API_KEY` in your **local** `.env` file. The default `OPENROUTER_MODEL=openrouter/free` uses OpenRouter's free-model router and requires no OpenAI key. Free models are rate-limited and can vary by request; their availability and output quality may change. To pin a particular model, set `OPENROUTER_MODEL` to its exact model ID from https://openrouter.ai/models. Some models incur usage charges.

If you already extracted a ZIP rather than cloning with Git, download the updated ZIP and copy your private `.env` over locally. Do not commit it. To update an existing Git clone, run `git pull origin main`.

## Gemini model selection
The default `GEMINI_MODEL=gemini-2.5-flash` requires a Gemini API key with access to that model. Available model IDs and quotas vary by account and may change; if the API returns 404 or a quota/access error, check model availability in [Google AI Studio](https://aistudio.google.com/) and update `GEMINI_MODEL` in your local `.env`. Google Gemini requests send the retrieved PDF passages to Google's API; avoid sensitive PDFs.

## Other modes
- **Gemini:** provide `GEMINI_API_KEY` and choose an accessible `GEMINI_MODEL`.\n- **Retrieval only:** no API key needed; shows source passages without generated answers.
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
- Retrieved PDF passages are sent to the chosen external API provider (OpenRouter or Gemini); avoid sensitive documents.\n- This is an educational RAG prototype, not a validated deployed service or autonomous agent.
- Integration behavior, accuracy and latency should be verified locally before making portfolio claims.

## Portfolio summary
Python RAG PDF assistant with Streamlit, pypdf, Sentence Transformers, ChromaDB and optional OpenRouter or Gemini API generation; displays source pages for answer checking.

## Retrieval evaluation (labels required)

A new `evaluate_retrieval.py` script benchmarks page-labelled **Hit Rate@1** and **Hit Rate@4** across different chunk sizes (600, 900 and 1200 characters by default). See `evaluation/README.md` to prepare 20–30 manually verified question/source/page labels. No real retrieval accuracy is claimed until this human-labelled experiment is completed; passing unit tests is not an answer-quality metric.
