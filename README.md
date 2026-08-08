# SchemaPilot 🚀
### Autonomous DuckDB Schema Operations & Multi-Agent Validation Platform

Schema Pilot is an enterprise-grade, full-stack AI data analyst and schema operations platform. It bridges natural language user queries with structured analytical database environments, powered by FastAPI, DuckDB, LangChain, and OpenAI.

---

## 🌟 Key Features

* **Dynamic Analyst (Natural Language SQL Agent):** Translates plain-English business questions into syntactically correct DuckDB SQL queries, executes them live against data models, and returns computed analytical results.
* **Automated Metadata Extraction:** Automatically scans local database catalogs (`schemapilot.duckdb`) to generate structured YAML schema configuration contexts (`schema_config.yaml`).
* **Multi-Agent Collaborative Workflows:** Multi-agent pipelines designed for peer review, critique, and schema validation.
* **Audited Compliance Pipelines:** Generates strict compliance checks and audit trails for database schemas.
* **Self-Healing Migrations:** Automatically detects schema discrepancies and generates automated healing migration fixes.
* **Interactive Payload Console:** A built-in web dashboard console allowing developers and reviewers to test custom JSON parameters and natural-language endpoints live.

---

## 🏗️ Architecture & Tech Stack

* **Backend / API:** FastAPI, Uvicorn, Python
* **Database & Storage:** DuckDB (`schemapilot.duckdb`)
* **AI & Orchestration:** LangChain, OpenAI (`gpt-4o-mini`)
* **Metadata & Configuration:** YAML (`schema_config.yaml`)
* **Frontend:** Tailwind CSS, Phosphor Icons, Modern HTML5 / JavaScript Dashboard
* **Deployment:** Render (Live Production)

---

## 🚀 Live Demo & Access

* **Live Application:** [https://schema-pilot.onrender.com](https://schema-pilot.onrender.com)
* **API Documentation:** Accessible via FastAPI automatic docs (`/docs` or `/redoc`) on the live server.

---

## 🛠️ Local Installation & Setup

If you want to run Schema Pilot locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/abhishekrahul93/schema-pilot.git](https://github.com/abhishekrahul93/schema-pilot.git)
   cd schema-pilot
