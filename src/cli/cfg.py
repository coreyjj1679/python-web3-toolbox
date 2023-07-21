from typing import Annotated, Optional, List
from rich.console import Console
from rich import print
import src.configs.config as config
import typer

app = typer.Typer()
console = Console()


@app.command(help="list all user configs")
def ls():
    def f(v):
        print(
            f"""config file: {v.file_path.split("/")[-1]}, "key": {v.key}, "alias": {v.alias}"""
        )

    [(f(u)) for u in config.CONFIG_GROUP]


@app.command(help="print keys of configs")
def pk(alias: str):
    cfg_obj = config.get_config(alias)

    if not cfg_obj:
        print(f"Config {alias} not found.")

    keys = cfg_obj.keys()

    print(f"To add new entry for {alias}: ")
    k = " ".join([f"<{j.upper()}>" for j in keys])
    print(f"web3tools config {alias} add {k}")


@app.command()
def table(alias: str, index: Annotated[bool, typer.Option("--index")] = False):
    cfg_obj = config.get_config(alias)

    if not cfg_obj:
        print(f"Config {alias} not found.")
    cfg_obj.table(index)


@app.command()
def add(alias: str, entry: Annotated[Optional[List[str]], typer.Argument()] = None):
    cfg_obj = config.get_config(alias)
    if not cfg_obj:
        print(f"Config {alias} not found.")

    keys = cfg_obj.keys()
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
