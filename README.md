# Medical Domain Assistant — RAG-Powered Health Information System

A full-stack **Medical Assistant** built using **Retrieval-Augmented Generation (RAG)**. This application allows users to upload medical documents and receive precise, context-aware answers by combining **FastAPI**, **LangChain**, and **Streamlit**.

---

## System Architecture

The application implements a modular RAG pipeline to ensure medical accuracy and data grounding:

1. **Document Ingestion**: Extracts text from medical PDFs using PyMuPDF.
2. **Semantic Chunking**: Breaks text into manageable pieces using RecursiveCharacterTextSplitter.
3. **Vector Embedding**: Generates high-dimensional embeddings via Google gemini-embedding-001.
4. **Vector Storage**: Indexes and stores embeddings in Pinecone DB for low-latency retrieval.
5. **Contextual Retrieval**: Identifies relevant medical segments based on the user's query.
6. **LLM Generation**: Processes the retrieved context through Groq (gpt-oss-120b) to produce factual responses.


---

## Features

* **Intelligent Q&A**: Answers are grounded strictly in the uploaded documents to prevent hallucinations.
* **Real-time Processing**: Fast response times using Groq's high-speed inference.

---

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **LLM** | Groq (openai/gpt-oss-120b) |
| **Embeddings** | Google Generative AI (gemini-embedding-001) |
| **Vector Database** | Pinecone |
| **Orchestration** | LangChain |
| **Backend** | FastAPI |
| **Frontend** | Streamlit |

---

## API Endpoints

### POST /upload_pdfs/
Processes and embeds PDF files into the vector database.

### POST /ask_question/
Retrieves context and generates an answer for a medical query.

---

## Folder Structure
└── 📁assets
    ├── DIABETES.pdf
└── 📁client
    └── 📁components
        ├── chatUI.py
        ├── history_download.py
        ├── upload.py
    └── 📁utils
        ├── api.py
    ├── app.py
    ├── config.py
    └── requirements.txt
└── 📁server
    └── 📁middlewares
        ├── exception_handlers.py
    └── 📁modules
        ├── llm.py
        ├── load_vectorstore.py
        ├── pdf_handlers.py
        ├── query_handlers.py
    └── 📁routes
        ├── ask_question.py
        ├── upload_pdfs.py
    └── 📁uploaded_docs
        ├── DIABETES.pdf
        ├── Supratim Nag - LOR.pdf
    ├── .env
    ├── logger.py
    ├── main.py
    ├── requirements.txt
    └── test.py

---

## Quick Setup
```bash
# Clone the repo
$ git clone https://github.com/roshankumbhar/medicalAssistant.git
$ cd medicalAssistant/server

# Create virtual env
$ uv venv
$ .venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
$ uv pip install -r requirements.txt

# Set environment variables (.env)
GOOGLE_API_KEY=...
GROQ_API_KEY=...
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=...
PINECONE_ENV=...

# Run the server
$ uvicorn main:app --reload --port 8000


$ cd medicalAssistant/client

# Create virtual env
$ uv venv
$ .venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
$ uv pip install -r requirements.txt

# Run the server
$ streamlit run app.py
```

---

## Deployment

Backend Hosted on Render
Frontend Hosted on Streamlit Cloud
