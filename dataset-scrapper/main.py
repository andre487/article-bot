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
def habr(start_page: str, page_count: int, result_file: str):
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



if __name__ == '__main__':
    main()
