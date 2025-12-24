# Architecture & Pre-Coding Design

> “Give me six hours to chop down a tree and I will spend the first four sharpening the axe.”
> ~ Abraham Lincoln

This folder documents the **architecture thinking and design decisions** behind the project.

Instead of jumping straight into implementation, time was spent defining how the system works at a structural level. The documents here explain the _what_, the _why_, and the _how_ — from request lifecycles to data ownership and data storage — so implementation decisions are grounded in a clear and shared understanding.

---

## Why this exists

Most projects rush into coding and pay the price later with unclear responsibilities and painful refactors.

This folder exists to capture the reasoning behind key decisions, such as:

- How a PDF flows from upload to vector embeddings
- How chats, documents, and questions relate to each other
- What data is considered source of truth versus derived
- Which parts of the system are public API concerns and which remain internal

Having this written down makes the system easier to reason about, maintain, and extend.

---

## Core Design Principles

- **Backend drives complexity**  
  The frontend only expresses intent; the backend owns validation, lifecycle, and orchestration logic (for example, chat creation can be implicit).

- **Data-first design**  
  Data ownership and relationships come first. API endpoints and handlers are derived from these constraints.

- **Internal by default**  
  Low-level implementation details such as chunks and embeddings are internal system concerns and are never exposed through the public API.

- **Derived data is disposable**  
  Vector data and other derived artifacts can always be rebuilt from the relational source of truth.

---

## Project Roadmap & Status

The project follows a design-first approach before moving into implementation.

| Phase                 | Component                        | Status      |
| --------------------- | -------------------------------- | ----------- |
| **Conceptual Design** | Request Lifecycle (PDF & Q&A)    | ✅ **Done** |
| **Conceptual Design** | Entity Relationships & Ownership | ✅ **Done** |
| **Conceptual Design** | API Responsibilities & Contracts | ✅ **Done** |
| **Schema Design**     | Database Schema (PostgreSQL)     | ✅ **Done** |
| **Schema Design**     | Vector DB Structure (Qdrant)     | ✅ **Done** |
| **Build**             | Backend Implementation           | ⏳ **Next** |

> For a detailed breakdown of the architecture decisions and design steps:
- **[conceptual_design.md](./conceptual_design.md)**.
- **[schema_design.md](./schema_design.md)**.
