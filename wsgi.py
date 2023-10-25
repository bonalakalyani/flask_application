import os
import sys

# from unsmin.config import basedir
# sys.path.insert(0, '/opt/ITU_ENV/ITU')
#
# activate_this = '/opt/ituvenv/bin/activate_this.py'
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))


config_name = os.environ['FLASK_ENV']

from service.app import create_app

app = create_app(config_name)
