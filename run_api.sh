#!/bin/bash
set -e  # stop if any command fails

export ANTHROPIC_API_KEY=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   # put your key here
export PERSIST_DIR=RAGDataMite/RAG/ProcessedDocuments/chroma_db

if [ ! -d "$PERSIST_DIR" ]; then
    echo "Building vector DB..."
    python RAGDataMite/main.py --mode index --persist_dir "$PERSIST_DIR"
else
    echo "Vector DB already exists, skipping index step."
fi

echo "Starting API server on http://127.0.0.1:8000 ..."
uvicorn RAGDataMite.RAG.api:app --host 0.0.0.0 --port 8000