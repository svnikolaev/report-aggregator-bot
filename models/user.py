import logging
from typing import Optional, Union

from utils.file_handler import read_data_from_file, write_data_to_file

logger = logging.getLogger(__name__)

USERS_FILE = 'users.json'
# levels:
ADMIN = 'admin'
REPORTER = 'reporter'
PENDING = 'pending'
BLOCKED = 'blocked'


def read_users() -> dict:
    try:
        users = read_data_from_file(USERS_FILE)
    except FileNotFoundError:
        users = {}
    return users or {}


def save_users(users: dict):
    write_data_to_file(users, USERS_FILE)


def get_users(level: Optional[str] = None) -> dict:
    users = read_users()
    if level:
        return {
            user_id: user
            for user_id, user in users.items() if user['level'] == level
        }
    return users


def add_user(user: dict, level: Optional[str] = PENDING):
    users = get_users()
    user_id = str(user['id'])
    users[user_id] = user
    users[user_id].update(level=level)
    write_data_to_file(users, USERS_FILE)


def get_user_level(user_id: Union[str, int]) -> str:
    if isinstance(user_id, int):
        user_id = str(user_id)
    users = get_users()
    user = users.get(user_id)
    user_level = user.get('level') if user is not None else ''
    return user_level


def is_admin(user_id: Union[str, int]) -> bool:
    return get_user_level(user_id) in [ADMIN]


def is_reporter(user_id: Union[str, int]) -> bool:
    return get_user_level(user_id) in [ADMIN, REPORTER]


def set_user_level(user_id: Union[str, int], level: str):
    if isinstance(user_id, int):
        user_id = str(user_id)
    users = get_users()
    logger.info(f'if user_id in users.keys(): {user_id in users.keys()}')
    if user_id in users.keys():
        users[user_id].update(level=level)
    save_users(users)
