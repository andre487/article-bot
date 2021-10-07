from typing import Dict, List

import requests
from bs4 import BeautifulSoup

SCHEMA_HABR = {
    'article': 'article.tm-articles-list__item',
    'title': '.tm-article-snippet__title span',
}


def get_page_content(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def parse_page(schema: Dict[str, str], contents: List[str]) -> List[Dict[str, str]]:
    articles = []
    for content in contents:
        soup = BeautifulSoup(content, 'lxml')
        for art in soup.select(schema['article']):
            articles.append(dict(
                title=art.select(schema['title'])[0].get_text(),
            ))

    return articles
