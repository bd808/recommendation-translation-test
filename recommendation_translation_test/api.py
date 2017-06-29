import collections

import flask_restplus
from flask_restplus import reqparse
from flask_restplus import fields
from recommendation.api import helper

from recommendation_translation_test import dal

api = helper.build_api('translation_test', __name__, url_prefix='/types/translation_test')
v1 = helper.build_namespace(api, 'v1', description='')

ItemSpec = collections.namedtuple('Item', ['id', 'prediction'])

item_params = reqparse.RequestParser()

item_params.add_argument(
    'target',
    type=str,
    required=True
)

items_model = v1.model(ItemSpec.__name__, ItemSpec(
    id=fields.String(description='wikidata_id', required=True),
    prediction=fields.Float(description='prediction', required=True)
)._asdict())

items_doc = dict(description='Gets recommendations for translation',
                 params=dict(target='Target language'))


@v1.route('/items')
class Items(flask_restplus.Resource):
    @v1.expect(item_params)
    @v1.marshal_with(items_model, as_list=True)
    @v1.doc(**items_doc)
    def get(self):
        kwargs = item_params.parse_args()
        return recommend_items(**kwargs)


def recommend_items(target):
    return dal.get_items(target)
