from dataclasses import dataclass, field
from time import time
from typing import Any, Dict, List, Literal

from dataclasses_json import DataClassJsonMixin


@dataclass
class BackupData(DataClassJsonMixin):
    file: int = 0
    patchIndex: int = 0
    timestamp: float = field(default_factory=time)


@dataclass
class BackupInfo(DataClassJsonMixin):
    backupNumber: int = 0
    lastBackup: float = 0
    backups: List[BackupData] = field(default_factory=list)
    user: str = ""


@dataclass
class BackupFile(DataClassJsonMixin):
    creationDate: float = 0
    settings: Dict[str, Any] = field(default_factory=dict)
    patches: List[Any] = field(default_factory=list)

Action = Literal["dump", "import", "restore", "backup"]
