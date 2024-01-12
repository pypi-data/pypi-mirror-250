from pathlib import Path
from typing import Union

from ValLib.api import get_extra_auth, get_load_out, get_region, set_load_out
from ValLib.structs import ExtraAuth
from ValVault.terminal import User, get_auth

from .storage import *
from .structs import Action


def action(action: Action, user: User, cfg):
    auth = get_auth(user)
    loadAuth = get_extra_auth(auth, user.username)

    if action == "dump":
        download(cfg, loadAuth)
    elif action == "import":
        backup(loadAuth)
        upload(cfg, loadAuth)
    elif action == "restore":
        restore(loadAuth)
    elif action == "backup":
        backup(loadAuth)


def write(data, file: Union[str, Path], sub: str):
    create_path(settingsPath / "loadouts" / sub)
    json_write(data, settingsPath / "loadouts" / sub / file)


def read(file: Union[str, Path], sub: str):
    return json_read(settingsPath / "loadouts" / sub / file)


def list(sub: str):
    return list_dir(settingsPath / "loadouts" / sub)


def upload(cfg: str, loadAuth: ExtraAuth):
    data = read(cfg, loadAuth.username)
    req = set_load_out(loadAuth, data)
    print(f'Loadout status code: {req.status_code}')


def download(cfg: str, loadAuth: ExtraAuth):
    data = get_load_out(loadAuth)
    write(data, cfg, loadAuth.username)


def backup_file(loadAuth: ExtraAuth):
    file_name = f"{loadAuth.username}.json"
    backup_folder = settingsPath / "backup" / "_loadouts"
    return backup_folder / file_name


def backup(loadAuth: ExtraAuth):
    data = get_load_out(loadAuth)
    backup_path = backup_file(loadAuth)
    json_write(data, backup_path)


def restore(loadAuth: ExtraAuth):
    backup_path = backup_file(loadAuth)
    data = json_read(backup_path)
    set_load_out(loadAuth, data)

__all__ = ["write", "read", "list", "upload", "download", "backup", "restore"]
