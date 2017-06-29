from flask import Flask

from recommendation_translation_test import api
from recommendation.utils import logger

logger.initialize_logging()

app = Flask(__name__)
app.register_blueprint(api.api.blueprint)

app.config['RESTPLUS_VALIDATE'] = True
app.config['RESTPLUS_MASK_SWAGGER'] = False
application = app

if __name__ == '__main__':
    application.run()

