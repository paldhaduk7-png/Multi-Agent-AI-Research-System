import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.tools import tool
from rich import print
from tavily import TavilyClient

load_dotenv()


@tool
def web_search(query: str) -> str:
    """Searches the web using Tavily API and returns relevant search results with title, URL, and snippet."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("[bold red]✖ [Tools:web_search][/bold red] Missing TAVILY_API_KEY in .env")
        return "Error: TAVILY_API_KEY environment variable is not set. Please add it to your .env file."

    print(f"[bold cyan]🔍 [Tools:web_search][/bold cyan] Searching web for: [yellow]'{query}'[/yellow]")

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=5)
        results = response.get("results", [])

        if not results:
            print(f"[bold yellow]⚠ [Tools:web_search][/bold yellow] No results found for: '{query}'")
            return f"No results found for query: '{query}'."

        print(f"[bold green]✔ [Tools:web_search][/bold green] Retrieved [bold]{len(results)}[/bold] search results.")

        formatted_output = []
        for i, res in enumerate(results, start=1):
            title = res.get("title", "No Title")
            url = res.get("url", "")
            content = res.get("content", "").strip()
            formatted_output.append(f"[{i}] {title}\nURL: {url}\nSnippet: {content}")

        return "\n\n".join(formatted_output)

    except Exception as e:
        print(f"[bold red]✖ [Tools:web_search][/bold red] Search failed: {str(e)}")
        return f"Error executing web search for '{query}': {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrapes a webpage URL and extracts clean readable text using BeautifulSoup."""

    if not url or not url.startswith(("http://", "https://")):
        return f"Error: Invalid URL '{url}'. URL must begin with http:// or https://."

    print(f"[bold cyan]🌐 [Tools:scrape_url][/bold cyan] Scraping webpage: [yellow]{url}[/yellow]")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=12)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Strip non-content elements to extract clean readable text
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "form"]):
            element.decompose()

        text = soup.get_text(separator="\n")

        # Strip empty lines and excessive whitespace
        lines = [line.strip() for line in text.splitlines()]
        clean_text = "\n".join(line for line in lines if line)

        # Truncate content (~4,000 chars) to prevent context window overflow
        max_chars = 4000
        if len(clean_text) > max_chars:
            clean_text = clean_text[:max_chars] + "\n\n[Content truncated for length...]"

        if not clean_text:
            print(f"[bold yellow]⚠ [Tools:scrape_url][/bold yellow] No readable text on page: {url}")
            return f"Notice: Webpage at {url} was reached, but no readable text could be extracted."

        print(f"[bold green]✔ [Tools:scrape_url][/bold green] Extracted [bold]{len(clean_text)}[/bold] characters from {url}")
        return f"Content extracted from {url}:\n\n{clean_text}"

    except requests.exceptions.RequestException as e:
        print(f"[bold red]✖ [Tools:scrape_url][/bold red] Network/HTTP error on {url}: {str(e)}")
        return f"Error scraping URL '{url}': {str(e)}"
    except Exception as e:
        print(f"[bold red]✖ [Tools:scrape_url][/bold red] Parsing error on {url}: {str(e)}")
        return f"Unexpected error parsing '{url}': {str(e)}"


if __name__ == "__main__":
    print("[bold magenta]Testing tools directly with rich output...[/bold magenta]")
    
    # Test 1: scrape_url
    sample_content = scrape_url.invoke({"url": "https://www.wikipedia.org"})
    print(f"\n[dim]{sample_content}[/dim]\n")

    # Test 2: web_search
    sample_search = web_search.invoke({"query": "LangChain agents"})
    print(f"\n[dim]{sample_search[:250]}...[/dim]")
