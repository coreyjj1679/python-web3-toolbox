import json
import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from typing import TypedDict


class BlockInfo(TypedDict):
    block_height: int
    timestamp: int


class Web3Instance:
    provider: Web3.HTTPProvider

    def __init__(self, endpoint):
        self.provider = self.connect_web3(endpoint)

    def get_latest_block(self) -> BlockInfo:
        return {
            "block_height": self.provider.eth.get_block("latest")["number"],
            "timestamp": self.provider.eth.get_block("latest")["timestamp"],
        }

    def get_latest_block_custom(self, custom_chain):
        base_path = os.path.dirname(__file__)
        network_path = os.path.join(base_path, "../configs/networks.json")
        networks = json.loads(open(network_path, "r").read())
        custom_network = next(
            item for item in networks if item["chain_slug"] == custom_chain
        )

        if custom_network:
            temp_provider = self.connect_web3(custom_network["rpc"])
            return {
                "block_height": temp_provider.eth.get_block("latest")["number"],
                "timestamp": temp_provider.eth.get_block("latest")["timestamp"],
            }

    def get_balance(self, address, block=None):
        return str(
            Web3.from_wei(
                self.provider.eth.get_balance(
                    address, block_identifier=int(block) if block else "latest"
                ),
                "ether",
            )
        )

    @staticmethod
    def connect_web3(endpoint):
        """
        :param endpoint: RPC endpoint
        :return: web3 connector object
        """
        try:
            provider = Web3(Web3.HTTPProvider(endpoint))
            provider.middleware_onion.inject(geth_poa_middleware, layer=0)
            if provider.is_connected():
                return provider
        except ConnectionError:
            print(f"Failed to connect to {endpoint}")
            return None
