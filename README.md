# acs_redis_multi_sessions

Multiple Redis backends for your sessions!

Designed for moving sessions from one session engine to another, and separate read/write operations.

------------
Installation
------------

**Depend on `redis` package.**

1. Download the archive and run `https://github.com/zhangyonglei/acs_redis_multi_sessions`

2. Set ``acs_redis_multi_sessions.session`` as your session engine, like so::

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
