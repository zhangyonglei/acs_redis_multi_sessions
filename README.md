# acs_redis_multi_sessions

Multiple Redis backends for your sessions!

Designed for moving sessions from one session engine to another, and separate read/write operations.

------------
Installation
------------

> **Depend on `redis` package.**

1. Download the archive `https://github.com/zhangyonglei/acs_redis_multi_sessions`, and copy `acs_redis_multi_sessions/acs_redis_multi_sessions` path into the directory of python `site-packages` or `dist-packages` location. Or run `python setup.py install`.

2. Set `acs_redis_multi_sessions.session` as your session engine, like so::

        SESSION_ENGINE = "acs_redis_multi_sessions.session"

3. Example settings::
```
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
            'SESSION_REDIS_HOST': '172.31.2.45',
            'SESSION_REDIS_PORT': 6379,
            'SESSION_REDIS_DB': 1,
            'SESSION_REDIS_PASSWORD': '',
            'SESSION_REDIS_PREFIX': 'ds_',
            'SESSION_REDIS_SOCKET_TIMEOUT': 5,
        },
    },
)
```
4. About the "setting" section, you can refer to `django-redis-sessions` package.
You can put below settings into "settings" section.

```
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = 'password'
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_SOCKET_TIMEOUT = 1

# If you prefer domain socket connection,
# you can just add this line instead of SESSION_REDIS_HOST and SESSION_REDIS_PORT.

SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = '/var/run/redis/redis.sock'

# Redis Sentinel
SESSION_REDIS_SENTINEL_LIST = [(host, port), (host, port), (host, port)]
SESSION_REDIS_SENTINEL_MASTER_ALIAS = 'sentinel-master'

# Redis Pool (Horizontal partitioning)
# Splits sessions between Redis instances based on the session key.
# You can configure the connection type for each Redis instance in the pool (host/port, unix socket, redis url).
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_SOCKET_TIMEOUT = 1
SESSION_REDIS_RETRY_ON_TIMEOUT = False
SESSION_REDIS_POOL = [
    {
        'SESSION_REDIS_HOST': 'localhost3',
        'SESSION_REDIS_PORT': 6379,
        'SESSION_REDIS_DB': 0,
        'SESSION_REDIS_PASSWORD': None,
        'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH': None,
        'SESSION_REDIS_URL': None,
        'SESSION_REDIS_WEIGHT': 1,
    },
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
```

5. Available modes:

* "read"   - Allows launch "load" method;
* "write"  - Allows launch "save" and "create" method;
* "delete" - Allows launch the "delete" method.

6. Test
 Go to `test` path. and run `python manage.py runserver`, then visit `http://127.0.0.1:8000/test/`.

8. Validate and check keys

```
redis-cli -h localhost -p 6379 -n 0 KEYS \*
redis-cli -h localhost -p 6379 -n 1 KEYS \*
```

9. Debug Output
Put below code block into your `settings.py` file

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'test.log',
            'maxBytes': 1048576,
            'backupCount': 10
        },
    },
    'loggers': {
        'acs_redis_multi_sessions': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    }
}
```
