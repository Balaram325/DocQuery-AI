"""Evaluate retrieval hit-rate across chunk sizes with labelled PDF questions.

Input JSONL records: {"question":"...","source":"paper.pdf","page":2}.
Each record identifies a relevant source page, not a specific sentence.
A hit is a retrieved chunk from that source/page. Human-authored labels required.
No LLM API key needed. Dataset/model downloaded only on first run.
"""
import argparse
import json
from pathlib import Path
from rag_core import split_text, build_index, retrieve

def hit_metrics(results, labels, ks):
    if len(results) != len(labels) or not labels:
        raise ValueError("Need matching nonempty retrieval results and labels")
    scores = {}
    for k in ks:
        if k < 1:
            raise ValueError("k must be positive")
        hits = sum(any(hit["source"] == row["source"] and hit["page"] == row["page"]
                       for hit in ranked[:k])
                   for ranked, row in zip(results, labels))
        scores[f"hit_rate_at_{k}"] = hits / len(labels)
    return scores

def evaluate(data_dir, question_file, chunk_sizes, overlap=150, ks=(1, 4)):
    from pypdf import PdfReader
    from sentence_transformers import SentenceTransformer
    import hashlib
    path = Path(data_dir)
    labels = [json.loads(line) for line in Path(question_file).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not labels or any(not x.get("question") or not x.get("source") or not isinstance(x.get("page"), int) or x["page"] < 1 for x in labels):
        raise ValueError("Every labelled question must have question, source PDF filename, and 1-based page")
    pages = []
    for pdf in sorted(path.glob("*.pdf")):
        with pdf.open("rb") as stream:
            reader = PdfReader(stream)
            for number, page in enumerate(reader.pages, 1):
                pages.append((pdf.name, number, page.extract_text() or ""))
    if not pages:
        raise ValueError("No PDFs found")
    valid = {(s, p) for s, p, _ in pages}
    for x in labels:
        if (x["source"], x["page"]) not in valid:
            raise ValueError(f"Unknown labelled source/page: {x['source']} page {x['page']}")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    all_scores = {}
    for size in chunk_sizes:
        if overlap >= size:
            raise ValueError("overlap must be smaller than every chunk size")
        chunks = []
        for source, page, text in pages:
            for index, passage in enumerate(split_text(text, size=size, overlap=overlap)):
                identity = hashlib.sha256(f"{source}:{page}:{index}:{passage}".encode()).hexdigest()
                chunks.append({"id": identity, "text": passage, "source": source, "page": page})
        if not chunks:
            raise ValueError("PDFs contain no extractable text")
        collection = build_index(chunks, model)
        found = [retrieve(collection, model, x["question"], k=max(ks)) for x in labels]
        all_scores[str(size)] = {"chunks": len(chunks), **hit_metrics(found, labels, ks)}
    return {"question_count": len(labels), "label_type": "source PDF and 1-based page",
            "overlap_characters": overlap, "chunk_size_results": all_scores,
            "caution": "Page-level hit rate measures retrieval of a labelled page, not answer correctness or citation faithfulness."}

def main():
    parser = argparse.ArgumentParser(description="Offline labelled page hit-rate evaluation")
    parser.add_argument("--pdf-dir", required=True)
    parser.add_argument("--questions", required=True)
    parser.add_argument("--chunk-sizes", nargs="+", type=int, default=[600, 900, 1200])
    parser.add_argument("--overlap", type=int, default=150)
    parser.add_argument("--output", default="reports/retrieval_evaluation.json")
    args = parser.parse_args()
    result = evaluate(args.pdf_dir, args.questions, args.chunk_sizes, args.overlap)
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
