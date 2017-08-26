# coding: utf-8

import redis
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
try:
    from django.utils.encoding import force_unicode
except ImportError:  # Python 3.*
    from django.utils.encoding import force_text as force_unicode

class Dict(object):
    def __init__(self, _dict):
        self.__dict__.update(_dict)

class RedisServer():
    __redis = {}

    def __init__(self, session_key, engine_settings):
        self.session_key = session_key
        self.connection_key = ''
        self.connection_type = ''

        if engine_settings:
            self.engine_backend = engine_settings
            self.engine_settings = Dict(engine_settings['setting'])
        else:
            self.engine_settings = settings
            self.engine_backend = None

        if getattr(self.engine_settings, 'SESSION_REDIS_SENTINEL_LIST', None) is not None:
            self.connection_type = 'sentinel'
        else:
            if getattr(self.engine_settings, 'SESSION_REDIS_POOL', None) is not None:
                server_key, server = self.get_server(session_key, getattr(self.engine_settings, 'SESSION_REDIS_POOL', None))
                self.connection_key = str(server_key)
                self.engine_settings.SESSION_REDIS_HOST = getattr(server, 'SESSION_REDIS_HOST', 'localhost')
                self.engine_settings.SESSION_REDIS_PORT = getattr(server, 'SESSION_REDIS_PORT', 6379)
                self.engine_settings.SESSION_REDIS_DB = getattr(server, 'SESSION_REDIS_DB', 0)
                self.engine_settings.SESSION_REDIS_PASSWORD = getattr(server, 'SESSION_REDIS_PASSWORD', None)
                self.engine_settings.SESSION_REDIS_URL = getattr(server, 'SESSION_REDIS_URL', None)
                self.engine_settings.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = getattr(server,
                                                                         'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH', None)

            if getattr(self.engine_settings, 'SESSION_REDIS_URL', None) is not None:
                self.connection_type = 'redis_url'
            elif getattr(self.engine_settings, 'SESSION_REDIS_HOST', None) is not None:
                self.connection_key = self.engine_backend and str(self.engine_backend.get('backend', 0))
                self.connection_type = 'redis_host'
            elif getattr(self.engine_settings, 'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH', None) is not None:
                self.connection_type = 'redis_unix_url'

        self.connection_key += self.connection_type

    def get_server(self, key, servers_pool):
        total_weight = sum([row.get('SESSION_REDIS_WEIGHT', 1) for row in servers_pool])
        pos = 0
        for i in range(3, -1, -1):
            pos = pos * 2 ** 8 + ord(key[i])
        pos = pos % total_weight

        pool = iter(servers_pool)
        server = next(pool)
        server_key = 0
        i = 0
        while i < total_weight:
            if i <= pos < (i + server.get('SESSION_REDIS_WEIGHT', 1)):
                return server_key, server
            i += server.get('SESSION_REDIS_WEIGHT', 1)
            server = next(pool)
            server_key += 1

        return

    def get(self):
        if self.connection_key in self.__redis:
            return self.__redis[self.connection_key]

        if self.connection_type == 'sentinel':
            from redis.sentinel import Sentinel
            self.__redis[self.connection_key] = Sentinel(
                getattr(self.engine_settings, 'SESSION_REDIS_SENTINEL_LIST', None),
                socket_timeout=getattr(self.engine_settings, 'SESSION_REDIS_SOCKET_TIMEOUT', 0.1),
                retry_on_timeout=getattr(self.engine_settings, 'SESSION_REDIS_RETRY_ON_TIMEOUT', False),
                db=getattr(self.engine_settings, 'SESSION_REDIS_DB', 0),
                password=getattr(self.engine_settings, 'SESSION_REDIS_PASSWORD', None)
            ).master_for(getattr(self.engine_settings, 'SESSION_REDIS_SENTINEL_MASTER_ALIAS', None))

        elif self.connection_type == 'redis_url':
            self.__redis[self.connection_key] = redis.StrictRedis.from_url(
                getattr(self.engine_settings, 'SESSION_REDIS_URL', None),
                socket_timeout=getattr(self.engine_settings, 'SESSION_REDIS_SOCKET_TIMEOUT', 0.1)
            )
        elif self.connection_type == 'redis_host':
            self.__redis[self.connection_key] = redis.StrictRedis(
                host=getattr(self.engine_settings, 'SESSION_REDIS_HOST', None),
                port=getattr(self.engine_settings, 'SESSION_REDIS_PORT', 6379),
                socket_timeout=getattr(self.engine_settings, 'SESSION_REDIS_SOCKET_TIMEOUT', 0.1),
                retry_on_timeout=getattr(self.engine_settings, 'SESSION_REDIS_RETRY_ON_TIMEOUT', False),
                db=getattr(self.engine_settings, 'SESSION_REDIS_DB', 0),
                password=self.engine_settings.SESSION_REDIS_PASSWORD
            )
        else:
            self.__redis[self.connection_key] = redis.StrictRedis(
                unix_socket_path=getattr(self.engine_settings, 'SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH', None),
                socket_timeout=getattr(self.engine_settings, 'SESSION_REDIS_SOCKET_TIMEOUT', 0.1),
                retry_on_timeout=getattr(self.engine_settings, 'SESSION_REDIS_RETRY_ON_TIMEOUT', False),
                db=getattr(self.engine_settings, 'SESSION_REDIS_DB', 0),
                password=getattr(self.engine_settings, 'SESSION_REDIS_PASSWORD', None),
            )

        return self.__redis[self.connection_key]

