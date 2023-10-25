import os


# postgres_local_base = os.environ['DATABASE_URL']

# basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.getenv('SECRET_KEY', 'saichandra1443')
    DEBUG = False
    LOG_FORMAT = (
        '[%(asctime)s] %(levelname)s in %(filename)s:%(lineno)d '
        '%(message)s')
    PAGINATION_SEARCH_COUNT = 3


class StagingConfig(Config):
    """Configuring the Database."""
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/test'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/flask_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuring the Database."""
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/flask_db'   
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@host.docker.internal/flask_db' # configuration while running the code in docker
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Configuring the Database."""
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/flask_db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    stag=StagingConfig,
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)


key = Config.SECRET_KEY
