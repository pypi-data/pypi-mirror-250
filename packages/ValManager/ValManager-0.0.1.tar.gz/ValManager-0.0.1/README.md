# ValManager

A python module to manage ValUtils user Valorant configurations and loadouts.

## Features

- Multiple profiles
- Incremental backups for configuration
- Ease of use

## Installation

The preferred method of installation is through `pip` but if you know better use the package manager that you want.

```sh
pip install ValManager
```

## Reference

There is two modules to import `config` and `loadout` they both contain the following methods:

- `upload`: Upload a configuration that is *in-disk* on the ValManager directory
- `download`: Download a configuration to the ValManager directory
- `backup`: Make a backup
- `restore`: Restore a backup of a user

Files:

- `list`: List all the configurations
- `write`: Write `JSON` data to the ValManager directory
- `read`: Read `JSON` data to the ValManager directory
