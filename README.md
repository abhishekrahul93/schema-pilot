# SchemaPilot 🚀

A multi-agent SQL analytics and governance engine built with FastAPI, DuckDB, LangChain, and an automated LLM-judge evaluation pipeline.

## 📌 Overview
SchemaPilot bridges natural language processing with robust database governance. It allows users to query databases using natural language while ensuring syntax validity, security constraints, and structured evaluation testing via automated agents.

## 🛠️ Tech Stack
- **Backend**: FastAPI, Python 3.11, Uvicorn
- **Database & Query**: DuckDB, SQL
- **AI & Agents**: LangChain, OpenAI API
- **Evaluation Framework**: Custom TestClient runner with exact-match and LLM-judge scorers
- **CI/CD**: GitHub Actions

## 📂 Project Structure
```text
schema-pilot/
├── backend/               # Core backend services
├── evals/                 # Custom evaluation framework & test cases
│   ├── test_cases/        # JSON test suites (exact match & LLM judge)
│   └── run_evals.py       # Automated evaluation test runner
├── schema-pilot-clean/    # Clean FastAPI application implementation
└── .github/workflows/     # CI/CD pipelines
