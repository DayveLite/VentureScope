from tavily import TavilyClient

from app.config import TAVILY_API_KEY


def search_web(query: str, max_results: int = 5) -> dict:
    """
    Search the web and return structured research results.
    """

    if not TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY is missing.")

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not 1 <= max_results <= 10:
        raise ValueError("max_results must be between 1 and 10.")

    client = TavilyClient(api_key=TAVILY_API_KEY)

    response = client.search(
        query=query.strip(),
        search_depth="basic",
        max_results=max_results,
        include_answer=True,
    )

    return {
        "query": query.strip(),
        "answer": response.get("answer"),
        "results": [
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
                "score": item.get("score"),
            }
            for item in response.get("results", [])
        ],
    }
