import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from rich import print
from tools import web_search, scrape_url

load_dotenv()

# ── Primary Model: Google Gemini ──────────────────────────────────────────────
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=gemini_key,
    temperature=0,
)

# ── Fallback Model: Mistral AI ────────────────────────────────────────────────
# Automatically invoked when Gemini hits quota / rate-limit (429)
mistral_key = os.getenv("MISTRAL_API_KEY")
if mistral_key:
    from langchain_mistralai import ChatMistralAI

    mistral_llm = ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=mistral_key,
        temperature=0,
    )
    # with_fallbacks: LangChain seamlessly retries on Gemini failure → Mistral
    llm = gemini_llm.with_fallbacks([mistral_llm])
else:
    llm = gemini_llm


def _safe_llm_call(chain, inputs: dict) -> str:
    """
    Wraps any LangChain chain.invoke() call.
    - On Gemini quota exhaustion (429), retries directly on Mistral if available.
    - On any other error, raises a clean RuntimeError with a user-friendly message.
    """
    try:
        return chain.invoke(inputs)
    except Exception as e:
        err = str(e)

        # Gemini quota / rate-limit hit → try Mistral directly
        if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower():
            if mistral_key:
                try:
                    # Re-build chain with pure Mistral (bypass the with_fallbacks wrapper)
                    if hasattr(chain, "steps"):
                        # LCEL pipeline: replace first step (the LLM) with mistral_llm
                        new_chain = chain.steps[0] | mistral_llm | chain.steps[-1]
                    else:
                        new_chain = mistral_llm
                    return new_chain.invoke(inputs)
                except Exception as mistral_err:
                    raise RuntimeError(
                        f"⚠️ Gemini quota exhausted AND Mistral also failed.\n"
                        f"Gemini error: {err[:200]}\n"
                        f"Mistral error: {str(mistral_err)[:200]}\n\n"
                        f"Fix: Check your MISTRAL_API_KEY or wait for Gemini quota reset."
                    ) from mistral_err
            else:
                raise RuntimeError(
                    "⚠️ Gemini Free Tier quota exhausted (429 RESOURCE_EXHAUSTED).\n"
                    "No Mistral fallback configured (MISTRAL_API_KEY missing).\n\n"
                    "Options:\n"
                    "  1. Add MISTRAL_API_KEY to your .env file\n"
                    "  2. Wait for Gemini quota to reset (resets daily at midnight PT)\n"
                    "  3. Visit https://ai.dev/rate-limit to check your usage"
                ) from e

        # Any other error → clean message
        raise RuntimeError(f"LLM call failed: {err[:400]}") from e


# ── 1st agent: Search Agent ───────────────────────────────────────────────────
def build_search_agent():
    """Builds the search agent with web_search tool (Gemini primary, Mistral fallback)."""
    return create_agent(
        model=llm,
        tools=[web_search],
    )


# ── 2nd agent: Reader Agent ───────────────────────────────────────────────────
def build_reader_agent():
    """Builds the reader agent with scrape_url tool (Gemini primary, Mistral fallback)."""
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )


# ── Writer Chain (LCEL) ───────────────────────────────────────────────────────
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


def invoke_writer(topic: str, research: str) -> str:
    """Safe writer chain call with quota fallback."""
    return _safe_llm_call(writer_chain, {"topic": topic, "research": research})


# ── Critic Chain (LCEL) ───────────────────────────────────────────────────────
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


def invoke_critic(report: str) -> str:
    """Safe critic chain call with quota fallback."""
    return _safe_llm_call(critic_chain, {"report": report})


if __name__ == "__main__":
    print("[bold magenta]Testing agents.py with Gemini + Mistral Fallback...[/bold magenta]")

    search_agent = build_search_agent()
    print("[bold green]✔ Search Agent ready (with automatic fallback)[/bold green]")

    reader_agent = build_reader_agent()
    print("[bold green]✔ Reader Agent ready (with automatic fallback)[/bold green]")

    print("[bold green]✔ Writer Chain ready (LCEL)[/bold green]")
    print("[bold green]✔ Critic Chain ready (LCEL)[/bold green]")
    print("[bold cyan]Setup complete: Gemini is primary, Mistral is fallback on quota exhaustion![/bold cyan]")
