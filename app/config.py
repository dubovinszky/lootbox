import os

base_dir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres@localhost/'
database_name = 'lootbox'


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_strong_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRIZES_PER_DAY = 5
    WIN_LIMIT = 0.7
    DAILY_MODIFIER = 0.05
    MIN_USER_CHANCE = 0.5
    MIN_DAILY_MODIFIER = 0.8
    USER_CHANCE_MODIFIER = 0.1
    USER_CHANCE_RESET_DAYS = 5
    PRESENTATION_MODE = True
    PRESENTATION_ID = 107


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        postgres_local_base + database_name)


class TestingConfig(BaseConfig):
    """
    Testing application configuration
    """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL_TEST',
        postgres_local_base + database_name + "_test")


class ProductionConfig(BaseConfig):
    """
    Production application configuration
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        postgres_local_base + database_name)
