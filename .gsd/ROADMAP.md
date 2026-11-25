---
milestone: v1.0
version: 0.1.0
updated: 2026-11-25
---

# Roadmap

> **Current Phase:** 1 - Search & Extraction Pipeline
> **Status:** planning

## Must-Haves (from SPEC)

- [ ] Search Agent querying Tavily API and extracting candidate URLs
- [ ] Reader Agent scraping and cleaning web text using BeautifulSoup
- [ ] Writer Chain generating structured Markdown reports via LangChain (Gemini / Mistral)
- [ ] Critic Chain evaluating report quality with structured critique and score
- [ ] FastAPI backend with REST endpoints and SSE real-time streaming
- [ ] Streamlit interface for interactive agent execution, testing, and report review (React deferred to v2)

---

## Project Architecture Steps (Curriculum Blueprint)

- **Step 1: Project Setup & Dependencies** (Completed ✅)
  - Virtual environment `.venv`
  - `requirements.txt` with LangChain, Gemini, Mistral, Tavily, BeautifulSoup
  - `.env.example` and `.gitignore`

- **Step 2: Custom Tools (`tools.py`)** (Pending ⬜)
  - `@tool web_search`: Tavily API integration returning live internet search results.
  - `@tool scrape_url`: BeautifulSoup web scraper extracting clean, readable text from target URLs.

- **Step 3: Multi-Agent & Chains System (`agents.py`)** (Pending ⬜)
  - `Search Agent`: `create_react_agent` + `AgentExecutor` with `web_search` tool.
  - `Reader Agent`: `create_react_agent` + `AgentExecutor` with `scrape_url` tool.
  - `Writer Chain`: LCEL pipe (`prompt | llm | StrOutputParser()`) synthesizing structured research report.
  - `Critic Chain`: LCEL pipe (`prompt | llm | StrOutputParser()`) auditing report with score and actionable feedback.

- **Step 4: Orchestration Pipeline (`pipeline.py`)** (Pending ⬜)
  - Supervisor function `run_research_pipeline(topic)`
  - Shared state dictionary passing data across Search → Reader → Writer → Critic.
  - Step-by-step terminal logging of each agent's execution.

- **Step 5: Run & Verification** (Pending ⬜)
  - Interactive terminal execution: `python pipeline.py`
  - End-to-end verification of search, read, write, and review workflow.

---

## Progress Summary

| Phase | Status | Plans | Complete |
|-------|--------|-------|----------|
| 1 | ⬜ | 0/2 | — |
| 2 | ⬜ | 0/2 | — |
| 3 | ⬜ | 0/2 | — |
| 4 | ⬜ | 0/2 | — |

---

## Timeline

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| 1 | — | — | — |
| 2 | — | — | — |
| 3 | — | — | — |
| 4 | — | — | — |
