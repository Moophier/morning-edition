from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


def _fetch_readme_raw(full_name):
    """Fetch README from raw.githubusercontent.com (no auth needed)."""
    url = f"https://raw.githubusercontent.com/{full_name}/main/README.md"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        return resp.text[:4000]
    # Try master branch
    url = f"https://raw.githubusercontent.com/{full_name}/master/README.md"
    resp = requests.get(url, timeout=15)
    if resp.status_code == 200:
        return resp.text[:4000]
    return ""


def fetch_trending(top_n=10, language=None):
    """
    Fetch trending repos via GitHub search API with minimal auth footprint.
    Uses only 1 API call (search) + N raw content fetches (no auth needed).
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "stars:>1",
        "sort": "updated",
        "order": "desc",
        "per_page": 30,
    }
    headers = {"Accept": "application/vnd.github.v3+json"}

    print("  Fetching repo list from GitHub...")
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    repos = []
    for item in data.get("items", []):
        repos.append(
            {
                "name": item["full_name"],
                "short_name": item["name"],
                "description": (item.get("description") or ""),
                "owner": item["owner"]["login"],
                "stars": item["stargazers_count"],
                "forks": item["forks_count"],
                "language": item.get("language", ""),
                "url": item["html_url"],
                "topics": item.get("topics", []),
            }
        )

    # Sort by stars desc (closest proxy to "trending" without auth)
    repos.sort(key=lambda r: r["stars"], reverse=True)
    repos = repos[:top_n]

    # Fetch READMEs (no auth)
    for i, repo in enumerate(repos):
        print(f"  [{i + 1}/{len(repos)}] Fetching README: {repo['name']}")
        repo["readme"] = _fetch_readme_raw(repo["name"])

    return repos
