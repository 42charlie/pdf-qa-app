# Architecture & Pre-Coding Design

This folder documents the **thinking process** before the coding process.

Instead of jumping straight into implementation, we paused to define exactly how the system works. This blueprint covers the "what" and the "how" from request lifecycles to data ownership ensuring the backend architecture is solid before writing a single line of code.

## Why this exists

Most projects skip this step, but clarity here prevents messy refactors later. Before opening the IDE, we answered the hard questions:

- How exactly does a PDF go from upload to vector embeddings?
- Who owns a "Chat" vs. a "Document"?
- Which APIs are public and which remain internal?

## Core Design Principles

- **Backend drives complexity:** The frontend simply expresses intent; the backend handles the logic (e.g., chat creation is implicit).
- **Data-first design:** API endpoints are derived from entity relationships, not the other way around.
- **Internal by default:** Technical details like text chunks have no public API; they are internal system concerns.

## Project Roadmap & Status

We are currently moving from the **Conceptual Design** phase into **Implementation**.

| Phase                 | Component                        | Status         |
| :-------------------- | :------------------------------- | :------------- |
| **Conceptual Design** | Request Lifecycle (PDF & Q&A)    | ✅ **Done**    |
| **Conceptual Design** | Entity Relationships & Ownership | ✅ **Done**    |
| **Conceptual Design** | API Responsibilities & Contracts | ✅ **Done**    |
| **Schema Design**     | Database Schema (PostgreSQL)     | 📅 **Planned** |
| **Schema Design**     | Vector DB Structure (Qdrant)     | 📅 **Planned** |
| **Build**             | Backend Implementation           | 📅 **Planned** |

> Check the **[architecture notes](./architecture-notes.md)** in this folder for the detailed breakdown of the completed Conceptual Design phase.
