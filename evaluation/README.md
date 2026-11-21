# Retrieval evaluation

This project does not yet claim measured retrieval accuracy. To benchmark it responsibly:

1. Select one or more **searchable** research PDFs; place them locally in `evaluation/pdfs/` (ignored by Git).
2. Manually write **20–30 questions**, each with a verified source PDF name and **1-based page number**. Save as `evaluation/questions.jsonl` (ignored).
3. Every JSONL line should look like `{"question":"What is the main contribution?","source":"research.pdf","page":2}`.
4. Run:

```powershell
python evaluate_retrieval.py --pdf-dir evaluation/pdfs --questions evaluation/questions.jsonl --chunk-sizes 600 900 1200 --overlap 150
```

5. Report page-labelled **Hit Rate@1** and **Hit Rate@4** plus question count and chunk size. Compare settings with the same question set. Keep an evaluation dataset free from confidential files.

Page-level hit rate only verifies that a chunk from the labelled page was retrieved; it does not establish answer correctness, factual grounding or precision of individual chunks. Do not report a percentage in a CV until the evaluation was actually run on human-verified questions.