class ACSSessionStore(SessionBase):
    """
    Implements Redis database session store.
    """
    def __init__(self, session_key=None, engine_backend=None):
        super(ACSSessionStore, self).__init__(session_key)
        self.engine_backend = engine_backend
        self.server = RedisServer(session_key, self.engine_backend).get()

    def load(self):
        try:
            session_data = self.server.get(
                self.get_real_stored_key(self._get_or_create_session_key())
            )
            return self.decode(force_unicode(session_data))
        except:
            self._session_key = None
            return {}

    def exists(self, session_key):
        return self.server.exists(self.get_real_stored_key(session_key))

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()

            try:
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            return

    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        if must_create and self.exists(self._get_or_create_session_key()):
            raise CreateError
        data = self.encode(self._get_session(no_load=must_create))
        if redis.VERSION[0] >= 2:
            self.server.setex(
                self.get_real_stored_key(self._get_or_create_session_key()),
                self.get_expiry_age(),
                data
            )
        else:
            self.server.set(
                self.get_real_stored_key(self._get_or_create_session_key()),
                data
            )
            self.server.expire(
                self.get_real_stored_key(self._get_or_create_session_key()),
                self.get_expiry_age()
            )

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            self.server.delete(self.get_real_stored_key(session_key))
        except:
            pass

    def get_real_stored_key(self, session_key):
        """Return the real key name in redis storage
        @return string
        """
        s = self.engine_backend.get('setting', None)
        prefix = s and s.get('SESSION_REDIS_PREFIX', '') or ''
        if not prefix:
            return session_key
        return ':'.join([prefix, session_key])

class SessionStore(SessionBase):
    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)
        self.pool_backends = settings.ACS_SESSION_MULTISESSIONS_POOL

    def load(self):
        for backend in self.pool_backends:
            session = ACSSessionStore(self.session_key, backend)
            if session.exists(self.session_key):
                session_data = session.load()
                return session_data
            else:
                # Try another backend
                continue
        # If the session is not exists, then create it
        self.create()
        return {}

    def exists(self, session_key):
        for backend in self.pool_backends:
            try:
                return ACSSessionStore(self.session_key, backend).exists(session_key)
            except:
                # Try another backend
                continue
        return False

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, *a, **kw):
        backends = self._get_backends(modes=("write",))
        for backend in backends:
            try:
                session = ACSSessionStore(self.session_key, backend)
                if hasattr(self, '_session_cache'):
                    if not hasattr(session, '_session_cache'):
                        session._session_cache = {}
                    session._session_cache.update(self._session_cache)
                session.save(*a, **kw)
                self._session_key = session.session_key
            except:
                # Try another backend
                continue

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        backends = self._get_backends(modes=("write", "delete"))
        for backend in backends:
            try:
                session = ACSSessionStore(session_key, backend)
                session.delete()
            except:
                # Try another backend
                continue

    def _get_backends(self, modes=tuple()):
        """Return available backends by modes
        @return list
        """
        if not modes:
            return list(self.pool_backends)
        else:
            backends = []
            for backend in self.pool_backends:
                if any(map(lambda mode: mode in backend['modes'], modes)):
                    backends.append(backend)

            return backends
