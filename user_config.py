import configparser
import json
from typing import TypedDict, List
from web3_instance import Web3Instance, Web3
import os


class WalletConfig:
    address: str
    name: str

    def __init__(self, address, name):
        self.address = Web3.to_checksum_address(address)
        self.name = name


class NetworkConfig(TypedDict):
    chain_id: int
    chain_slug: str
    rpc: str
    native_currency: str
    api: str


class BookMarkConfig(TypedDict):
    name: str
    url: str


class UserConfig:
    chain: str
    endpoint: str
    network_list: List[NetworkConfig]
    wallet_list: List[WalletConfig]
    bookmark_list: List[BookMarkConfig]
    cur_network: NetworkConfig
    web3_instance: Web3Instance

    def __init__(self):
        # Update abs path to ensure we could run the script in anywhere
        base_path = os.path.dirname(__file__)
        config_path = os.path.join(base_path, 'configs/config.ini')
        network_path = os.path.join(base_path, 'configs/networks.json')
        wallet_path = os.path.join(base_path, 'configs/wallet.json')
        bookmark_path = os.path.join(base_path, 'configs/bookmarks.json')

        cfg = configparser.ConfigParser()
        cfg.read(config_path)
        self.chain = cfg['DEFAULT']['default_chain']

        self.network_list = json.loads(open(network_path, "r").read())
        self.wallet_list = [WalletConfig(i['address'], i['name']) for i
                            in json.loads(open(wallet_path, "r").read())]
        self.bookmark_list = json.loads(open(bookmark_path, "r").read())
        self.cur_network = next((item for item in self.network_list if item["chain_slug"] == self.chain), None)
        self.web3_instance = Web3Instance(self.cur_network['rpc'])


config = UserConfig()

