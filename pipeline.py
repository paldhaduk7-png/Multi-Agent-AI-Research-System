import time
from rich import print
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def _extract_content(message_content) -> str:
    """Helper to ensure content is always extracted as a clean string,
    even if the model returns a list of content blocks.
    """
    if isinstance(message_content, list):
        return "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in message_content
        )
    return str(message_content)


def run_research_pipeline(topic: str) -> dict:
    """Supervises the research pipeline across Search, Reader, Writer, and Critic."""
    state = {}
    total_start = time.time()

    # Step 1: Search Agent queries live web sources
    print("\n" + "=" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    t0 = time.time()
    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]},
        config={"recursion_limit": 6},
    )
    state["search_results"] = _extract_content(search_result["messages"][-1].content)
    print(f"\n[dim](Step 1 took {time.time() - t0:.2f}s)[/dim]")
    print("\n search result:\n", state["search_results"])

    # Step 2: Reader Agent scrapes deep content from the top URL
    print("\n" + "=" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    t0 = time.time()
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [(
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick ONE exact URL from the text below and call scrape_url once.\n\n"
                f"Search Results:\n{state['search_results']}",
            )]
        },
        config={"recursion_limit": 6},
    )
    state["scraped_content"] = _extract_content(reader_result["messages"][-1].content)
    print(f"\n[dim](Step 2 took {time.time() - t0:.2f}s)[/dim]")
    print("\nscraped content:\n", state["scraped_content"])

    # Step 3: Writer Chain synthesizes findings into a full report
    print("\n" + "=" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    t0 = time.time()
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    print(f"\n[dim](Step 3 took {time.time() - t0:.2f}s)[/dim]")
    print("\n Final Report:\n", state["report"])

    # Step 4: Critic Chain evaluates the draft report and scores it
    print("\n" + "=" * 50)
    print("step 4 - critic is reviewing the report ...")
    print("=" * 50)

    t0 = time.time()
    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })
    print(f"\n[dim](Step 4 took {time.time() - t0:.2f}s)[/dim]")
    print("\n critic report:\n", state["feedback"])

    print(f"\n[bold green]Total pipeline time: {time.time() - total_start:.2f}s[/bold green]")
    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ").strip()
    if not topic:
        topic = "Agentic AI Trends"
    run_research_pipeline(topic)
