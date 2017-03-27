import itertools

import psycopg2

_connection = None


def _get_connection():
    global _connection
    if _connection is None or _connection.closed != 0:
        _connection = psycopg2.connect('dbname=test user=www-data')
    return _connection


def get_sections_by_categories(categories):
    sql = 'select template from category_to_sections where category = any(%s);'

    with _get_connection().cursor() as cursor:
        cursor.execute(sql, categories)
        results = cursor.fetchall()

    sections = set(itertools.chain(*[result[0] for result in results]))
    return sections


def get_sections_by_sections(sections):
    sql = '''
    select missing from sections_to_section where
      current = (select array(select unnest(%s) as s order by s))
      and confidence >= 0.9
    order by confidence;
    '''

    sections -= {'REFERENCES', 'EXTERNAL LINKS', 'SEE ALSO'}
    if sections:
        with _get_connection().cursor() as cursor:
            cursor.execute(sql, list(sections))
            results = cursor.fetchall()
        sections = set(itertools.chain(*[result[0] for result in results]))
        return sections
    else:
        return set()


def get_articles_to_expand():
    sql = 'select * from title_to_stub limit 24;'
    with _get_connection().cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return results
