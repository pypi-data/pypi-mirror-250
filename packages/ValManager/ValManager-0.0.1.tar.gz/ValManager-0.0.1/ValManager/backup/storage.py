from pathlib import Path

from ValStorage import get_settings, save_to_drive

from ..storage import create_path, json_read, json_write, settingsPath
from ..structs import BackupFile, BackupInfo

backupPath = settingsPath / "backup"


def backup_write(data, file, sub):
    create_path(settingsPath / "backup" / sub)
    json_write(data, settingsPath / "backup" / sub / file)


def backup_read(file, sub):
    return json_read(settingsPath / "backup" / sub / file)


def save_backup(file: BackupFile, path: Path):
    save_to_drive(file.to_json(), path)


def get_info(sub: str):
    path = backupPath / sub / "info.json"
    path.parent.mkdir(exist_ok=True)
    return get_settings(BackupInfo, path)


def save_info(sub, info):
    backup_write(info.to_dict(), "info.json", sub)
