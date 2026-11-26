import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from rich import print
from tools import web_search, scrape_url

load_dotenv()

# Primary Model: Google Gemini
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=gemini_key,
    temperature=0,
)

# Automatic Fallback Model: Mistral AI (invoked if Gemini runs out of tokens or hits quota/rate limits)
mistral_key = os.getenv("MISTRAL_API_KEY")
if mistral_key:
    from langchain_mistralai import ChatMistralAI

    mistral_llm = ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=mistral_key,
        temperature=0,
    )
    # LangChain with_fallbacks: seamlessly switches to Mistral if Gemini fails
    llm = gemini_llm.with_fallbacks([mistral_llm])
else:
    llm = gemini_llm


# 1st agent: Search Agent
def build_search_agent():
    """Builds the search agent using modern create_agent with web_search tool."""
    return create_agent(
        model=llm,
        tools=[web_search],
    )


# 2nd agent: Reader Agent
def build_reader_agent():
    """Builds the reader agent using modern create_agent with scrape_url tool."""
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )


# Writer Chain
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

Be detailed, factual and professional.""",
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    (
        "human",
        """Review the research report below and evaluate it strictly.

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
...""",
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()


if __name__ == "__main__":
    print("[bold magenta]Testing agents.py with Gemini + Mistral Fallback...[/bold magenta]")

    search_agent = build_search_agent()
    print("[bold green]✔ Search Agent ready (with automatic fallback)[/bold green]")

    reader_agent = build_reader_agent()
    print("[bold green]✔ Reader Agent ready (with automatic fallback)[/bold green]")

    print("[bold green]✔ Writer Chain ready (LCEL)[/bold green]")
    print("[bold green]✔ Critic Chain ready (LCEL)[/bold green]")
    print("[bold cyan]Setup complete: Gemini is primary, Mistral is fallback on token/quota exhaustion![/bold cyan]")
