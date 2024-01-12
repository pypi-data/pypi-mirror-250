import json
from typing import Any, Dict, List

json_keys = ["SavedCrosshairProfileData", "MutedWords"]
settings_name = {
    "boolSettings": "EAresBoolSettingName",
    "floatSettings": "EAresFloatSettingName",
    "intSettings": "EAresIntSettingName",
    "stringSettings": "EAresStringSettingName"
}


def get_enum_index(enum: str, settings: list):
    return next((settings.index(x) for x in settings if enum in x["settingEnum"]), -1)


def load_key(enum: str, strSettings: list):
    index = get_enum_index(enum, strSettings)
    if index == -1:
        return
    setting = strSettings[index]
    setting["value"] = json.loads(setting["value"])


def dump_key(enum: str, strSettings: list):
    index = get_enum_index(enum, strSettings)
    if index == -1:
        return
    setting = strSettings[index]
    setting["value"] = json.dumps(setting["value"])


def from_raw_config(config: Dict[str, Any]):
    if not config:
        return {}
    loadify(config)
    magicify(config)
    return config


def to_raw_config(config: Dict[str, Any]):
    demagicify(config)
    dumpify(config)
    return config


def dumpify(config):
    if "stringSettings" not in config:
        return
    strSettings = config["stringSettings"]
    for key in json_keys:
        dump_key(key, strSettings)
    return


def loadify(config):
    if "stringSettings" not in config:
        return
    strSettings = config["stringSettings"]
    for key in json_keys:
        load_key(key, strSettings)
    return


def magicify(config: Dict[str, Any]):
    for value_type in settings_name.keys():
        if value_type not in config:
            continue
        config[value_type] = dictify(config[value_type])


def demagicify(config: Dict[str, Any]):
    for value_type in settings_name.keys():
        if value_type not in config:
            continue
        config[value_type] = undictify(config[value_type], value_type)


def dictify(settings: List[Dict[str, Any]]):
    result = {}
    for setting in settings:
        enum = setting["settingEnum"]
        setting_name = enum.split("::")[1]
        result[setting_name] = setting["value"]
    return result


def undictify(settings: Dict[str, Any], value_type: str):
    result = []
    for setting in settings:
        result.append({
            "settingEnum": f"{settings_name[value_type]}::{setting}",
            "value": settings[setting]
        })
    return result
