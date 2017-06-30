import collections

import flask_restplus
from flask_restplus import reqparse
from flask_restplus import fields
from flask_restplus import inputs
from recommendation.api import helper
from recommendation.api.external_data import wikidata

from recommendation_translation_test import dal

api = helper.build_api('translation_test', __name__, url_prefix='/types/translation_test')
v1 = helper.build_namespace(api, 'v1', description='')

ItemSpec = collections.namedtuple('Item', ['title', 'id', 'prediction'])

item_params = reqparse.RequestParser()

item_params.add_argument(
    'source',
    type=str,
    required=True
)
item_params.add_argument(
    'target',
    type=str,
    required=True
)
item_params.add_argument(
    'count',
    type=inputs.int_range(0, 50),
    required=False,
    default=24
)

items_model = v1.model(ItemSpec.__name__, ItemSpec(
    title=fields.String(description='title', required=True),
    id=fields.String(description='wikidata_id', required=True),
    prediction=fields.Float(description='prediction', required=True)
)._asdict())

items_doc = dict(description='Gets recommendations for translation',
                 params=dict(target='Target language',
                             count='Number of recommendations to fetch'))


@v1.route('/items')
class Items(flask_restplus.Resource):
    @v1.expect(item_params)
    @v1.marshal_with(items_model, as_list=True)
    @v1.doc(**items_doc)
    def get(self):
        kwargs = item_params.parse_args()
        return recommend_items(**kwargs)


def recommend_items(source, target, count):
    items = dal.get_items(source, target, count)
    items_map = {item['id']: {'prediction': item['prediction']} for item in items}
    wikidata_items = wikidata.get_titles_from_wikidata_items(source, items_map.keys())
    for item in wikidata_items:
        items_map[item.id]['title'] = item.title
    return sorted([dict(title=item['title'], prediction=item['prediction'], id=wikidata_id)
                  for wikidata_id, item in items_map.items() if 'title' in item],
                  key=lambda item: item['prediction'], reverse=True)
