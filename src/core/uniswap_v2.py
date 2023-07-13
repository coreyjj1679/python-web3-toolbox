from web3 import contract, Web3
from src.constants import path
from src.utils import contract as ch
from src.cli.user_config import config
from typing import List

class UniswapV2:
    router: contract.Contract
    factory: contract.Contract
    name: str

    def __init__(self, router_address, name='UniswapV2-like'):
        self.name = name
        self.router = ch.get_contract_instance(
            config.web3_instance.provider,
            Web3.to_checksum_address(router_address),
            path.ROUTER_V2_ABI,
        )["instance"]

        factory_address = self.router.functions.factory().call()
        self.factory = ch.get_contract_instance(
            config.web3_instance.provider,
            Web3.to_checksum_address(factory_address),
            path.FACTORY_V2_ABI,
        )["instance"]

    # [READ]
    def get_pair(self, token_0: str, token_1: str):
        return self.factory.functions.getPair(
            Web3.to_checksum_address(token_0),
            Web3.to_checksum_address(token_1)
        ).call()

    def quote(self, token_path: List[str]):
        pass

    # [WRITE]
    def wrap(self, amount):
        pass

    def unwrap(self, amount):
        pass

    def create_pair(self):
        pass

    def swap(self, token_path: List[str], amountIn: float):
        pass
