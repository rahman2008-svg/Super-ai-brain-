import requests

def duckduckgo_search(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    # Main direct answer
    if data.get("AbstractText"):
        return data["AbstractText"], data.get("AbstractSource")

    # Fallback: related topics
    topics = data.get("RelatedTopics")
    if topics:
        for t in topics:
            if isinstance(t, dict) and t.get("Text"):
                return t["Text"], "DuckDuckGo (Related)"

    return None, None


# Test
if __name__ == "__main__":
    ans, src = duckduckgo_search("Bangladesh population")
    if ans:
        print("Answer:", ans)
        print("Source:", src)
    else:
        print("No live info found")
