---
title: VentureSense AI
emoji: 🔮
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# VentureSense AI - Startup Idea Validation Platform

VentureSense AI is a comprehensive, AI-powered platform designed to stress-test and validate startup ideas through intelligent market analysis, competitor intelligence, multi-dimensional risk assessment, and strategic Go/No-Go advisory.

Built on a unified high-performance architecture, VentureSense AI combines a **FastAPI backend** running **LangGraph-orchestrated agents** with a premium **React + Tailwind frontend**.

---

## 🔮 Core Features

- **Multi-Agent Orchestration**: Powered by LangGraph, coordinating dedicated agents for market trends, competitor analysis, risk mitigation, and advisory.
- **Sanity Checks & Critical Advisory**: Built-in logical guards that identify and reject absurd, impossible, or satirical ideas, providing realistic Go/No-Go recommendations.
- **Web Search Integration**: Real-time competitor and market lookups using DuckDuckGo search.
- **Synthesized Intelligence**: The agents loop back to summarize search results, ensuring a cohesive venture thesis rather than raw search dumps.
- **Premium User Interface**: A responsive React SPA dashboard styled with a space theme, glassmorphic cards, color-coded verdict banners, and interactive tabs.
- **Free Serverless Inference**: Fully configured to run on free serverless models like `Qwen/Qwen2.5-7B-Instruct` on Hugging Face (no paid billing credits required).

---

## 🏗️ Architecture

```
├── main.py                     # FastAPI backend (serves static files and endpoints)
├── config.py                   # Configuration parameters and model settings
├── dist/                       # Compiled production React frontend assets
├── state/
│   └── agent_state.py          # Shared agent state definition (Annotated messages list)
├── graphs/
│   └── workflow.py             # LangGraph workflow builder and loop-back routing
├── nodes/                      # Reasoning agent nodes
│   ├── market_analyst.py       # Market analysis agent (Search enabled)
│   ├── competitor_analysis.py  # Competitor landscape agent (Search enabled)
│   ├── risk_assessor.py        # Risk evaluator agent (Search enabled)
│   └── advisor.py              # Strategic Go/No-Go advisor (Pydantic parsed outputs)
├── tools/
│   └── web_search_tool.py      # DuckDuckGo search integration with rate delay
└── prompts/                    # Agent-specific system instruction templates
    ├── market_analyst.txt
    ├── competitor_analyst_prompt.txt
    ├── risk_assessor.txt
    └── advisor.txt
```

---

## 🚀 Quick Start

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/Sushanth-1000/VentureSenseAI.git
cd VentureSenseAI
```

### 2. Configure API Key
Create a `.env` file in the root directory and add your free Hugging Face Access Token:
```env
HUGGINGFACEHUB_API_TOKEN=hf_yourHuggingFaceTokenHere
```

### 3. Launch the Application
Start the unified FastAPI server which serves both the API endpoints and the React frontend:
```bash
# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Start the application
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```

### 4. Open in Browser
Visit **`http://localhost:8000`** in your browser to start validating your startup ideas.

---

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
All rights reserved.