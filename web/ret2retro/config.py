import os

PROJECT_NAME = 'ret2retro'

PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

ALLOWED_UPLOAD_CONTENT_TYPES = {'jpeg', 'png'}

WORKER_COUNT = int(os.getenv('WORKER_COUNT', '4'))

TEMPLATES_PATH = os.path.join(PROJECT_PATH, 'ret2retro', 'views')
UPLOAD_PATH = os.path.join(PROJECT_PATH, 'upload')
STATIC_PATH = os.path.join(PROJECT_PATH, 'static')

RET2RETRO_ENV = os.getenv('RET2RETRO_ENV', 'development')
IS_PRODUCTION = RET2RETRO_ENV == 'production'
