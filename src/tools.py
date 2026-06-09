from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search(query: str) -> str:
    """Search the web using Tavily API."""
    try:
        response = tavily_client.search(query=query, max_results=5, include_answer=True)
        results_text = f"Search Results for '{query}':\n\n"
        if response.get("answer"):
            results_text += f"Summary: {response['answer']}\n\n"
        for i, result in enumerate(response.get("results", []), 1):
            results_text += f"{i}. {result['title']}\n"
            results_text += f"   URL: {result['url']}\n"
            results_text += f"   Content: {result['content'][:200]}...\n\n"
        return results_text
    except Exception as e:
        return f"Search failed: {str(e)}"

def write_file(filename: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"File '{filename}' created with {len(content)} characters."
    except Exception as e:
        return f"Write failed: {str(e)}"

def read_file(filename: str) -> str:
    """Read content from a file."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Read failed: {str(e)}"