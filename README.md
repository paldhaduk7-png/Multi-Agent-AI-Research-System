# Multi-Agent AI Research System

An autonomous, multi-agent AI research pipeline that takes any research topic, queries real-time web sources, scrapes full-text web pages, drafts a structured academic/industry research report, and evaluates its own output through a critic agent.

Powered by **Groq** (`openai/gpt-oss-20b`), **Tavily API**, and **LangChain**.

---

## Architecture Diagram

```mermaid
flowchart TD
    User(["User Input: Research Topic"]) --> Pipeline["pipeline.py: run_research_pipeline()"]

    subgraph Step1["Step 1: Web Search"]
        Pipeline --> SA["Search Agent (agents.py)"]
        SA --> LLM1["ChatGroq LLM"]
        SA --> ToolSearch["web_search (tools.py)"]
        ToolSearch --> Tavily["Tavily Search API"]
        Tavily --> ResSearch["Top 5 Search Results & URLs"]
        ResSearch --> StateSearch["state['search_results']"]
    end

    subgraph Step2["Step 2: Deep Scraping"]
        StateSearch --> RA["Reader Agent (agents.py)"]
        RA --> LLM2["ChatGroq LLM"]
        RA --> ToolScrape["scrape_url (tools.py)"]
        ToolScrape --> BS4["Requests + BeautifulSoup"]
        BS4 --> ResScrape["Clean Text (capped at 2500 chars)"]
        ResScrape --> StateScrape["state['scraped_content']"]
    end

    subgraph Step3["Step 3: Synthesis & Drafting"]
        StateSearch & StateScrape --> WC["Writer Chain (agents.py)"]
        WC --> LLM3["ChatGroq LCEL Chain"]
        LLM3 --> ResReport["Structured Research Report"]
        ResReport --> StateReport["state['report']"]
    end

    subgraph Step4["Step 4: Quality Review"]
        StateReport --> CC["Critic Chain (agents.py)"]
        CC --> LLM4["ChatGroq LCEL Chain"]
        LLM4 --> ResCritic["Score X/10 + Feedback"]
        ResCritic --> StateFeedback["state['feedback']"]
    end

    StateReport & StateFeedback --> Output(["Final Research Output & Feedback"])
```

---

## Sequence & Execution Flow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Pipeline as pipeline.py
    participant Agents as agents.py
    participant Tools as tools.py
    participant Groq as Groq API
    participant Web as Tavily / Internet

    User->>Pipeline: Enter research topic
    Note over Pipeline: Initializes state = {}

    %% Step 1
    Pipeline->>Agents: build_search_agent()
    Agents-->>Pipeline: search_agent
    Pipeline->>Agents: search_agent.invoke(topic)
    Agents->>Groq: Decide search query
    Groq-->>Agents: Call web_search tool
    Agents->>Tools: web_search(query)
    Tools->>Web: Tavily Search API
    Web-->>Tools: 5 Results with URLs
    Tools-->>Agents: Formatted search text
    Agents->>Groq: Summarize findings
    Groq-->>Agents: Key findings + URLs
    Agents-->>Pipeline: Save to state['search_results']

    %% Step 2
    Pipeline->>Agents: build_reader_agent()
    Agents-->>Pipeline: reader_agent
    Pipeline->>Agents: reader_agent.invoke(search_results)
    Agents->>Groq: Pick best URL to inspect
    Groq-->>Agents: Call scrape_url tool
    Agents->>Tools: scrape_url(url)
    Tools->>Web: HTTP GET & HTML parse
    Web-->>Tools: HTML content
    Tools-->>Agents: Clean text (up to 2500 chars)
    Agents->>Groq: Summarize scraped content
    Groq-->>Agents: Deep page summary
    Agents-->>Pipeline: Save to state['scraped_content']

    %% Step 3
    Pipeline->>Agents: writer_chain.invoke(topic, research)
    Agents->>Groq: Generate report (Intro, Findings, Conclusion, Sources)
    Groq-->>Agents: Structured Report
    Agents-->>Pipeline: Save to state['report']

    %% Step 4
    Pipeline->>Agents: critic_chain.invoke(report)
    Agents->>Groq: Evaluate report strictly
    Groq-->>Agents: Score (X/10), Strengths, Improvements, Verdict
    Agents-->>Pipeline: Save to state['feedback']

    Pipeline-->>User: Display Final Report & Critic Score
```

---

## File Structure & Responsibilities

| File | Role | Key Functions / Components |
|---|---|---|
| **`tools.py`** | External tool execution | `web_search()` (Tavily), `scrape_url()` (BeautifulSoup) |
| **`agents.py`** | AI agent definitions & chains | `build_search_agent()`, `build_reader_agent()`, `writer_chain`, `critic_chain` |
| **`pipeline.py`** | Workflow supervisor | `run_research_pipeline(topic)` |

---

## Setup & Running

### 1. Prerequisites
- Python 3.10+
- Groq API Key ([groq.com](https://console.groq.com))
- Tavily API Key ([tavily.com](https://tavily.com))

### 2. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Run the Pipeline
```bash
python pipeline.py
```
Enter your topic when prompted (e.g. `What is the impact of war on stock markets?`). The complete autonomous research process takes ~10-15 seconds.
