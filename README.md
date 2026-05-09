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
- Keep the system simple, scalable, and explainable

---

## 🏗️ Pipeline

Upload → Validate → Extract → Chunk → Embed → Retrieve → Generate

---

## ⚙️ Tech Stack
<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Qdrant-FF5A5F?style=flat&logo=qdrant&logoColor=white" />
  <img src="https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB" />
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white" />
</p>

- **Backend:** FastAPI (Fully Asynchronous)
- **App State & Metadata:** PostgreSQL (via `asyncpg`)
- **Vector Search & Memory:** Qdrant
- **Frontend:** React + Tailwind (minimal)

---

## 📂 Structure

`backend/`
- `api/` → endpoints (the front door)
- `services/` → business logic (parsing, chunking, LLM generation)
- `db/` → data layer (PostgreSQL and Qdrant interactions)

`frontend/`
- minimal UI (upload + Q&A)

`docs/`
- notes & decisions

---

## 🔄 Current Progress

- [x] File upload & validation (MIME, extension, magic bytes)
- [x] Safe storage (UUID)
- [x] PDF text extraction (PyMuPDF)
- [x] Text cleaning & normalization (ligatures, hyphenation, noise removal)
- [x] Chunking
- [x] Embeddings + Qdrant (Migrated from FAISS for payload management)
- [x] Asynchronous database pooling (PostgreSQL)
- [x] Retrieval + generation with prompt injection armor
- [x] UI visualization

---

## 💡 Key Ideas

- **Built to learn:** The goal is to expose the retrieved chunks, cosine scores, and raw prompts so I can actually see what the LLM is looking at before it answers.
- **Zero LangChain or LlamaIndex:** I wanted to write the chunking, embedding, and retrieval logic from scratch to understand the actual mechanics, instead of hiding everything behind a magic `.run()` method.
- **One document per chat:** Keeping it strictly to one PDF per conversation keeps the context window clean and makes debugging the retrieval accuracy way easier.
- **Clean Database Split:** Postgres handles the standard state (dates, filenames, chat history) while Qdrant handles the AI memory (vectors and text payloads).

---

## 📌 Why this project

Most tutorials show how to _use_ RAG.

This project focuses on:
→ understanding how it works internally  
→ building it step by step
→ scaling it from a local script to a production-ready async architecture

---

Built as part of my journey into AI Engineering.