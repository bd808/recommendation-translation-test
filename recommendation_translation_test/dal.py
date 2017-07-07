import psycopg2
from psycopg2 import sql

_connection = None


def _get_connection():
    global _connection
    if _connection is None or _connection.closed != 0:
        _connection = psycopg2.connect(dbname='test', user='testing', password='testing', host='localhost')
        _connection.autocommit = True
    return _connection


def get_items(source, target, count):
    query = sql.SQL((
        'select id, {target} as prediction from predictions'
        ' where {target} is not null'
        ' and {source} is null'
        ' order by {target} desc'
        ' limit {count};')).format(
        target=sql.Identifier('{}wiki'.format(target)),
        source=sql.Identifier('{}wiki'.format(source)),
        count=sql.Literal(count))

    with _get_connection().cursor() as cursor:
        try:
            cursor.execute(query)
            results = cursor.fetchall()
        except psycopg2.Error as e:
            cursor.close()
            print(e)
            return []

    return [{'id': result[0], 'prediction': result[1]} for result in results]


def sort_items(source, target, items, count):
    query = sql.SQL((
        'select id, {target} as prediction from predictions'
        ' where id in %s'
        ' and {target} is not null'
        ' and {source} is null'
        ' order by {target} desc'
        ' limit {count};')).format(
        target=sql.Identifier('{}wiki'.format(target)),
        source=sql.Identifier('{}wiki'.format(source)),
        count=sql.Literal(count))

    with _get_connection().cursor() as cursor:
        try:
            cursor.execute(query, [tuple(items)])
            results = cursor.fetchall()
        except psycopg2.Error as e:
            cursor.close()
            print(e)
            return []

    return [{'id': result[0], 'prediction': result[1]} for result in results]
