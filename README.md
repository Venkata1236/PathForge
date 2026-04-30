# PathForge 🧭

**Adaptive Learning Path Generator** — powered by LangGraph + FAISS + GPT-3.5-turbo

## Overview
PathForge interviews a learner about their current skills and target role,
then uses a 4-node LangGraph pipeline to assess skill gaps, retrieve relevant
courses via RAG, and generate a personalized week-by-week curriculum.

## Architecture
React (Vite + Tailwind) → FastAPI → LangGraph (4 nodes) → FAISS + GPT-3.5-turbo → PostgreSQL

## Pipeline
| Node | Job |
|---|---|
| AssessNode | Maps skills to proficiency levels |
| GapAnalysisNode | Prioritizes skill gaps 1-5 |
| PathGeneratorNode | FAISS retrieval per gap |
| ScheduleBuilderNode | Week-by-week schedule |

## Quick Start
`ash
cd backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # add your OPENAI_API_KEY
python -m app.rag.embedder
uvicorn app.main:app --reload --port 8000
`

## Live URLs
- Frontend: https://pathforge.vercel.app
- API Docs: https://pathforge-api.onrender.com/docs
