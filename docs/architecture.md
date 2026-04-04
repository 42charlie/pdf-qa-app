# Architecture

## Overview

This project is a minimal RAG pipeline for PDF Q&A.

The goal is to understand the full flow of a document-based AI system, from file upload to answer generation, while keeping the architecture simple and modular.

---

## Pipeline

Upload → Validate → Store → Extract → Clean → Chunk → Embed → Retrieve → Generate

---

## Flow

### 1. Upload

The user uploads a PDF through the backend API.

### 2. Validate

The file is checked using:

- MIME type
- extension
- magic bytes
- size limits

Only valid PDFs are accepted.

### 3. Store

The uploaded file is stored safely using a UUID-based filename.

### 4. Extract

Text is extracted from the PDF using PyMuPDF.

### 5. Clean

The extracted text is normalized before further processing:

- fix ligatures
- fix broken hyphenation
- remove obvious noise lines
- normalize whitespace

### 6. Chunk

The cleaned text is split into smaller pieces for retrieval.

### 7. Embed

Each chunk is converted into an embedding vector.

### 8. Retrieve

When the user asks a question:

- the question is embedded
- similar chunks are searched in FAISS
- top relevant chunks are returned

### 9. Generate

The retrieved chunks are added to a prompt, and the LLM generates the final answer.

---

## Main Components

### Backend

Handles:

- upload endpoint
- validation
- extraction
- cleaning
- chunking
- retrieval
- answer generation

### SQLite

Stores:

- document metadata
- extracted text
- chunk metadata

SQLite is the source of truth.

### FAISS

Stores embedding vectors for similarity search.

FAISS is used only for retrieval, not as the main database.

### Frontend

A minimal interface for:

- uploading PDFs
- asking questions
- viewing answers and sources

---

## Current Direction

The project is being built step by step:

1. file handling
2. text extraction
3. cleaning
4. chunking
5. embeddings
6. retrieval
7. generation
8. UI visualization

Each stage is completed before moving to the next.
