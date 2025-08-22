# Stop if any command fails
$ErrorActionPreference = "Stop"

# Set environment variables
$env:ANTHROPIC_API_KEY = "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"   # put your key here
$env:PERSIST_DIR = "RAGDataMite/RAG/ProcessedDocuments/chroma_db"

# Check if persist dir exists
if (-Not (Test-Path $env:PERSIST_DIR)) {
    Write-Host "Building vector DB..."
    python RAGDataMite/main.py --mode index --persist_dir $env:PERSIST_DIR
} else {
    Write-Host "Vector DB already exists, skipping index step."
}

Write-Host "Starting API server on http://127.0.0.1:8000 ..."
uvicorn RAGDataMite.RAG.api:app --host 0.0.0.0 --port 8000
