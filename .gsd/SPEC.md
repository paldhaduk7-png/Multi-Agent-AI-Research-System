# SPEC.md — Project Specification

> **Status**: `FINALIZED`
>
> ⚠️ **Planning Lock**: No code may be written until this spec is marked `FINALIZED`.

## Vision
An autonomous Multi-Agent AI Research System that conducts end-to-end web research on user-provided queries, extracts and sanitizes source content, synthesizes comprehensive research reports, critiques and scores report quality, and streams real-time agent progress and final reports through an interactive React frontend.

## Goals
1. **Search & Extraction Pipeline** — Implement a Search Agent using the Tavily Search API and a Reader Agent using BeautifulSoup to discover and scrape relevant web sources.
2. **Synthesis & Quality Auditing** — Implement a Writer Chain to generate structured research reports and a Critic Chain to review, critique, and score the research using LangChain with Google Gemini and Mistral AI models.
3. **Modular API & Real-Time Streaming** — Expose a FastAPI backend providing REST endpoints for research task lifecycle management and Server-Sent Events (SSE) for streaming agent status, intermediate findings, and workflow progress.
4. **Interactive React UI** — Deliver a modern React single-page application enabling query submission, visual agent timeline monitoring via SSE, and rich Markdown report visualization with critic scorecards.

## Non-Goals (Out of Scope for v1)
- Autonomous iterative loop where Writer and Critic re-draft indefinitely (v1 uses a single review pass; architecture remains extensible for loops later).
- Bi-directional WebSockets (v1 relies on REST + SSE; architecture remains modular for WebSockets if needed later).
- Multi-tenant authentication, user billing, or persistent cloud database clusters (local / file-based / SQLite storage for v1).

## Users
- **Knowledge Workers & Researchers**: Seeking automated, citation-backed web research synthesis without manual browsing.
- **Engineers & AI Developers**: Exploring modular multi-agent architectures combining search, scraping, generation, and critique.

## Constraints
- **Language / Runtime**: Python 3.10+ backend in `.venv` on Windows.
- **Agent / LLM Framework**: LangChain (with custom agent loops), Google Gemini API, Mistral AI API.
- **Search & Scraping**: Tavily Search API, BeautifulSoup4, `httpx`/`requests`.
- **Backend**: FastAPI with Uvicorn and SSE streaming support.
- **Frontend**: React (Vite-based modern SPA).
- **Environment**: Secrets managed via `.env` (never committed to version control).

## Success Criteria
- [ ] User can submit a research topic through the React UI or REST API.
- [ ] Search Agent executes queries via Tavily and collects relevant source links.
- [ ] Reader Agent scrapes web pages using BeautifulSoup, cleaning HTML into structured text.
- [ ] Writer Chain generates a structured Markdown report citing retrieved sources using Gemini or Mistral.
- [ ] Critic Chain evaluates the generated report and assigns an objective quality score with structured feedback.
- [ ] Backend streams live agent activity events (Search -> Scrape -> Write -> Critic) to the frontend via SSE.
- [ ] React UI displays live execution status, the final Markdown report, and the Critic review card.

---

*Last updated: 2026-11-25*
