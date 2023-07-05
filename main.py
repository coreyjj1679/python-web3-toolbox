import os.path
import typer
from typing_extensions import Annotated
from typing import List
from rich import print
from rich.console import Console
from rich.table import Table
from user_config import UserConfig
from web3 import Web3
import utils.explorer as eh
import date_helper as dh
import json

config = UserConfig()
app = typer.Typer()
console = Console()


@app.command(help='Get current block height of the default / specifc chain.')
def block(chain: Annotated[str, typer.Option("--chain", "-c", help='custom chain slug. e.g. "bnb"')] = None) -> None:
    if chain:
        block_info = config.web3_instance.get_latest_block_custom(chain)
    else:
        block_info = config.web3_instance.get_latest_block()
    print(f"latest block: {block_info['block_height']}, chain_id: {chain or config.cur_network['chain_slug']}, "
          f"timestamp: {block_info['timestamp']}")


@app.command(help='Get current native balance. default: wallets inside wallet.json')
def balance(block_height: Annotated[int, typer.Option("--block", "-b",
                                                      help='custom_block_height chain slug. e.g. "bnb"')] = None,
            addresses: Annotated[List[str], typer.Option("--address", "-a",
                                                         help='custom addresses')] = None
            ):
    if addresses:
        table = Table("index", "address", f"{config.cur_network['native_currency']} balance")
        for i, j in enumerate(addresses):
            cs_address = Web3.to_checksum_address(j)
            table.add_row(str(i), cs_address, config.web3_instance.get_balance(cs_address, block_height))

    else:
        table = Table("index", "name", "address", f"{config.cur_network['native_currency']} balance")
        for i, wallet in enumerate(config.wallet_list):
            table.add_row(str(i), wallet.name, wallet.address, config.web3_instance.get_balance(wallet.address,
                                                                                                block_height))
    console.print(table)


@app.command(help="Simply convert to lower case")
def lc(x: str):
    print(x.lower())


@app.command(help="Simply convert to UPPER case")
def uc(x: str):
    print(x.upper())


@app.command(help="Simply convert to checksum address")
def cs(x: str):
    try:
        print(Web3.to_checksum_address(x))
    except ValueError:
        console.print_exception(show_locals=True)


@app.command(help="convert timestamp to date string in local timezone")
def ts_to_date(timestamp: int):
    print(dh.timestamp_to_datestr(timestamp))


@app.command(help="convert date string to timestamp in local timezone")
def date_to_ts(date_str: str):
    print(dh.datestr_to_timestamp(date_str))


@app.command(help='open your favourite dapp on browser')
def goto(name: str):
    togo = next(item for item in config.bookmark_list if item["name"].lower() == name.lower())
    typer.launch(togo['url'])


@app.command(help="Add your favourite dapp to bookmark")
def bookmark(name: str, url: str):
    base_path = os.path.dirname(__file__)
    bookmark_path = os.path.join(base_path, 'configs/bookmarks.json')
    new_entry = {"name": name, "url": url}

    with open(bookmark_path) as old_json:
        bookmarks = json.load(old_json)

    if any(name in d['name'].lower() for d in bookmarks):
        print(f'{name} already exists.')
        return

    bookmarks.append(new_entry)
    with open(bookmark_path, mode='w') as f:
        f.write(json.dumps(bookmarks, indent=2))
    print(f'added {name} to bookmarks.json')


@app.command(help='remove bookmark from the list')
def remove_bookmark(name: str):
    base_path = os.path.dirname(__file__)
    bookmark_path = os.path.join(base_path, 'configs/bookmarks.json')

    with open(bookmark_path) as bookmark_json:
        bookmarks = json.load(bookmark_json)

    if not any(name in d['name'].lower() for d in bookmarks):
        print(f'{name} not found.')
        return

    updated_json = [d for d in bookmarks if d['name'] != name]
    with open(bookmark_path, mode='w') as f:
        f.write(json.dumps(updated_json, indent=2))
    print(f'{name} removed from bookmark.')


@app.command(help='get contract abi from any blockchain explorer')
def get_abi(address: Annotated[str, typer.Option("--address", "-a",
                                                 help='contract address')] = None,
            chain: Annotated[str, typer.Option("--chain", "-c",
                                               help='custom chain_slug')] = None,
            output_dir: Annotated[str, typer.Option("--output", "-o",
                                                    help='destination of the abi')] = 'abis',
            fname: Annotated[str, typer.Option("--name", "-n",
                                               help='file name of the json')] = None,
            ):
    abi = config.cur_network['api']
    if chain:
        custom_chain = next((item for item in config.network_list if item["chain_slug"] == chain), None)
        if not custom_chain:
            print(f'{chain} not found inside networks.json')
            print(f'supported networks: {[i["chain_slug"] for i in config.network_list]}')
            return
        else:
            abi = custom_chain['api']

    abi = eh.get_contract_abi(address, abi)

    base_path = os.path.dirname(__file__)
    dest = os.path.join(base_path, f'{output_dir}/{chain or config.cur_network["chain_slug"]}')
    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)

    file_name = f'{fname or address}'
    file_dest = f'{dest}/{file_name}.json'
    if os.path.exists(file_dest):
        print('abi already exists')
        return

    with open(file_dest, mode='w') as f:
        f.write(json.dumps(json.loads(abi), indent=2))
    print(f'abi of {file_name} saved to {file_dest}')


if __name__ == "__main__":
    app()
