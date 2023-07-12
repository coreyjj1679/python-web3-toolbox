import typer
import os
import json
import src.constants.path as path
from src.cli.user_config import config
from src.core.erc_instance import ERC20
from typing_extensions import Annotated

app = typer.Typer()


@app.command(help="bookmark your token")
def add(addr: str, name: str):
    token_dir = path.TOKENS_DIR
    token_path = os.path.join(token_dir, f'{config.cur_network["chain_slug"]}.json')
    new_entry = {"name": name, "address": addr}

    if not os.path.exists(token_dir):
        os.makedirs(token_dir, exist_ok=True)

    if os.path.exists(token_path):
        with open(token_path) as token_json:
            tokens = json.load(token_json)
    else:
        tokens = []

    if any(name.lower() in d["name"].lower() for d in tokens):
        print(f"{name} already exists.")
        return

    tokens.append(new_entry)
    with open(token_path, mode="w") as f:
        f.write(json.dumps(tokens, indent=2))
    print(f"added {name} to bookmarks.json")


@app.command(help="remove token from bookmark")
def rm(name: str):
    token_dir = path.TOKENS_DIR
    token_path = os.path.join(token_dir, f'{config.cur_network["chain_slug"]}.json')

    with open(token_path) as token_json:
        tokens = json.load(token_json)

    if not any(name.lower() in d["name"].lower() for d in tokens):
        print(f"{name} not found.")
        return

    updated_json = [d for d in tokens if d["name"].lower() != name.lower()]
    with open(token_path, mode="w") as f:
        f.write(json.dumps(updated_json, indent=2))
    print(f"{name} removed from bookmark.")


@app.command(help="check ERC20 token balance")
def balance(
    token: Annotated[str, typer.Option("--token", "-t", help="token address/name")],
    address: Annotated[
        str, typer.Option("--address", "-a", help="user address")
    ] = None,
    block: Annotated[
        int,
        typer.Option("--block", "-d", help="hist. balance at specific block height"),
    ] = None,
) -> None:
    token_dir = path.TOKENS_DIR
    token_path = os.path.join(token_dir, f'{config.cur_network["chain_slug"]}.json')
    if not os.path.exists(token_path):
        print(
            "bookmarked token not found. use balance add <ADDRESS> <NAME> to bookmark token first"
        )
        return

    with open(token_path) as token_json:
        tokens = json.load(token_json)
    bookmarked = next(
        (
            item
            for item in tokens
            if item["name"].lower() == token.lower() or item["address"] == token.lower()
        ),
        None,
    )

    if bookmarked:
        token = ERC20(bookmarked["address"])
    else:
        token = ERC20(token)
    user_balance = token.balance_of(address, True, block)
    print(f"{address}: {user_balance} {token.symbol}")
