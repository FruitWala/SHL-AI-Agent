# SHL AI Assessment Recommendation Agent

## Overview

This project is an AI-powered recommendation system that helps recruiters find suitable SHL assessments based on job roles, experience level, and hiring requirements.

The application uses:

- FastAPI
- Google Gemini
- ChromaDB
- Sentence Transformers
- SHL Assessment Catalog

---

## Features

- Semantic search using embeddings
- Multi-turn conversation
- Session memory
- AI-powered recommendations
- SHL assessment retrieval
- REST API

---

## Project Structure

```
app/
    agents/
    api/
    retrieval/
    utils/
    memory.py

data/
chroma_db/

main.py
build_index.py
requirements.txt
```

---

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run:

```bash
uvicorn main:app --reload
```

---

## API

### Health

GET

```
/health
```

### Chat

POST

```
/chat
```

Example request:

```json
{
    "session_id": "demo",
    "message": "Java Backend Developer"
}
```

---

## Tech Stack

- FastAPI
- Google Gemini
- ChromaDB
- Sentence Transformers
- Python

---

## Author

Gaurav Kori