# DECISIONS.md — Architecture Decision Records

> **Purpose**: Log significant technical decisions and their rationale.

## [DECISION-001] Tech Stack: FastAPI, SSE, React, and LangChain

**Date**: 2026-11-25  
**Status**: Accepted  

### Context
We are designing an autonomous Multi-Agent AI Research System that requires web search, page scraping, multi-model LLM generation (Gemini + Mistral), a reviewer/critic chain, and real-time user-facing feedback.

### Decision
1. **Backend**: FastAPI with Python.
2. **Streaming**: Server-Sent Events (SSE) for unidirectional real-time progress and logs from backend to frontend.
3. **Frontend**: React (Vite SPA) displaying search input, live agent execution pipeline, and Markdown reports.
4. **Agents & LLMs**: LangChain for orchestrating chains and custom agent loops, with Google Gemini and Mistral AI as model providers.
5. **Search & Scrape**: Tavily Search API for high-relevance search results; BeautifulSoup4 for HTML cleaning and extraction.

### Rationale
- SSE is lightweight, native over HTTP, and easier to debug and scale than full duplex WebSockets for one-directional research progress streaming.
- LangChain provides standardized interfaces for Gemini (`langchain-google-genai`) and Mistral (`langchain-mistralai`).
- Tavily is optimized for agentic search; BeautifulSoup handles resilient content extraction.

### Consequences
- Architecture is kept modular so WebSockets and multi-turn iterative feedback loops can be introduced later without major rewrites.

---

## [DECISION-002] Linear Writer-Critic Review for v1

**Date**: 2026-11-25  
**Status**: Accepted  

### Context
The user requested a Writer chain that creates a research report and a Critic chain that reviews and assigns a score to the research.

### Decision
Implement a single-pass review for v1 (Search -> Scrape -> Write -> Critic -> Output), while designing the chain output schema to support iterative feedback loops in future iterations.

### Rationale
Ensures predictable execution times and token costs for v1 while proving the end-to-end multi-agent pipeline.
