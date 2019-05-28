from flask import current_app
import os


class base_config:
    SITE_NAME = os.environ.get('APP_NAME', 'Maths Race')

    SECRET_KEY = os.environ.get('SECRET_KEY',
                                'secret')

    DATABASE = os.environ.get('DATABASE',
                              os.path.join(current_app.instance_path, 'mathsrace.sqlite'))

    SUPPORTED_LOCALES = ['en']


class dev_config(base_config):
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False


class test_config(base_config):
    TESTING = True
    WTF_CSRF_ENABLED = False
