from ValStorage import *


def set_path():
    global settingsPath
    utilsPath = utils_path()
    settingsPath = utilsPath / "config"
    create_path(settingsPath)


set_path()
