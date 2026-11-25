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

## Phases

### Phase 1: Search & Extraction Pipeline
**Status:** ⬜ Not Started  
**Objective:** Build and verify the Search Agent (Tavily API) and Reader Agent (BeautifulSoup scraper) to acquire clean, relevant web text from research queries.  
**Requirements:** REQ-01, REQ-02, REQ-03, NFR-01  

**Plans:**
- [ ] Plan 1.1: Core environment setup, Tavily client integration, and Search Agent
- [ ] Plan 1.2: BeautifulSoup Reader Agent, HTML sanitization, and pipeline integration tests

---

### Phase 2: Synthesis & Critique Engine
**Status:** ⬜ Not Started  
**Objective:** Implement LangChain-powered Writer and Critic chains supporting Gemini and Mistral to draft reports and audit quality.  
**Depends on:** Phase 1  
**Requirements:** REQ-04, REQ-05, NFR-02  

**Plans:**
- [ ] Plan 2.1: LLM provider abstraction (Gemini + Mistral) and Writer Chain implementation
- [ ] Plan 2.2: Critic Chain evaluation prompt, scoring rubrics, and research synthesis pipeline

---

### Phase 3: FastAPI Backend & Real-time Streaming
**Status:** ⬜ Not Started  
**Objective:** Create the FastAPI application with REST endpoints for research tasks and SSE streaming for live progress updates.  
**Depends on:** Phase 2  
**Requirements:** REQ-06, REQ-07, NFR-03  

**Plans:**
- [ ] Plan 3.1: FastAPI task management REST API and async research runner
- [ ] Plan 3.2: SSE event broadcaster for real-time agent execution updates

---

### Phase 4: Streamlit Interactive UI & End-to-End Validation
**Status:** ⬜ Not Started  
**Objective:** Build a Streamlit dashboard for interactive testing of the multi-agent system, live monitoring, and report inspection.  
**Depends on:** Phase 3  
**Requirements:** REQ-08, REQ-09, REQ-10, NFR-04  

**Plans:**
- [ ] Plan 4.1: Streamlit dashboard with research query input and live agent output display
- [ ] Plan 4.2: Final report visualizer, Critic scorecard viewer, and end-to-end verification

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
