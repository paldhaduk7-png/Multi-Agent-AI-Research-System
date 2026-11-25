---
milestone: v1.0
updated: 2026-11-25
---

# Requirements

## Overview
Requirements derived from SPEC.md for traceability and coverage tracking.

---

## Functional Requirements

| ID | Requirement | Source | Phase | Status |
|----|-------------|--------|-------|--------|
| REQ-01 | Search Agent queries Tavily API and retrieves ranked URLs and snippets | SPEC Goal 1 | 1 | Pending |
| REQ-02 | Reader Agent fetches web pages and extracts sanitized body text using BeautifulSoup | SPEC Goal 1 | 1 | Pending |
| REQ-03 | Content sanitization cleans boilerplate, script/style tags, and limits token length | SPEC Goal 1 | 1 | Pending |
| REQ-04 | Writer Chain uses LangChain with Gemini/Mistral to produce a structured Markdown report | SPEC Goal 2 | 2 | Pending |
| REQ-05 | Critic Chain audits the report, generates qualitative critique, and computes a score | SPEC Goal 2 | 2 | Pending |
| REQ-06 | FastAPI service provides REST endpoints to create, list, and read research tasks | SPEC Goal 3 | 3 | Pending |
| REQ-07 | FastAPI exposes SSE endpoint streaming agent state changes, logs, and progress events | SPEC Goal 3 | 3 | Pending |
| REQ-08 | React frontend provides input for research topics and selects model/options | SPEC Goal 4 | 4 | Pending |
| REQ-09 | React UI listens to SSE to display a real-time progress timeline of active agents | SPEC Goal 4 | 4 | Pending |
| REQ-10 | React UI renders the final research report in Markdown alongside the Critic score card | SPEC Goal 4 | 4 | Pending |

---

## Non-Functional Requirements

| ID | Requirement | Category | Phase | Status |
|----|-------------|----------|-------|--------|
| NFR-01 | Graceful fallback when Tavily or web scrapers encounter rate limits or 403s | Reliability | 1 | Pending |
| NFR-02 | Model-agnostic LLM interface supporting both Gemini and Mistral via env config | Maintainability | 2 | Pending |
| NFR-03 | SSE events use standardized JSON payload schema for clean frontend parsing | Interoperability | 3 | Pending |
| NFR-04 | Responsive, clean UI with clear agent activity indicators | UX | 4 | Pending |

---

## Constraints

| ID | Constraint | Source | Impact |
|----|------------|--------|--------|
| CON-01 | Single review pass in v1 (no infinite reflection loops) | User / SPEC | Phase 2 architecture designed modularly for future loops |
| CON-02 | SSE for unidirectional live events; extensible for WebSockets | User / SPEC | Backend streaming service cleanly abstracted |
| CON-03 | API keys stored securely in `.env` | SPEC | Never committed to git |

---

## Traceability Matrix

| Requirement | Plans | Tests | Status |
|-------------|-------|-------|--------|
| REQ-01, REQ-02, REQ-03 | Phase 1 Plans | Unit & Integration tests | Pending |
| REQ-04, REQ-05 | Phase 2 Plans | Prompt & Chain validation | Pending |
| REQ-06, REQ-07 | Phase 3 Plans | API & SSE tests | Pending |
| REQ-08, REQ-09, REQ-10 | Phase 4 Plans | End-to-End integration test | Pending |
