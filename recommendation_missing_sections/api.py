import collections

import flask_restplus
from flask_restplus import reqparse
from flask_restplus import fields
from recommendation.api import helper

api = helper.build_api('missing_sections', __name__, url_prefix='/types/missing_sections')
v1 = helper.build_namespace(api, 'v1', description='')

SectionSpec = collections.namedtuple('Section', ['name'])

v1_params = reqparse.RequestParser()

v1_params.add_argument(
    'title',
    type=str,
    required=True)

v1_model = v1.model(SectionSpec.__name__, SectionSpec(
    name=fields.String(description='name', required=True)
)._asdict())

v1_doc = dict(description='Gets recommendations for sections missing in an article',
              params=dict(title='Title of the article to get missing sections for')
              )

@v1.route('/sections')
class Section(flask_restplus.Resource):
    @v1.expect(v1_params)
    @v1.marshal_with(v1_model, as_list=True)
    @v1.doc(**v1_doc)
    def get(self):
        args = v1_params.parse_args()
        return process_request(args)


def process_request(args):
    sections = recommend(**args)
    return sections


def recommend(title):
    return []
