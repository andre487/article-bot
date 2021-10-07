import logging
import time

import click

import scrapper


@click.group()
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')


@main.command()
@click.option('--start-page', default='https://habr.com/ru/all/top100/', show_default=True)
@click.option('--page-count', default=10, show_default=True)
def habr(start_page: str, page_count: int):
    contents = []
    for i in range(1, page_count + 1):
        logging.info(f'Get page {i} content')
        content = scrapper.get_page_content(start_page + f'page{i}/')
        contents.append(content)
        time.sleep(0.1)

    logging.info('Parse pages')
    parsed_page = scrapper.parse_page(scrapper.SCHEMA_HABR, contents)

    print(parsed_page)



if __name__ == '__main__':
    main()
