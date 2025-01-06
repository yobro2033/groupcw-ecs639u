import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

engines = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}


def config():
    service_name = os.getenv('DATABASE_SERVICE_NAME', '').upper().replace('-', '_')
    engine_key = os.getenv('DATABASE_ENGINE', 'sqlite').lower()

    if engine_key not in engines:
        logger.error(f"Unsupported DATABASE_ENGINE: {engine_key}. Defaulting to SQLite.")
        engine_key = 'sqlite'

    engine = engines[engine_key]

    name = os.getenv('DATABASE_NAME')
    if not name and engine == engines['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    config = {
        'ENGINE': engine,
        'NAME': name,
        'USER': os.getenv('DATABASE_USER', ''),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'HOST': os.getenv(f'{service_name}_SERVICE_HOST', 'localhost'),
        'PORT': os.getenv(f'{service_name}_SERVICE_PORT', ''),
    }


    logger.info(f"Database configuration: {config}")
    return config
    
