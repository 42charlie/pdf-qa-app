export const steps = [
  {
    id: "upload",
    title: "Document Ingestion",
    description:
      "PDF is uploaded and validated for supported formats before being assigned a unique UUID for tracking.",
  },
  {
    id: "document",
    title: "Metadata & Storage",
    description:
      "The system records file metadata, including the filename and total page count, while persisting the document record to the database.",
  },
  {
    id: "text",
    title: "Text Extraction & Cleaning",
    description:
      "Raw text is extracted from PDF pages and processed through a cleaning pipeline to remove noise and validate content quality.",
  },
  {
    id: "chunks",
    title: "Semantic Chunking",
    description:
      "Text is partitioned into manageable segments using a chunk size of 800 characters and an overlap of 120 characters to preserve context.",
  },
  {
    id: "question",
    title: "Query Embedding",
    description:
      "The user's question is converted into a high-dimensional vector representation to enable semantic similarity searching.",
  },
  {
    id: "retrieval",
    title: "Vector Similarity Search",
    description:
      "The system identifies the most relevant chunks by calculating distances in the vector space, filtering results based on a relevance threshold.",
  },
  {
    id: "answer",
    title: "Grounded Generation",
    description:
      "An LLM generates a JSON-formatted response strictly limited to the provided context, citing specific chunk IDs used for grounding.",
  },
];
