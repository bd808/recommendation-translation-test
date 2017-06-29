import psycopg2

_connection = None


def _get_connection():
    global _connection
    if _connection is None or _connection.closed != 0:
        _connection = psycopg2.connect(dbname='test', user='testing', password='testing', host='localhost')
    return _connection


def get_items(target):
    sql = 'select id, (%s)wiki as prediction from predictions order by (%s)wiki desc;'

    with _get_connection().cursor() as cursor:
        cursor.execute(sql, (target, target))
        results = cursor.fetchall()

    return [{'id': result[0], 'title': result[1]} for result in results]
