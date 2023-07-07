import os

base_path = os.path.dirname(__file__)


def get_abs_path(path: str):
    return os.path.join(base_path, path)


# [User Config]
CONFIG_PATH = get_abs_path("configs/config.ini")
NETWORK_PATH = get_abs_path("configs/networks.json")
WALLET_PATH = get_abs_path("configs/wallet.json")
BOOKMARK_PATH = get_abs_path("configs/bookmarks.json")
TOKENS_DIR = get_abs_path("configs/tokens/")

# [abis]
ERC20_ABI = get_abs_path("abis/common/ERC20.json")
GB_ABI = get_abs_path("abis/common/GovernorBravo.json")
