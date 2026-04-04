# 🧠 Mini RAG Pipeline — PDF Q&A

## 🚀 Overview

This project is a **minimal Retrieval-Augmented Generation (RAG) system** built to understand how document-based AI systems work internally.

Instead of building a feature-heavy product, the focus is on a **clean, modular pipeline** from document upload to answer generation.

---

## 🎯 Goal

- Build a clear end-to-end RAG pipeline
- Focus on understanding core concepts:
  - text extraction
  - chunking
  - embeddings
  - retrieval
  - generation
- Keep the system simple, local, and explainable

---

## 🏗️ Pipeline

Upload → Validate → Extract → Chunk → Embed → Retrieve → Generate

---

## ⚙️ Tech Stack

- Backend: FastAPI
- Database: SQLite
- Vector Search: FAISS
- Frontend: React + Tailwind (minimal)

---

## 📂 Structure

backend/

- api → endpoints
- services → logic (parsing, chunking, retrieval)
- db → SQLite

frontend/

- minimal UI (upload + Q&A)

docs/

- notes & decisions

---

## 🔄 Current Progress

- [x] File upload & validation (MIME, extension, magic bytes)
- [x] Safe storage (UUID)
- [x] PDF text extraction (PyMuPDF)
- [x] Text cleaning & normalization (ligatures, hyphenation, noise removal)
- [ ] Chunking
- [ ] Embeddings + FAISS
- [ ] Retrieval + generation
- [ ] UI visualization

---

## 💡 Key Ideas

- Local-first system
- One document per chat (simplifies retrieval)
- SQLite = source of truth
- FAISS = fast vector search
- Focus on understanding, not complexity

---

## 📌 Why this project

Most tutorials show how to _use_ RAG.

This project focuses on:
→ understanding how it works internally  
→ building it step by step

---

Built as part of my journey into AI Engineering.
