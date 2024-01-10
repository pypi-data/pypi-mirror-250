import logging
import uuid

from models.models import Session

logger = logging.getLogger(__name__)

"""
The session manager is responsible for persisting and retrieving sessions.

TODO - use a database instead of a cache map in memory!

"""
class SessionMgr:

    def __init__(self):
        self._cache = {}

    def _cache_id(self, app_name: str, session_id: str) -> str:
        return f"{app_name}>{session_id}"

    def get_session(self, app_name: str, session_id: str) -> Session:
        cache_id = self._cache_id(app_name, session_id)
        if cache_id in self._cache:
            logger.debug(f"Found session for app_name={app_name}, session_id={session_id}")
            return self._cache[cache_id]
        else:
            logger.info(f"No session found for app_name={app_name}, session_id={session_id}")
            raise KeyError(f"No session found for app_name={app_name}, session_id={session_id}")

    def get_or_create_session(self, app_name: str, session_id: str) -> Session:
        # No valid session id provided, lets create one!
        if not session_id:
            session_id = uuid.uuid4()
            logger.info(f"No session id provided, allocating session id {session_id}")

        cache_id = self._cache_id(app_name, session_id)

        if cache_id in self._cache:
            logger.debug(f"Found session for app_name={app_name}, session_id={session_id}")
            return self._cache[cache_id]
        else:
            logger.info(f"No session found for app_name={app_name}, session_id={session_id}, creating new session")
            session = Session(session_id=session_id, app_name=app_name, events=[], app_metadata={})
            self._cache[cache_id] = session
            return session
