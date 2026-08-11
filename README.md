# AI Job Finder

A personal AI-powered job finder, candidate profiler, and intelligent job matching platform.

## Architecture

- **Backend**: Python 3.11, FastAPI, SQLAlchemy 2.0, Pydantic v2, PyPDF & python-docx for text extraction, Google Gemini / OpenAI structured parsing with fallback heuristic parsing.
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide icons.
- **Database**: PostgreSQL (via Docker Compose) with dynamic SQLite fallback for lightweight local dev.
- **Orchestration**: Docker & Docker Compose.

---

## Quick Start Guide

### Option 1: Running with Docker Compose (Recommended)

1. Clone or navigate to the repository:
   ```bash
   cd ai-job-finder
   ```

2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

3. (Optional) Set `GEMINI_API_KEY` or `OPENAI_API_KEY` in `.env` for AI resume parsing. If left blank, the built-in fallback heuristic parser will be used.

4. Start all services using Docker Compose:
   ```bash
   docker compose up --build
   ```

5. Access the applications:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Backend Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

### Option 2: Running Locally (Without Docker)

#### Backend Setup:

1. Navigate to `backend`:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch backend dev server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

#### Frontend Setup:

1. Open a new terminal and navigate to `frontend`:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Run frontend development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Running Unit & Integration Tests

Run backend tests using `pytest`:

```bash
cd backend
pytest -v
```

---

## Supported Features (Phase 1 & Phase 2)

- ✅ **PDF & DOCX Resume Upload**: Validates format, size, and safely stores original files.
- ✅ **Text Extraction**: Extracts clean text from single/multi-page PDFs and DOCX documents with table support.
- ✅ **LLM Candidate Parser**: Formats candidate profile into structured JSON (roles, experience, programming languages, frameworks, databases, tools, cloud, education, preferences).
- ✅ **Fallback Parsing Engine**: Pattern matching parser that operates even without external LLM keys.
- ✅ **Interactive Dashboard & Resume Viewer**: Real-time rendering of candidate profile tags, experience counters, and skill badges.
