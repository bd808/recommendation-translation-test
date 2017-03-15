import collections

import flask_restplus
from flask_restplus import reqparse
from flask_restplus import fields
from recommendation.api import helper

from recommendation_missing_sections import dal

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
        return recommend(**kwargs)


def recommend(categories=None, sections=None):
    results = set()
    if categories is not None:
        for category in categories:
            results.update(dal.get_sections_by_category(category))
    if sections is not None:
        results.update(dal.get_section_by_sections(sections))
    return [{'name': result} for result in results]
