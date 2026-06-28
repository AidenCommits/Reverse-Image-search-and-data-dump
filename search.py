from ddgs import DDGS
from urllib.parse import urlparse

#identifier = print_sku()

PREFERRED_DOMAINS = [
    "amazon.com",
    "ebay.com",
    "walmart.com",
    "target.com",
    "bestbuy.com",
    "newegg.com",
    "homedepot.com",
    "lowes.com",
    "costco.com",
    "macys.com",
]

BLOCKED_DOMAINS = [
    "wikipedia.org",
    "wikidata.org",
    "facebook.com",
    "reddit.com",
    "pinterest.com",
    "youtube.com"
]

def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")

def domain_is_blocked(url):
    
    domain = get_domain(url)
    
    for blocked_domain in BLOCKED_DOMAINS:
        if blocked_domain == domain:
            return True
    
    return False

def score_result(result, identifier):
    
    score = 0

    title = result.get('title', '').lower()
    url = result.get('href', '').lower()
    domain = get_domain(url)

    identifier_lower = identifier.lower()

    if identifier_lower in title:
        score += 40
    if identifier_lower in url:
        score += 30
    for preferred_domain in PREFERRED_DOMAINS:
        if preferred_domain in domain:
            score += 50

    return score

def search_web(identifier, max_results=3):

    candidates = []

    with DDGS() as ddgs:
        results = ddgs.text(identifier, max_results=max_results)

        print(f"searching for '{len(results)}' results")
        print(results)

        for result in results:
            url = result.get('href')

            if not url:
                continue

            if domain_is_blocked(url):
                continue

            candidate = {
                "title": result.get('title', ''),
                "url": url,
                "score": score_result(result, identifier)
            }

            candidates.append(candidate)

        candidates.sort(key=lambda item: item['score'], reverse=True)

    return candidates
