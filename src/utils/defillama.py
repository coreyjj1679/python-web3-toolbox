import requests as rq

# https://defillama.com/docs/api
URL = "https://api.llama.fi"


def get_protocols():
    # List all protocols on defillama along with their tvl
    path = "/protocols"
    return rq.get(URL + path).json()


def get_protocol(slug):
    # Get historical TVL of a protocol and breakdownws by token and chain
    path = f"/protocol/{slug}"
    return rq.get(URL + path).json()


def get_v2_chains():
    # Get current TVL of all chains
    path = "/v2/chains"
    return rq.get(URL + path).json()
