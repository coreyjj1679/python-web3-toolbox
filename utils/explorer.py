import utils.rq as rq


def get_contract_abi(contract_address: str, api: str):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }
    endpoint = f"{api}api/?module=contract&action=getabi&address={contract_address}"
    resp = rq.get(endpoint, headers, "etherscan")
    return resp["result"]
