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
    # Shared state dictionary to pass findings between agents
    state = {}

    # -------------------------------------------------------------
    # Step 1: Search Agent queries live web sources
    # -------------------------------------------------------------
    print("\n" + " =" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = _extract_content(search_result["messages"][-1].content)

    print("\n search result:\n", state["search_results"])

    # -------------------------------------------------------------
    # Step 2: Reader Agent scrapes deep content from the top URL
    # -------------------------------------------------------------
    print("\n" + " =" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [(
            "user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}",
        )]
    })
    state["scraped_content"] = _extract_content(reader_result["messages"][-1].content)

    print("\nscraped content:\n", state["scraped_content"])

    # -------------------------------------------------------------
    # Step 3: Writer Chain synthesizes findings into a full report
    # -------------------------------------------------------------
    print("\n" + " =" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    print("\n Final Report:\n", state["report"])

    # -------------------------------------------------------------
    # Step 4: Critic Chain evaluates the draft report and scores it
    # -------------------------------------------------------------
    print("\n" + " =" * 50)
    print("step 4 - critic is reviewing the report ")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\n critic report:\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ").strip()
    if not topic:
        topic = "Agentic AI Trends"
    run_research_pipeline(topic)
