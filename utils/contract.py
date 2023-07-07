from web3 import Web3
from web3.exceptions import ExtraDataLengthError
from web3.middleware import geth_poa_middleware
import json


def abi_loader(file_path):
    """
    :param file_path: file path of json file
    :return: json object of contract abi
    """
    with open(file_path) as f:
        return json.load(f)


def contract_loader(provider, contract_address, contract_abi):
    """
    :param provider: web3 provider object
    :param contract_address: contract address
    :param contract_abi: contract abi
    :return: contract object of contract abi
    """
    _address = Web3.to_checksum_address(contract_address)
    return provider.eth.contract(address=_address, abi=contract_abi)


def get_contract_instance(provider, contract_address, file_path):
    """
    :param provider: web3 provider object
    :param contract_address: contract address
    :param file_path: file path of contract abi
    :return: contract abi object, contract instance
    """
    contract_abi = abi_loader(file_path)
    contract_instance = contract_loader(provider, contract_address, contract_abi)

    return {"abi": contract_abi, "instance": contract_instance}


def check_contract_created(provider, contract_address, block=None):
    """
    check if a contract was created as specific block height
    :param provider: web3 provider object
    :param contract_address: contract address
    :param block: block height. empty to check lastest block height
    :return: true if contract created
    """
    if block:
        return provider.eth.get_code(contract_address, block) != b""
    else:
        return provider.eth.get_code(contract_address) != b""


def get_code(provider, contract_address, block):
    """
    helper function to get contract creation block by bin search
    """
    current_block = check_contract_created(provider, contract_address, block)
    prev_block = not check_contract_created(provider, contract_address, block - 1)

    if current_block and prev_block:
        return 0
    if not current_block:
        return 1
    if current_block and not prev_block:
        return -1


def binary_search_creation_block(provider, contract_address, start, end):
    """
    helper function to get contract creation block by bin search
    """
    if end >= start:
        mid = (end + start) // 2
        idx = get_code(provider, contract_address, mid)
        if idx == 0:
            return mid
        elif idx == -1:
            return binary_search_creation_block(
                provider, contract_address, start, mid - 1
            )
        elif idx == 1:
            return binary_search_creation_block(
                provider, contract_address, mid + 1, end
            )
    else:
        return -1


def get_contract_creation_block(provider, contract_address):
    start_block = 0
    end_block = provider.eth.get_block("latest")["number"]
    contract_address = provider.to_checksum_address(contract_address)
    return binary_search_creation_block(
        provider, contract_address, start_block, end_block
    )
