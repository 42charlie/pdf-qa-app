## Data Ownership Hierarchy

The system is built around clear parent–child ownership.  
Every entity has exactly one owner, and nothing lives without its parent.

```
User
 └── Chat
      ├── Document
      │    └── Chunk
      └── Question
           └── Answer
```

## Stable vs Derived Data

Some data is the source of truth and must be consistent at all times.  
Other data is derived, can be regenerated, and is treated as disposable.

| Entity   | Stable / Truth DB | Derived / Ephemeral DB |
| -------- | ----------------- | ---------------------- |
| User     | ✔️                |                        |
| Chat     | ✔️                |                        |
| Document | ✔️                |                        |
| Chunk    |                   | ✔️                     |
| Question | ✔️                |                        |
| Answer   |                   | ✔️                     |

PostgreSQL is the authoritative source of truth.  
The vector database only stores derived data used for semantic retrieval.

## Map Actions to DB Responsibility

Each API action clearly maps to a primary entity and a primary database.
Some actions trigger side effects such as cascaded deletes or vector updates.

| Route Path     | HTTP Method | Action / Responsibility | Primary Entity | Primary DB | Cascade / Side Effects                                                 |
| -------------- | ----------- | ----------------------- | -------------- | ---------- | ---------------------------------------------------------------------- |
| /auth/register | POST        | Register user           | User           | Postgres   | —                                                                      |
| /auth/login    | POST        | Authenticate user       | User           | Postgres   | —                                                                      |
| /users/me      | DELETE      | Delete user account     | User           | Postgres   | Deletes all chats → documents → chunks → questions → answers → vectors |
| /chats/{id}    | GET         | Retrieve chat           | Chat           | Postgres   | Includes document + messages                                           |
| /chats         | GET         | List user chats         | Chat           | Postgres   | —                                                                      |
| /chats/{id}    | PATCH       | Update chat title       | Chat           | Postgres   | —                                                                      |
| /chats/{id}    | DELETE      | Delete chat             | Chat           | Postgres   | Deletes document, chunks, questions, answers, vectors                  |
| /documents     | POST        | Upload PDF              | Document       | Postgres   | Creates chunks + vectors                                               |
| /questions     | POST        | Ask question            | Question       | Postgres   | Reads vectors, creates answer                                          |

## Define Vector DB Payload Contract

The vector database is used only for semantic search.
It is not authoritative and can always be rebuilt from PostgreSQL.

Collection: `document_chunks`

Each vector represents **one document chunk** and includes the following payload metadata:

- `chunk_id`  
  Links the vector to the relational chunk record

- `document_id`  
  Used for document-level deletion

- `chat_id`  
  Ensures retrieval is scoped to a single chat

- `user_id`  
  Enforces ownership and prevents cross-user access

- `chunk_index`  
  Preserves the original document order

## Plan Deletion Flows

Deletion always starts from a stable entity in PostgreSQL.
Vector DB data is deleted only as a consequence of relational lifecycle events.

```
User deletion:
 → deletes all Chats
      → deletes all Documents
           → deletes all Chunks (Vector DB)
      → deletes all Questions
           → deletes all Answers
```

## Step 6 — Query Patterns & Performance Assumptions

We identify common query patterns early so the system stays clear and easy to reason about.

Expected common queries:

- List all chats for a user  
  → filtered by `user_id`

- Retrieve a single chat  
  → chat + document + last N questions/answers

- Ask a question  
  → vector search filtered by `chat_id` (and `user_id` if needed)

- Delete a chat or document  
  → cascade in Postgres + filtered deletion in Vector DB
