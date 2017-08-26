from django.conf import settings

SESSION_ENGINE = "acs_redis_multi_sessions.session"
ACS_SESSION_MULTISESSIONS_POOL = (
    {
        "backend": "0",
        "modes": ["read", "write"],
        "setting": {
            'SESSION_REDIS_HOST': 'localhost',
            'SESSION_REDIS_PORT': 6379,
            'SESSION_REDIS_DB': 0,
            'SESSION_REDIS_PASSWORD': '',
            'SESSION_REDIS_PREFIX': 'ds_',
            'SESSION_REDIS_SOCKET_TIMEOUT': 5,
        },
    },
    {
        "backend": "1",
        "modes": ["read", "delete"],
        "setting": {
            'SESSION_REDIS_HOST': 'localhost',
            'SESSION_REDIS_PORT': 6379,
            'SESSION_REDIS_DB': 1,
            'SESSION_REDIS_PASSWORD': '',
            'SESSION_REDIS_PREFIX': 'ds_',
            'SESSION_REDIS_SOCKET_TIMEOUT': 5,
        },
    },
)

SECRET_KEY = "test"

# For unittest
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# SESSION_REDIS_HOST = getattr(settings, 'SESSION_REDIS_HOST', 'localhost')
# SESSION_REDIS_PORT = getattr(settings, 'SESSION_REDIS_PORT', 6379)
# SESSION_REDIS_SOCKET_TIMEOUT = getattr(settings, 'SESSION_REDIS_SOCKET_TIMEOUT', 0.1)
# SESSION_REDIS_RETRY_ON_TIMEOUT = getattr(settings, 'SESSION_REDIS_RETRY_ON_TIMEOUT', False)
# SESSION_REDIS_DB = getattr(settings, 'SESSION_REDIS_DB', 0)
# SESSION_REDIS_PREFIX = getattr(settings, 'SESSION_REDIS_PREFIX', '')
# SESSION_REDIS_PASSWORD = getattr(settings, 'SESSION_REDIS_PASSWORD', None)
# SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = getattr(settings, 'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH', None)
# SESSION_REDIS_URL = getattr(settings, 'SESSION_REDIS_URL', None)

"""
Should be on the format:
[
    {
        'SESSION_REDIS_HOST': 'localhost2',
        'SESSION_REDIS_PORT': 6379,
        'SESSION_REDIS_DB': 0,
        'SESSION_REDIS_PASSWORD': None,
        'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
        'SESSION_REDIS_URL': None,
        'SESSION_REDIS_WEIGHT': 1,
    },
    {
        'SESSION_REDIS_HOST': 'localhost1',
        'SESSION_REDIS_PORT': 6379,
        'SESSION_REDIS_DB': 0,
        'SESSION_REDIS_PASSWORD': None,
        'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
        'SESSION_REDIS_URL': None,
        'SESSION_REDIS_WEIGHT': 1,
    },
]
"""
# SESSION_REDIS_POOL = getattr(settings, 'SESSION_REDIS_POOL', None)

# # should be on the format [(host, port), (host, port), (host, port)]
# SESSION_REDIS_SENTINEL_LIST = getattr(settings, 'SESSION_REDIS_SENTINEL_LIST', None)
# SESSION_REDIS_SENTINEL_MASTER_ALIAS = getattr(settings, 'SESSION_REDIS_SENTINEL_MASTER_ALIAS', None)
