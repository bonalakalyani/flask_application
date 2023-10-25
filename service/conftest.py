import os
import pytest
from wsgi import create_app

config_name = os.environ['FLASK_ENV']


@pytest.fixture
def app():
    app = create_app(config_name)
    return app
