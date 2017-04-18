import collections
import random

import flask_restplus
from flask_restplus import reqparse
from flask_restplus import fields
from recommendation.api import helper
from recommendation.api.types.translation import candidate_finders

from recommendation_missing_sections import dal
from recommendation_missing_sections import wikipedia

api = helper.build_api('missing_sections', __name__, url_prefix='/types/missing_sections')
v1 = helper.build_namespace(api, 'v1', description='')

SectionSpec = collections.namedtuple('Section', ['name'])

sections_params = reqparse.RequestParser()

sections_params.add_argument(
    'category',
    type=str,
    required=False,
    dest='categories',
    action='append')
sections_params.add_argument(
    'section',
    type=str,
    required=False,
    dest='sections',
    action='append'
)

sections_model = v1.model(SectionSpec.__name__, SectionSpec(
    name=fields.String(description='name', required=True)
)._asdict())

sections_doc = dict(description='Gets recommendations for missing sections',
                    params=dict(category='Seed category',
                                section='Seed section'))


@v1.route('/sections')
class Sections(flask_restplus.Resource):
    @v1.expect(sections_params)
    @v1.marshal_with(sections_model, as_list=True)
    @v1.doc(**sections_doc)
    def get(self):
        kwargs = sections_params.parse_args()
        return recommend_sections(**kwargs)


def recommend_sections(categories=None, sections=None):
    results = set()
    if categories is not None:
        results.update(dal.get_sections_by_categories(categories))
    if sections is not None:
        results.update(dal.get_sections_by_sections(sections))
    return [{'name': result} for result in results]


ArticleSpec = collections.namedtuple('Article', ['title', 'sections'])

articles_params = reqparse.RequestParser()

articles_params.add_argument(
    'seed',
    type=str,
    required=False
)

articles_model = v1.model(ArticleSpec.__name__, ArticleSpec(
    title=fields.String(description='title', required=True),
    sections=fields.List(fields.String, description='sections', required=True)
)._asdict())

articles_doc = dict(description='Gets recommendations for articles that have missing sections',
                    params=dict(seed='Seed for finding articles'))


@v1.route('/articles')
class Articles(flask_restplus.Resource):
    @v1.expect(articles_params)
    @v1.marshal_with(articles_model, as_list=True)
    @v1.doc(**articles_doc)
    def get(self):
        kwargs = articles_params.parse_args()
        return recommend_articles(**kwargs)


def recommend_articles(seed=None):
    articles = []

    if seed is not None:
        candidates = candidate_finders.get_morelike_candidates('en', seed, 24)
        titles = [candidate.title for candidate in candidates]
    else:
        candidates = list(dal.get_articles_to_expand())
        titles = [candidate['title'] for candidate in candidates]

    existing_categories_by_title = wikipedia.get_sections_for_articles(titles)
    categories_by_title = wikipedia.get_categories_for_articles(titles)

    for title in titles:
        existing_sections = set(existing_categories_by_title[title])
        categories = categories_by_title[title]
        recommended_sections = dal.get_sections_by_sections(existing_sections)
        recommended_sections.update(dal.get_sections_by_categories(categories))

        if recommended_sections:
            missing_sections = list(recommended_sections - existing_sections)
            random.shuffle(missing_sections)
            if missing_sections:
                articles.append(ArticleSpec(
                    title=title,
                    sections=missing_sections[:12]
                )._asdict())

    return articles
