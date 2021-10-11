import json
import logging
import time

import click

import scrapper


@click.group()
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')


@main.command()
@click.option('--start-page', default='https://habr.com/ru/all/top100/', show_default=True)
@click.option('--page-count', default=50, show_default=True)
@click.argument('result_file', required=True)
def habr_top(start_page: str, page_count: int, result_file: str):
    contents = []
    for i in range(1, page_count + 1):
        logging.info(f'Get page {i} content')
        content = scrapper.get_page_content(start_page + f'page{i}/')
        contents.append(content)
        time.sleep(0.25)

    logging.info('Parse pages')
    parsed_page = scrapper.parse_page(scrapper.SCHEMA_HABR, contents)

    with open(result_file, 'w') as fp:
        json.dump(parsed_page, fp, indent=2, ensure_ascii=False)


@main.command()
@click.option('--start-page', default='https://habr.com/ru/users/', show_default=True)
@click.option('--page-count', default=5, show_default=True)
@click.option('--favorite-page-count', default=10, show_default=True)
@click.argument('result_file', required=True)
def habr_users(start_page: str, page_count: int, favorite_page_count: int, result_file: str):
    contents = []
    for i in range(1, page_count + 1):
        logging.info(f'Get page {i} content')
        content = scrapper.get_page_content(start_page + f'page{i}/')
        contents.append(content)
        time.sleep(0.25)

    users = scrapper.parse_users(scrapper.SCHEMA_HABR, contents)
    logging.info(f'Got {len(users)} users')

    result = []
    for user_name in users:
        logging.info(f'Get favorites for {user_name}')
        favorites_link = f'https://habr.com/ru/users/{user_name}/favorites/posts/'
        contents = []
        for i in range(1, favorite_page_count + 1):
            logging.info(f'Get favorites of {user_name} page {i} content')
            content = scrapper.get_page_content(favorites_link + f'page{i}/')
            contents.append(content)
            time.sleep(0.25)

        logging.info(f'Parse pages for {user_name}')
        parsed_page = scrapper.parse_page(scrapper.SCHEMA_HABR, contents, const_fields={'user': user_name})
        result.extend(parsed_page)

    with open(result_file, 'w') as fp:
        json.dump(result, fp, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
