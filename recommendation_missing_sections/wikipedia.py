from multiprocessing import dummy as multiprocessing

from recommendation.api.external_data import fetcher
from recommendation.utils import configuration


def get_sections_for_articles(titles):
    with multiprocessing.Pool(len(titles)) as pool:
        results = pool.map(get_sections_in_article, titles)
    aggregated = {}
    for result in results:
        aggregated.update(result)
    return aggregated


def get_sections_in_article(title):
    endpoint = configuration.get_config_value('endpoints', 'restbase')
    path = configuration.get_config_value('sections_query', 'path')
    endpoint = endpoint.format(source='en')
    path = path.format(title=title)
    url = endpoint + path
    try:
        result = fetcher.get(url)
    except ValueError:
        return {title: []}
    sections = {title: [item['line'].upper() for item in result.get('sections', []) if 'line' in item]}
    return sections


def get_categories_for_articles(titles):
    with multiprocessing.Pool(len(titles)) as pool:
        results = pool.map(get_categories_for_article, titles)
    aggregated = {}
    for result in results:
        aggregated.update(result)
    return aggregated


def get_categories_for_article(title):
    endpoint = configuration.get_config_value('endpoints', 'wikipedia')
    params = {
        'action': 'query',
        'prop': 'categories',
        'format': 'json',
        'titles': title
    }
    endpoint = endpoint.format(source='en')
    try:
        result = fetcher.get(endpoint, params=params)
    except ValueError:
        return {title: []}
    items = list(result.get('query', {}).get('pages', {}).values())
    if len(items) != 1:
        return {title: []}
    categories = {title: [item['title'].replace(' ', '_') for item in items[0].get('categories', []) if 'title' in item]}
    return categories
