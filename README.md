
# 🚀 AI Incident Assistant  
### _AI-powered multi-agent platform for incident analysis, log intelligence, and root-cause automation_

This repository contains a **full-stack production-grade AI system** that analyzes infrastructure incidents using **LLMs, multi-agent orchestration, RAG, vector search, and long‑term memory**.

Built with:

- **FastAPI (Backend)**
- **React + Vite + Tailwind (Frontend)**
- **ChromaDB (Vector Store)**
- **OpenAI GPT‑4o**
- **Custom Multi-Agent Orchestrator**
- **Long-term memory + per-incident RAG**

This project is structured and polished specifically for hackathon/demo scenarios.

---

# 🧠 Problem Statement

Modern infrastructure teams handle complex incidents daily:

- 502 / 504 errors  
- Slow queries  
- High CPU/memory  
- Deployment failures  
- DB connection pool issues  
- Latency spikes  

Manually scanning logs, correlating alerts, and writing resolution steps wastes time and slows recovery.

### ✔ Our Solution  
An **AI-powered incident assistant** that:

- Reads and interprets logs
- Detects patterns and anomalies
- Suggests **root cause**
- Generates **fix steps / runbooks**
- Visualizes **incident timeline**
- Uses **RAG + memory + multi-agents**
- Supports **per-incident knowledge ingestion**
- Tracks **LLM performance metrics**

---

# ✨ Features

## 🧩 1. Multi-Agent Architecture
The backend orchestrates **5 specialized agents**:

| Agent | Description |
|-------|-------------|
| **Log Analysis Agent** | Detects patterns, errors, anomalies in logs |
| **Root Cause Agent** | Gives likely root cause |
| **Runbook/Resolution Agent** | Suggests repair steps |
| **Timeline Agent** | Generates chronological event timeline |
| **Presenter Agent** | Creates final structured and readable response |

Agents collaborate to produce a single final answer.

---

## 📚 2. RAG (Retrieval Augmented Generation)

Uses **ChromaDB** for:

- Documentation uploads  
- Runbooks / SOPs  
- Troubleshooting guides  
- Uploaded logs (file-based)  
- Incident-specific logs  
- Long-term memory summaries  

The assistant retrieves the most relevant chunks during every query.

---

## 📝 3. Log Ingestion (Textarea + File Upload)

Supports:

- Pasting logs directly  
- Uploading `.log`, `.txt`, `.err`, `.out` files  
- Saving logs into incident-specific RAG  
- Reusing textarea logs for repeated analysis  

---

## 📘 4. Knowledge Base Upload

Upload your own:

- Nginx runbooks  
- Kubernetes troubleshooting docs  
- Internal playbooks  
- Investigation SOPs  

These documents are chunked and stored in vector DB.

---

## 🧠 5. Long-Term Memory

Every chat session is stored.  
Older messages are summarized and stored in long-term memory via Chroma.

---

## 🕒 6. Incident Timeline Generation

Timeline agent stitches chronological flow like:

```
t0: Nginx reported upstream timeout
t1: Backend latency reached 3.2s
t2: CPU at 88% on pod checkout-api-12
t3: Root cause detected: DB connection pool saturation
```

---

## 📊 7. LLM Performance Tracking (Metrics Dashboard)

Tracks:

- Model used  
- Number of calls  
- Latency (ms)  
- Prompt size  
- Completion size  
- Success/Error count  

Visible in the UI.

---

# 🏗️ Architecture Overview

```
ai-incident-assistant/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI routes
│   │   ├── agents/        # Multi-agent logic
│   │   ├── rag/           # RAG, chunking, retrieval
│   │   ├── core/          # LLM client, DB, config
│   │   ├── models/        # SQLAlchemy ORM
│   │   └── main.py        # App entrypoint
│   └── .env
│
├── frontend/
│   ├── src/               # React + Vite code
│   ├── public/
│   └── .env
│
└── README.md
```

---

# 🔐 Environment Setup

## Backend `.env`  
Create `backend/.env`:

```
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1
DATABASE_URL=sqlite+aiosqlite:///./incident.db
```

## Frontend `.env`  
Create `frontend/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
```

---

# ▶️ Running the Project

## 🟦 Backend

```bash
cd backend
python -m venv venv
venv/Scripts/activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open docs:  
👉 http://localhost:8000/docs

---

## 🟩 Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:  
👉 http://localhost:5173/

---

# 🧪 Demo Flow (Ideal for Hackathon Judges)

### 1. Create an Incident
Left menu → click **+ New**

Example:  
`"Nginx 502 in Checkout"`

---

### 2. Paste Logs or Upload Log Files

Paste:

```
2024-12-04T10:22:11Z [error] upstream timed out
2024-12-04T10:22:12Z [warn] upstream response time 3.2 sec
```

Or upload `error.log`.

Press: **Save textarea logs to incident RAG**

---

### 3. Ask Incident-Level Questions (Agent Mode)

Switch to:  
**Incident (Agents)**

Ask:

> “Analyze these logs and tell me the root cause.”

System returns:

- Log analysis  
- Root cause  
- Resolution plan  
- Timeline  

---

### 4. Upload Knowledge Base Docs

Upload internal docs like:

- `Nginx_502_Runbook.md`
- `DB_Performance_Checklist.pdf` (text-extracted)

Ask:

> “Apply our internal runbook to this incident.”

---

### 5. View LLM Metrics  
Right panel → **LLM Metrics**

Shows performance of all LLM calls.

---

# 📚 Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React, Vite, Tailwind |
| Backend | FastAPI, SQLAlchemy |
| Vector DB | ChromaDB |
| LLM | OpenAI GPT‑4o |
| DB | SQLite |
| Architecture | Multi-Agent + RAG + Memory |

---

# 📄 License  
Personal side project. No license attached.

---

# ❤️ Made for Hackathons  
Designed to impress with:

- Full-stack development  
- Multi-agent reasoning  
- RAG + memory  
- Realistic logs ingestion  
- Performance metrics dashboard  
- Enterprise-style UI  

---

# 📸 Screenshots (Add Later)

Place your screenshots under `/screenshots`:

- Dashboard view  
- Incident creation  
- Log uploads  
- Knowledge base uploads  
- Agent analysis output  
- Timeline view  
- Metrics dashboard  

