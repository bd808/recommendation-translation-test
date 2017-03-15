import itertools
import json

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


def get_sections_by_category(category):
    results = _get_db().category_to_sections.find({'category': category})
    sections = set(itertools.chain(*[result['template'] for result in results]))
    return sections


def get_section_by_sections(sections):
    query = {'current': {'$all': sections[:2]}}
    results = _get_db().sections_to_section.find(filter=query, sort=[('confidence', -1)], limit=100)
    sections = set()
    for result in results:
        sections.update(result['missing'])
        print(sections)
    return sections
    sections = set(itertools.chain(*[result['missing'] for result in results]))
    return sections
