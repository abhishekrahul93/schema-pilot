# SchemaPilot 🚀

SchemaPilot is an intelligent, automated database schema management and documentation agent powered by FastAPI and modern AI tools. It helps developers and data engineers seamlessly design, validate, document, and query data schemas with AI assistance.

---

## 🌟 Key Features

* **AI-Powered Schema Assistant:** Automatically generate, optimize, and explain SQL schemas and models using integrated agent workflows (uto_coder_agent.py).
* **FastAPI Backend:** High-performance, asynchronous REST API serving backend operations.
* **Interactive Web UI:** Clean, responsive static frontend dashboard for real-time visualization and interaction.
* **Embedded Analytics & Storage:** Powered by DuckDB for lightweight, lightning-fast analytical processing.
* **Containerized Deployment:** Fully Dockerized with Render Blueprint support for instant cloud deployment.

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Database & Engine:** DuckDB, SQLAlchemy / Custom YAML Configs
* **AI Agent:** Custom Auto-Coder Agent workflow
* **Deployment:** Docker, Render (Infrastructure-as-Code via ender.yaml)

---

## 🚀 Getting Started Locally

### 1. Clone the Repository
\\\ash
git clone https://github.com/abhishekrahul93/schema-pilot.git
cd schema-pilot
\\\

### 2. Set Up a Virtual Environment
\\\ash
python -m venv venv
# On Windows:
.\venv\Scripts\Activate
# On macOS/Linux:
# source venv/bin/activate
\\\

### 3. Install Dependencies
\\\ash
pip install -r requirements.txt
\\\

### 4. Run the Application
\\\ash
python main.py
\\\
Open your browser and navigate to \http://localhost:8000\.

---

## 🌐 Live Demo
* **Live API & Dashboard:** [Access SchemaPilot Live on Render](https://your-render-app-url.onrender.com)

---

## 📦 Deployment
SchemaPilot is configured for automated deployment on **Render** via the included \ender.yaml\ Blueprint and \Dockerfile\. Simply link your GitHub repository to Render as a Blueprint to spin up the production server instantly.

---

## 📄 License
This project is open-source and available under the MIT License.
