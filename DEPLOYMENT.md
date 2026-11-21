# Deploy DocQuery AI on Streamlit Community Cloud

The app is ready for a **retrieval-only public demo**. Visitors can upload searchable research PDFs, index them and inspect the passages retrieved for a question. This demonstration does not need an OpenAI, OpenRouter or Gemini key. API-backed answers can still be used locally.

## Deploy from GitHub

1. Sign in to https://share.streamlit.io/ and connect your GitHub account.
2. Create a new app from `Balaram325/DocQuery-AI`, branch `main`, entry point `app.py`.
3. In the app's **Advanced settings → Secrets** enter only:

```toml
RAG_PUBLIC_DEMO = "1"
```

4. Choose the app subdomain `docquery-ai-rag` if available, or use the existing deployed app at https://docquery-ai-rag.streamlit.app/ . Click **Deploy**. After deployment, open the actual `*.streamlit.app` URL and test with a small, non-confidential searchable PDF.
5. Save that exact working URL in this repository's README and your CV. **Don't invent the URL before deployment.**

**Important:** The app reads `RAG_PUBLIC_DEMO` from Streamlit Secrets when no environment variable is configured. Do not put provider API keys in a public demo unless you have server-side rate limiting, quotas and abuse controls.

## Privacy and limitations

- Use only PDFs that you have permission to upload to the host.
- The public demo does not promise document storage guarantees, tenant isolation or production-grade access control.
- Sentence Transformers model files download on first start and may take time.
- The free deployment may sleep, have resource limits, or fail to install large ML dependencies; check build logs.
- `RAG_PUBLIC_DEMO` is a deployment convenience, not a security boundary; don't attach a billable provider key to a public unauthenticated prototype.
