import requests
import feedparser

def search_arxiv(query: str, max_results=10):
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results
    }
    response = requests.get(base_url, params=params)
    feed = feedparser.parse(response.content)
    
    results = []
    for entry in feed.entries:
        results.append({
            "id": entry.id.split('/abs/')[-1],
            "title": entry.title.replace('\n', ' '),
            "authors": [a.name for a in entry.authors],
            "date": entry.published,
            "abstract": entry.summary,
            "source": "arXiv"
        })
    return results