import itertools

import pymongo

_client = None
_db = None


def _get_client():
    global _client
    if _client is None:
        _client = pymongo.MongoClient('localhost', 27017)
    return _client


def _get_db():
    global _db
    if _db is None:
        _db = _get_client().test
    return _db


def get_sections_by_categories(categories):
    pipeline = [
        {'$match': {'category': {'$in': categories}}},
        {'$group': {
            '_id': '$category',
            'sections': {
                '$push': '$template'
            }
        }},
        {'$unwind': '$sections'},
        {'$unwind': '$sections'},
        {'$group': {
            '_id': '$_id',
            'sections': {
                '$addToSet': '$sections'
            }
        }}
    ]
    results = _get_db().category_to_sections.aggregate(pipeline)
    sections = set(itertools.chain(*[result['sections'] for result in results]))
    return sections


def get_sections_by_sections(sections):
    sections -= {'REFERENCES', 'EXTERNAL LINKS', 'SEE ALSO'}
    if sections and len(sections) < 9:
        query = {'current': list(sections), 'confidence': {'$gte': 0.9}}
        results = _get_db().sections_to_section.find(filter=query, sort=[('confidence', -1)], limit=100)
        sections = set()
        for result in results:
            sections.update(result['missing'])
        return sections
    else:
        return set()


def get_articles_to_expand():
    pipeline = [{'$sample': {'size': 24}}]
    results = _get_db().title_to_stub.aggregate(pipeline)
    return results
