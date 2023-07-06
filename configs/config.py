from typing import List, Dict, Any, TypedDict, Optional
from rich.console import Console
from rich.table import Table
from enum import Enum
import os
import json
import path


class Action(Enum):
    add = 'add'
    rm = 'rm'
    table = 'table'


class BaseConfig:
    file_path: str
    alias: str

    def __init__(self, file_path, alias):
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        self.file_path = file_path
        self.alias = alias


class JsonConfig(BaseConfig):
    config_type: TypedDict
    key: str

    def __init__(self, file_path, alias, config_type, key):
        super().__init__(file_path, alias)
        self.config_type = config_type
        self.key = key

    def load_json(self):
        with open(self.file_path) as config_json:
            return json.load(config_json) or []

    def add(self, entry):
        records = self.load_json()
        if any(entry[self.key].lower() in d[self.key].lower() for d in records):
            print(f'{entry[self.key]} already exists.')
            return

        records.append(entry)
        with open(self.file_path, mode='w') as f:
            f.write(json.dumps(records, indent=2))
        print(f'added {entry[self.key]} to {self.file_path.split("/")[-1]}')

    def rm(self, k):
        records = self.load_json()
        if not any(k.lower() in d[self.key].lower() for d in records):
            print(f'{k} not found.')
            return

        updated_json = [d for d in records if d['name'].lower() != k.lower()]
        with open(self.file_path, mode='w') as f:
            f.write(json.dumps(updated_json, indent=2))
        print(f'{k} removed from bookmark.')

    def table(self, add_index=True):
        console = Console()
        records = self.load_json()
        keys = list(self.config_type.__annotations__.keys())
        if add_index:
            keys.insert(0, 'index')
        table = Table(*keys)
        for i, j in enumerate(records):
            row = [str(k) for k in list(j.values())]

            if add_index:
                row.insert(0, str(i))

            table.add_row(*row)

        console.print(table)


# @TODO: enhance for better folder structure
class WalletDict(TypedDict):
    address: str
    name: str


class LlamaDict(TypedDict):
    name: str
    llama_slug: str


class BookmarkDict(TypedDict):
    name: str
    url: str


class NetworkDict(TypedDict):
    chain_id: str
    chain_slug: str
    rpc: str
    native_currency: str
    api: str


wallet_config = JsonConfig(path.WALLET_PATH, 'wallet', WalletDict, 'name')
llama_config = JsonConfig(path.LLAMA_PATH, 'llama', LlamaDict, 'llama_slug')
bookmark_config = JsonConfig(path.BOOKMARK_PATH, 'bookmark', BookmarkDict, 'name')
network_config = JsonConfig(path.NETWORK_PATH, 'chain', NetworkDict, 'chain_slug')

CONFIG_GROUP = (wallet_config, llama_config, bookmark_config, network_config)


def get_config(alias: str):
    return next((i for i in CONFIG_GROUP if i.alias.lower() == alias.lower()), None)
