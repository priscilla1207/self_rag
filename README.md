# self_evolving_rag

🚀 Self-Evolving RAG (Retrieval-Augmented Generation)
A production-ready, self-improving Retrieval-Augmented Generation (RAG) system that continuously learns from user queries, detects weak knowledge, generates synthetic data, and autonomously improves its own performance over time.
This project goes beyond traditional RAG by introducing feedback loops, learning cycles, auto-reprocessing, and knowledge expansion making the system adaptive instead of static.

✨ Key Features
📄 Document Processing
Upload and ingest PDFs and text documents
Automatic chunking, preprocessing, and embedding generation
Persistent document & chunk tracking with status monitoring
🔍 Advanced Retrieval
Hybrid retrieval (semantic + keyword)
Configurable similarity thresholds
Optional reranking for improved relevance
Confidence scoring for every response
🤖 Query Intelligence
Asynchronous query processing
Source-grounded responses with retrieved context
Query history, similarity search, and feedback collection
🧠 Self-Learning System
Detects low-confidence and failed queries
Triggers learning cycles automatically
Identifies weak chunks and knowledge gaps
Improves retrieval quality over time
🔁 Auto-Reprocessing
Batch and single-chunk reprocessing
Quality-based chunk identification
Scheduled and manual auto-reprocess workflows
📚 Knowledge Expansion
Analyzes failed and frequent queries
Suggests new topics for knowledge base growth
Supports proactive expansion instead of reactive fixes
🧪 Synthetic Q&A Generation
Auto-generate Q&A pairs from documents or topics
Quality evaluation for generated data
Improves recall and coverage for sparse topics
📊 Observability & Metrics
Ingestion metrics
Learning cycle insights
Autonomous system statistics
Vector store health checks

🏗️ System Architecture (High-Level)

User Query
   ↓
Query API
   ↓
Hybrid Retriever → Vector DB (Qdrant)
   ↓
Reranker (optional)
   ↓
LLM Response Generator
   ↓
Confidence Evaluation
   ↓
Feedback & Learning Cycle
   ↓
Auto-Reprocess / Synthetic QA / Knowledge Expansion

🛠️ Tech Stack
Backend
Python
FastAPI
SQLAlchemy
PostgreSQL
Uvicorn
AI / ML
Embeddings (LLM-based)
Retrieval-Augmented Generation (RAG)
Synthetic Q&A generation
Confidence scoring
Vector Store
Qdrant
Infra & Tooling
Async background workers
RESTful API (OpenAPI 3.1)
Modular, extensible architecture

📂 API Overview
Documents
Upload documents
Process pending documents
Track document and chunk status
Queries
Create and evaluate queries
Feedback and regeneration
Similar query detection
Learning
Run learning cycles
Inspect learning insights
Reprocessing
Batch and individual chunk reprocessing
Auto-reprocess weak chunks
Knowledge Expansion
Topic suggestion from failed queries
Expansion statistics
Synthetic Q&A
Generate Q&A pairs (global / document / topic)
Evaluate and sample generated data

🧪 Why This Project Matters
Most RAG systems are static they retrieve once and forget.
This system:
Learns from its failures
Repairs weak knowledge
Expands intelligently
Improves without manual retraining
It is designed to resemble how real-world AI systems evolve in production.
