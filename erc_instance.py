import utils.contract as ch
import path
from web3 import contract, Web3
from user_config import config


class ERC20:
    contract: contract.Contract
    name: str
    symbol: str
    decimals: int

    def __init__(self, address):
        self.contract = ch.get_contract_instance(
            config.web3_instance.provider, Web3.to_checksum_address(address),
            path.ERC20_ABI)['instance']
        self.name = self.contract.functions.name().call()
        self.symbol = self.contract.functions.symbol().call()
        self.decimals = self.contract.functions.decimals().call()

    def __str__(self):
        return str(
            {"address": self.contract.address,
             "name": self.name,
             "symbol": self.symbol,
             "decimals": self.decimals}
        )

    def to_wei(self, v):
        return v * (10 ** self.decimals)

    def from_wei(self, v):
        return v / (10 ** self.decimals)

    def balance_of(self, user, convert=True, block=None):
        raw_b = self.contract.functions.balanceOf(Web3.to_checksum_address(user)).call(
            block_identifier=int(block) if block else 'latest')
        return self.from_wei(raw_b) if convert else raw_b
