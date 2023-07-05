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


@app.command(help='get contract abi from any blockchain explorer')
def abi(address: Annotated[str, typer.Option("--address", "-a",
                                             help='contract address')] = None,
        chain: Annotated[str, typer.Option("--chain", "-c",
                                           help='custom chain_slug')] = None,
        output_dir: Annotated[str, typer.Option("--output", "-o",
                                                help='destination of the abi')] = 'abis',
        fname: Annotated[str, typer.Option("--name", "-n",
                                           help='file name of the json')] = None,
        ):
    _abi = config.cur_network['api']
    if chain:
        custom_chain = next((item for item in config.network_list if item["chain_slug"] == chain), None)
        if not custom_chain:
            print(f'{chain} not found inside networks.json')
            print(f'supported networks: {[i["chain_slug"] for i in config.network_list]}')
            return
        else:
            _abi = custom_chain['api']

    _abi = eh.get_contract_abi(address, _abi)

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
