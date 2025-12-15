## One request lifecycle

### PDF upload flow

- User uploads PDF
- Backend receives file
- Text is extracted from PDF
- Text is split into chunks
- Chunks are embedded
- Embeddings stored in vector DB
- PDF and chunk metadata stored in relational DB

### Q&A flow

- User sends a question
- Backend fetches last N messages (History)
- Question is embedded
- Vector DB is queried for relevant chunks
- Prompt is constructed (system instructions, context, history, question)
- Prompt sent to LLM
- Response returned to user

## Entities

### User

- Created by: end user (signup)
- Owned by: self
- Deleted when: user requests account deletion
- Depends on: —
- Owns: Chats

---

### Chat

- Created by: user
- Owned by: User
- Deleted when: user deletes it or user is deleted
- Depends on: User
- Owns: Documents, Questions, Answers

---

### Document (PDF)

- Created by: user (uploaded inside a chat)
- Owned by: Chat
- Deleted when: chat is deleted
- Depends on: Chat
- Owns: Chunks

---

### Chunk

- Created by: system during document processing
- Owned by: Document
- Deleted when: document is deleted
- Depends on: Document

---

### Question

- Created by: user
- Owned by: Chat
- Deleted when: chat is deleted
- Depends on: Chat

---

### Answer

- Created by: system (LLM response)
- Owned by: Chat
- Deleted when: chat is deleted
- Depends on: Question / Chat

## API responsibilities

### User

- Register account
- Authenticate (login)
- Delete account

---

### Chat

- Create chat
- Retrieve chat
- List user chats
- Update chat title
- Delete chat

---

### Document (PDF)

- Upload PDF to a chat

---

### Chunk

- No public API (internal system entity)

---

### Questions & Answers

- Submit a question in a chat
- Generate and return an AI answer (synchronous)

## Route contracts

| Entity   | Responsibility | HTTP method | Route path     | Input                         | Output                  |
| -------- | -------------- | ----------- | -------------- | ----------------------------- | ----------------------- |
| User     | Register       | POST        | /auth/register | { email, password, username } | { token, user }         |
| User     | Login          | POST        | /auth/login    | { email, password }           | { token, user }         |
| User     | Delete account | DELETE      | /users/me      | —                             | success                 |
| Chat     | Get chat       | GET         | /chats/{id}    | —                             | { chat, pdf, messages } |
| Chat     | List chats     | GET         | /chats         | —                             | { chats[] }             |
| Chat     | Update title   | PATCH       | /chats/{id}    | { title }                     | { chat }                |
| Chat     | Delete chat    | DELETE      | /chats/{id}    | —                             | success                 |
| Document | Upload PDF     | POST        | /documents     | multipart { file, chat_id? }  | { chat, pdf }           |
| Q&A      | Ask question   | POST        | /questions     | { question, chat_id? }        | { chat, answer }        |
