"""Monitor news websites and store articles.

This module fetches configured websites using the requests library and
extracts article titles and content using BeautifulSoup.  The
extracted information is stored in the SQLite database via helper
functions from ``app.database``.

The extraction logic uses `.select()` and `.find()` from BeautifulSoup
to locate elements in the HTML.  For example, `.find('h1')` returns
the first `<h1>` element and `.find_all()` returns all matching
elements【224005379937597†L80-L104】.  You can customise the CSS selectors in
your configuration file.
"""

import argparse
from datetime import datetime
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup

from .config import load_config
from .database import init_db, insert_message


def fetch_site(site: Dict[str, Any]) -> Dict[str, str]:
    """Fetch a website and extract a title and content snippet.

    Parameters
    ----------
    site : Dict[str, Any]
        A dictionary with keys ``url``, ``title_selector`` and ``content_selector``.

    Returns
    -------
    Dict[str, str]
        A dictionary with keys ``title``, ``content`` and ``url``.
    """
    url = site.get("url")
    title_selector = site.get("title_selector", "h1")
    content_selector = site.get("content_selector", "p")
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")

    # Try to locate the title using CSS selectors or fallback to find()
    title_elem = soup.select_one(title_selector) or soup.find(title_selector)
    title = title_elem.get_text(strip=True) if title_elem else url

    # Attempt to find content using select() which returns a list
    content_elems = soup.select(content_selector) or soup.find_all(content_selector)
    if not content_elems:
        content = ""
    elif isinstance(content_elems, list):
        # Concatenate up to the first five elements
        content = "\n".join(elem.get_text(strip=True) for elem in content_elems[:5])
    else:
        content = content_elems.get_text(strip=True)

    return {"title": title, "content": content, "url": url}


def monitor_websites(config: Dict[str, Any]) -> None:
    """Monitor configured websites and insert extracted data into the database."""
    news_conf = config.get("news", {})
    websites = news_conf.get("websites", [])
    db_path = config.get("database", {}).get("path", "data/news.db")
    conn = init_db(db_path)

    for site in websites:
        try:
            entry = fetch_site(site)
        except Exception as exc:
            print(f"Error fetching {site.get('url')}: {exc}")
            continue
        data = {
            "source": "website",
            "channel": entry["url"],  # use URL as channel identifier
            "title": entry["title"],
            "content": entry["content"],
            "url": entry["url"],
            "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }
        insert_message(conn, data)

    conn.close()


def main() -> None:
    """CLI entry point for the website monitor."""
    parser = argparse.ArgumentParser(description="Monitor news websites")
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to the YAML configuration file",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    monitor_websites(config)


if __name__ == "__main__":
    main()