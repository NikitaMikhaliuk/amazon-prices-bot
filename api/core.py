from .amazon_api import AmazonApi
from .mock_api import MockApi

from enums import PyEnv
from settings import config


if config.py_env == PyEnv.PRODUCTION:
    api = AmazonApi(host=config.api_host, api_key=config.api_key.get_secret_value())
else:
    api = MockApi()
