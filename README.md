![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
# 🔬 ResearchMind

### Autonomous Multi-Agent Deep Research System

ResearchMind is an AI-powered **Autonomous Multi-Agent Deep Research System** that transforms a single research query into a comprehensive, structured, and evidence-backed research report.

Unlike traditional AI chatbots that generate short responses, ResearchMind employs multiple specialized AI agents that collaborate to search, analyze, synthesize, and validate information from trusted web sources.

---

# 🚀 Features

- 🔍 Autonomous Web Research
- 🤖 Multi-Agent Architecture
- 📚 Comprehensive Research Reports
- 🌐 Real-Time Web Search
- 📄 Structured Report Generation
- 🧠 Local LLM using Ollama
- ⚡ Streamlit User Interface
- 📑 Source-backed Research
- 🔄 Modular & Scalable Architecture

---

# 🏗️ System Architecture

```
                    User Query
                         │
                         ▼
                  Search Agent
                         │
                         ▼
                  Reader Agent
                         │
                         ▼
              Knowledge Aggregator
                         │
                         ▼
                  Writer Agent
                         │
                         ▼
                  Critic Agent
                         │
                         ▼
          Comprehensive Research Report
```

---

# ⚙️ Technology Stack

## Frontend

- Streamlit

## Backend

- Python

## AI Framework

- LangChain
- LangGraph

## Large Language Model

- Ollama
- DeepSeek-R1 7B

## Web Search

- Tavily Search API

## Web Scraping

- BeautifulSoup
- Requests

## Other Libraries

- Python Dotenv
- Pandas
- Pydantic

---

# 📂 Project Structure

```text
ResearchMind/
│
├── __pycache__/            # Python cache files
├── .gitignore              # Git ignore rules
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
│
├── app.py                  # Streamlit frontend application
├── agents.py               # Multi-Agent AI logic
├── pipeline.py             # Agent workflow & execution pipeline
├── tools.py                # Search tools, scraping & utility functions
│
└── .env                    # Environment variables (Not included in Git)
```

# 🛠 Installation

## 1. Clone the repository

```bash
https://github.com/LivingWithPaaji/ResearchMind.git
```

---

## 2. Navigate to the project

```bash
cd ResearchMind
```

---

## 3. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Install Ollama

Download Ollama from

https://ollama.com/

---

## Pull the model

```bash
ollama pull cieloforge/deepseek-r1-7b-spec:latest
```

Verify

```bash
ollama list
```

---

## Start Ollama

```bash
ollama serve
```

---

# 🔑 Environment Variables

Create a `.env` file in the root directory.

Example

```env
TAVILY_API_KEY=YOUR_API_KEY
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will be available at

```
http://localhost:8501
```

---

# 🔄 Workflow

1. User enters a research topic.
2. Search Agent gathers trusted sources.
3. Reader Agent extracts important information.
4. Writer Agent generates a structured report.
5. Critic Agent reviews and improves the report.
6. Final research report is displayed.

---

# 📷 Screenshots

## Homepage

(Add screenshot)

---

## Multi-Agent Pipeline

(Add screenshot)

---

## Generated Report

(Add screenshot)

---

# 🌍 Future Scope

- PDF Export
- DOCX Export
- Research History
- Vector Database Integration
- RAG Support
- Multi-Language Research
- Voice Assistant
- Academic Citation Formats
- Cloud Deployment
- Research Collaboration

---

# 👨‍💻 Author

**Jaspreet Singh**

Computer Science & Engineering

---

# 📄 License

This project is intended for educational and research purposes.

---

# ⭐ If you like this project

Please consider giving it a ⭐ on GitHub!
