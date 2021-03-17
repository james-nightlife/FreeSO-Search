import os

class BaseConfig:
    FREESO_API_BASE_URL = 'https://api.freeso.org'

class DevConfig(BaseConfig):
    ENV = 'development'

class ProdConfig(BaseConfig):
    ENV = 'production'

configurations = {
    'dev' : DevConfig,
    'prod' : ProdConfig
}