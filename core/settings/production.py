from core.settings.base import Config


class ProductionConfig(Config):
    """ Configuration class for site production environment """

    DEBUG = False
    TESTING = False
