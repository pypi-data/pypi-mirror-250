from pathlib import Path
from typing import Union

from ValLib import Auth, User
from ValLib.api import get_preference, set_preference
from ValVault.terminal import get_auth

from .storage import *
from .backup import backup_settings, get_backup
from .structs import Action


def action(action: Action, user: User, cfg):
    auth: Auth = get_auth(user)
    if action == "dump":
        download(cfg, auth)
    elif action == "import":
        backup(user, auth)
        upload(cfg, auth)
    elif action == "restore":
        restore(user, auth, cfg)
    elif action == "backup":
        backup(user, auth)


def write(data, file: Union[str, Path]):
    json_write(data, settingsPath / "configs" / file)


def read(file: Union[str, Path]):
    return json_read(settingsPath / "configs" / file)


def list():
    files = list_dir(settingsPath / "configs")
    files.sort(key=lambda f: "bck.json" in f)
    return files


def upload(cfg: str, auth: Auth):
    data = read(cfg)
    req = set_preference(auth, data)
    print(f'Config status code: {req.status_code}')


def download(cfg: str, auth: Auth):
    data = get_preference(auth)
    write(data, cfg)


def backup(user: User, auth: Auth):
    data = get_preference(auth)
    backup_settings(user.username, data)


def restore(user: User, auth: Auth, cfg):
    data = get_backup(user.username, cfg)
    set_preference(auth, data)


__all__ = ["write", "read", "list", "upload", "download", "backup", "restore"]
