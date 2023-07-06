from typing import Annotated, Optional, List

import typer
import configs.config as config
from rich.console import Console
from rich import print
from enum import Enum

app = typer.Typer()
console = Console()


@app.command(help="list all user configs")
def ls():
    def f(v): print(f"""config file: {v.file_path.split("/")[-1]}, "key": {v.key}, "alias": {v.alias}""")

    [(f(u)) for u in config.CONFIG_GROUP]


@app.command()
def table(alias: str, index=False):
    cfg_obj = config.get_config(alias)

    if not cfg_obj:
        print(f"Config {alias} not found.")
    cfg_obj.table()


@app.command()
def add(alias: str, entry: Annotated[Optional[List[str]], typer.Argument()] = None):
    cfg_obj = config.get_config(alias)
    if not cfg_obj:
        print(f"Config {alias} not found.")

    keys = list(cfg_obj.config_type.__annotations__.keys())
    if len(entry) != len(keys):
        print("Got unexpected arguments")
        print(f"Keys: {keys}")
        return

    new_entry = cfg_obj.config_type(dict(zip(keys, entry)))
    cfg_obj.add(new_entry)


@app.command()
def rm(alias: str, k):
    cfg_obj = config.get_config(alias)
    if not cfg_obj:
        print(f"Config {alias} not found.")

    cfg_obj.rm(k)
