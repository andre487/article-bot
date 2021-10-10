import logging
import re
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup, NavigableString

SCHEMA_HABR = {
    'domain': 'habr.com',
    'article': 'article.tm-articles-list__item',
    'title': '.tm-article-snippet__title span',
    'preview': '.tm-article-body',
    'full_article': '.article-formatted-body',
    'tag': '.tm-article-snippet__hubs-item',
    'link': '.tm-article-snippet__title-link',
}

space_replacer = re.compile(r'\s+')
url_replacer = re.compile(r'https?://([^/]+)(?:/.+)?$')


def get_page_content(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def parse_page(schema: Dict[str, str], contents: List[str]) -> List[Dict[str, str]]:
    articles = []
    for content in contents:
        soup = BeautifulSoup(content, 'lxml')
        for art in soup.select(schema['article']):
            art_title = get_node_text(art.select(schema['title']))
            logging.info(f'Parse {art_title}')

            art_url = parse_link(schema['domain'], art.select(schema['link']))

            art_text = ''
            art_data = dict(
                title=art_title,
                preview=get_node_text(art.select(schema['preview'])),
                article=art_text,
                tags=parse_tags(art.select(schema['tag'])),
                link=art_url,
            )
            articles.append(art_data)

            if art_url:
                resp = requests.get(art_url)
                if resp.ok:
                    art_text = get_node_text(BeautifulSoup(resp.text, 'lxml').select(schema['full_article']))
                    art_data['article'] = art_text

    return articles


def get_node_text(result_set: Any) -> str:
    if len(result_set):
        item = result_set[0]
        texsts = item.findAll(text=lambda x: isinstance(x, NavigableString))
        return url_replacer.sub(r'\1', space_replacer.sub(' ', ' '.join(texsts).strip()))
    return ''


def parse_tags(result_set: Any) -> List[str]:
    result = []
    for item in result_set:
        texsts = item.findAll(text=lambda x: isinstance(x, NavigableString))
        result.append(' '.join(texsts).strip())
    return result


def parse_link(domain: str, result_set: Any) -> str:
    if len(result_set) == 0:
        return ''
    url = result_set[0].attrs['href']
    if url.startswith('/'):
        return f'https://{domain}{url}'
    return url
