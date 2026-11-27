import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from rich import print
from tools import scrape_url, web_search

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("Missing GROQ_API_KEY in .env file.")

# Primary Groq model (fast + strong tool calling, low reasoning effort for speed & low TPM usage)
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=groq_key,
    temperature=0,
    reasoning_effort="low",
    max_tokens=4096,
    timeout=30,
    max_retries=2,
)


def build_search_agent():
    """Builds the search agent using Groq and web_search tool."""
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a fast web research assistant. "
            "Call web_search once with a focused query, then immediately provide a concise "
            "bullet-point summary of the key findings and list the exact URLs. Do not call web_search repeatedly."
        ),
    )


def build_reader_agent():
    """Builds the reader agent using Groq and scrape_url tool."""
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a fast web reader assistant. "
            "Your ONLY available tool is `scrape_url`. Never call any other tool name. "
            "Pick ONE exact http/https URL that literally appears in the provided text. "
            "Never invent, guess, or modify a URL. Call `scrape_url` AT MOST ONCE, "
            "then immediately summarize the result (even if scraping returned an error)."
        ),
    )


writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()


if __name__ == "__main__":
    print("[bold magenta]Testing agents.py with Groq...[/bold magenta]")

    search_agent = build_search_agent()
    print("[bold green]✔ Search Agent ready (Groq)[/bold green]")

    reader_agent = build_reader_agent()
    print("[bold green]✔ Reader Agent ready (Groq)[/bold green]")

    print("[bold green]✔ Writer Chain ready (Groq LCEL)[/bold green]")
    print("[bold green]✔ Critic Chain ready (Groq LCEL)[/bold green]")
