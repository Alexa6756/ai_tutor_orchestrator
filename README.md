# 🧠 Autonomous AI Tutor Orchestrator

**AI Agent Engineer – Task 2**

---

## 🎯 Goal

Enable an **AI Tutor** to autonomously decide which educational tool to use, how to call it, and how to adapt results to the student’s learning style and emotional state.

This system acts as the **“brain”** of an AI Tutor — analyzing user intent, extracting parameters, validating tool schemas, and managing personalized learning sessions.

---

## 🧩 Problem & Objective

### Problem

Traditional AI tutors can chat, but they **don’t know how to use multiple tools** intelligently.
They need a core **orchestration layer** that decides *what to do* and *how to do it* automatically.

### Objectives

* Understand conversational **intent**
* Extract **parameters** from natural language
* Validate input using **JSON schemas**
* Manage **state, emotion, and personalization**
* Seamlessly **orchestrate multiple educational tools**

---

## 🏗️ System Architecture

### Core Modules

| Module                  | Description                                                |
| ----------------------- | ---------------------------------------------------------- |
| **Context Analyzer**    | Understands conversation intent and selects the right tool |
| **Parameter Extractor** | Extracts and builds validated payloads for tool APIs       |
| **Tool Orchestrator**   | Executes API calls to tool adapters                        |
| **State Manager**       | Tracks user profiles, emotion, and mastery level           |
| **Validation Engine**   | Ensures payloads meet JSON Schema requirements             |

### Workflow

```
User Chat
   ↓
Context Analyzer
   ↓
Parameter Extractor
   ↓
Validation Engine
   ↓
Tool Orchestrator
   ↓
Response to Tutor
```

---

## ⚙️ Implementation Highlights

* **Backend:** FastAPI (async framework)
* **Programming Language:** Python 3.10+
* **Tools Integrated:**

  * Note Maker
  * Flashcard Generator
  * Concept Explainer
* **Logic:** Hybrid rule-based + LLM-assisted parameter extraction
* **Personalization:** Adapts difficulty, tone, and teaching style based on user emotion & mastery level

### Key Implementation Files

| File                      | Purpose                                   |
| ------------------------- | ----------------------------------------- |
| `context_analysis.py`     | Detects tool intent                       |
| `parameter_extraction.py` | Extracts structured parameters            |
| `orchestrator.py`         | Orchestration workflow logic              |
| `state_manager.py`        | Handles user state and personalization    |
| `validation.py`           | Schema validation                         |
| `tool_orchestrator.py`    | Runs and coordinates tool calls           |
| `llm_helpers.py`          | Stub for LLM prompt generation            |
| `agents.py`               | Agent logic for executing tool operations |

---

## 📁 Project Structure

```
ai_tutor_orchestrator/
│
├── src/
│   ├── main.py                     # FastAPI app entry point
│   ├── orchestrator.py             # Core orchestration logic
│   ├── tool_orchestrator.py        # Tool coordination and routing
│   ├── context_analysis.py         # Intent detection and tool selection
│   ├── parameter_extraction.py     # Parameter extraction and mapping
│   ├── validation.py               # JSON schema validation
│   ├── state_manager.py            # In-memory session store
│   ├── state_postgres.py           # Postgres-based state manager
│   ├── llm_helpers.py              # Prompt and inference stubs
│   ├── agents.py                   # Tool agent logic
│   ├── db.py                       # Database handling (SQLite / Postgres)
│   ├── utils.py                    # Common helpers
│   │
│   ├── adapters/                   # Mock tool connectors
│   │   ├── mock_note_maker.py
│   │   ├── mock_flashcard.py
│   │   └── mock_concept_explainer.py
│   │
│   ├── schemas/                    # Tool schemas & payload templates
│   │   ├── note_maker_schema.json
│   │   ├── flashcard_schema.json
│   │   ├── concept_explainer_schema.json
│   │   ├── note_maker_payload.py
│   │   ├── flashcard_payload.py
│   │   └── concept_explainer_payload.py
│
├── tests/                          # Unit & integration tests
│   ├── test_orchestrator.py
│   ├── test_agents.py
│   └── test_db.py
│
├── .env                            # Environment variables
├── requirements.txt                 # Dependencies
└── test_mock_adapters.py            # mock adapters testing
```

---

## ⚙️ Setup & Run

### Prerequisites

* Python 3.10+
* (Optional) PostgreSQL if persistent sessions are needed

### Installation

```bash
cd ai_tutor_orchestrator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the app

```bash
uvicorn src.main:app --reload
```

### Access API docs

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Example Scenario

**User:**

> “I’m struggling with calculus derivatives and need some practice.”

**System Flow:**

1. Context Analyzer → detects *“practice problem”* intent
2. Tool selected → Flashcard/Quiz Generator
3. Extracted parameters:

   ```json
   {
     "topic": "derivatives",
     "subject": "calculus",
     "difficulty": "easy"
   }
   ```
4. Validation → schema verified
5. Tool Orchestrator → calls flashcard API
6. Returns 5 easy derivative practice questions

---

## 🧪 Run Tests

```bash
pytest -v
```

---

## 🧾 Result & Impact

✅ Autonomous multi-tool AI tutoring layer
✅ Personalized by emotion & mastery
✅ Easily scalable for 80+ educational tools
✅ Foundation for adaptive AI learning systems

---
