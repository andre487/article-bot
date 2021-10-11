import logging
import re
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

SCHEMA_HABR = {
    'domain': 'habr.com',
    'user_in_list': '.tm-user-snippet__nickname',
    'article': 'article.tm-articles-list__item',
    'title': '.tm-article-snippet__title span',
    'preview': '.tm-article-body',
    'full_article': '.article-formatted-body',
    'tag': '.tm-article-snippet__hubs-item',
    'link': '.tm-article-snippet__title-link',
}

space_replacer = re.compile(r'\s+')


def get_page_content(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def parse_users(schema: Dict[str, str], contents: List[str]) -> List[str]:
    users = []
    for content in contents:
        soup = BeautifulSoup(content, 'lxml')
        for user_node in soup.select(schema['user_in_list']):
            user_name = get_node_text(user_node)
            if user_name.startswith('@'):
                user_name = user_name[1:]
            users.append(user_name)
    return users


def parse_page(schema: Dict[str, str], contents: List[str], const_fields: Dict[str, str] = None) -> List[Dict[str, str]]:
    if const_fields is None:
        const_fields = {}

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
                **const_fields,
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
        item = result_set
        if not getattr(item, 'find_all', None):
            item = result_set[0]
        texsts = item.find_all(string=True)
        return space_replacer.sub(' ', ' '.join(texsts).strip())
    return ''


def parse_tags(result_set: Any) -> List[str]:
    result = []
    for item in result_set:
        texsts = item.find_all(string=True)
        result.append(' '.join(texsts).strip())
    return result


def parse_link(domain: str, result_set: Any) -> str:
    if len(result_set) == 0:
        return ''
    url = result_set[0].attrs['href']
    if url.startswith('/'):
        return f'https://{domain}{url}'
    return url
