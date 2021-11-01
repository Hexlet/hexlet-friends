from typing import Optional

# noinspection PyUnresolvedReferences
from .main import *

DEBUG: bool = True
SECURE_PROXY_SSL_HEADER: Optional[Tuple[str, str]] = None
SECURE_SSL_REDIRECT: bool = False

ALLOWED_HOSTS: List[str] = [
    'localhost',
    '127.0.0.1',
]

# Logging setup
# region
logging.basicConfig(
    level=logging.DEBUG,
    filename=BASE_DIR / 'logs' / 'events.log',
    filemode='w',
    format='{asctime} - {levelname} - {message}',
    datefmt='%H:%M:%S',
    style='{',
)
# endregion

DATABASES: Dict[str, Dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

AUTH_PASSWORD_VALIDATORS: List[Dict[str, Tuple[str, str]]] = [
]
