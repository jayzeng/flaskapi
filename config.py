class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost:5432/api'

class TestingConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost:5432/api'

class StageConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost:5432/api'

config = {
    'development': DevelopmentConfig,
    'test': TestingConfig
}
