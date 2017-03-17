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
