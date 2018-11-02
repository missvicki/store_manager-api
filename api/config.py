"""config file"""
import datetime
import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """environment configurations """
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'secret'
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'


class DevelopmentConfig(BaseConfig):
    """development environment """
    ENV = 'development'
    DATABASE = 'storemanager'
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """ enables testing environment """
    ENV = 'testing'
    DATABASE = 'storemanager_test_db'
    DEBUG = True
    TESTING = True

class DeploymentConfig(BaseConfig):
    """ enables deplyment environment """
    ENV = 'deploying'
    DATABASE = 'd5ll442t19st4t'
    PASSWORD = 'a2b20d19532983892990bc0262c38e6e2d68c9e491c191e556ee015491dfcb71'
    USER = 'ptlamqvmvizpvv'
    PORT='5432'
    HOST='ec2-23-23-101-25.compute-1.amazonaws.com'
    DEBUG = False
    TESTING = False

env_config = dict(
    development = DevelopmentConfig,
    testing = TestingConfig,
    deploying = DeploymentConfig
)
