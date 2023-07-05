# python all-in-one web3 toolbox

All-in-one python toolbox for web3 and cli lovers. Aim to build a toolbox to do
everything inside terminal. Getting rugged or scammed without a browser.

## Environment

- python 3.11
- macOS Monterey 12.5.1

## Setup

- Clone the repo and install packages.

  ```bash
  $ git clone <THIS_REPO>
  $ pip install -r requirement.txt
  ```

- Setup `alias`(Optional)

  ```bash
  # for zsh users
  $ chmod u+x setup.zsh
  $ ./setup.zsh
  $ source ~./zshrc

  # for bash users
  $ chmod u+x setup.sh
  $ ./setup.sh
  $ source ~./bashrc
  ```

- Run
  ```bash
  # set alias
  $ web3tools --help
  or
  # no
  $ python3 main.py --help
  ```

## Commands

### General

- get list of command groups

  ```bash
  $ web3tools --help
  or
  $ python3 main.py --help
  ```

- get list of sub-commands
  ```bash
  $ web3tools <GROUP> --help
  or
  $ python3 main.py <GROUP> --help
  ```

### Basic

| command                                    | description                                         | remark                             |
| :----------------------------------------- | :-------------------------------------------------- | :--------------------------------- |
| `web3tools basic lc <STRING>`              | convert input str to lower case                     |                                    |
| `web3tools basic uc <STRING>`              | convert input str to UPPER case                     |                                    |
| `web3tools basic cs <STRING>`              | convert input str to checksum address               |                                    |
| `web3tools basic date-to-ts <DATE_STRING>` | convert date string to timestamp in local timezones | input format: YYYY-MM-DD HH:MM:SS  |
| `web3tools basic ts-to-date <TIMESTAMP>`   | convert timestamp to date string in local timezone  | output format: YYYY-MM-DD HH:MM:SS |

### w3

| command                                                              | description                                              | remark                                                                   |
| :------------------------------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------- |
| `web3tools w3 block [-c chain]`                                      | Get current block height of the default / specifc chain. |                                                                          |
| `web3tools w3 creation <ADDRESS>`                                    | Get creation block of a contract                         | may takes 10s for the binary search                                      |
| `web3tools w3 balance [-b block] [-a address]`                       | get native balance.                                      | default: wallets inside wallet.json, latest block                        |
| `web3tools w3 abi [-a address] [-c chain] [-o output] [-f filename]` | get contract abi from any blockchain explorer            | update [`configs/networks.json`](configs/networks.json) for other chains |

### token

| command                                              | description                   | remark                                                                                                                          |
| :--------------------------------------------------- | :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| `web3tools token add <ADDRESS> <NAME>`               | bookmark your favourite token |                                                                                                                                 |
| `web3tools token rm <NAME>`                          | remove token from bookmark    |                                                                                                                                 |
| `web3tools token [-t token] [-a address] [-b block]` | get erc20 balance             | just input the name for bookmarked token, e.g. ` web3tools token balance -t usdt -a 0xf888d1a8c69dff6cbf043ec40a0f4b78181ec0bb` |

### bookmark

| command                                   | description                         | remark |
| :---------------------------------------- | :---------------------------------- | :----- |
| `web3tools bookmark add <ADDRESS> <NAME>` | bookmark your favourite protocol    |        |
| `web3tools bookmark rm <NAME>`            | remove protocol from bookmark       |        |
| `web3tools bookmark goto <NAME>`          | open your favourite dapp on browser |        |

## WIPs

### Covalent

| command                                                                  | description                                                   | remark |
| :----------------------------------------------------------------------- | :------------------------------------------------------------ | :----- |
| `web3tools covalent log [-c chain] [-a address] [-t topic] [-o output]`  | fetch all event logs of a smart contract                      |        |
| `web3tools covalent ul [-c chain] [-a address] [-t topic] [-o output]` ` | fetch list of unique address interacted with a smart contract |        |
| `web3tools covalent token_holder [-c chain] [-a address] [-b block]`     | get number of token holder of any ERC20                       |        |

### DefiLlama

| command                                                    | description                                  | remark                                                     |
| :--------------------------------------------------------- | :------------------------------------------- | :--------------------------------------------------------- |
| `web3tools llama add <NAME> <LLAMA_SLUG>`                  | bookmark protocol                            |                                                            |
| `web3tools llama rm <LLAMA_SLUG>`                          | remove bookmark                              |                                                            |
| `web3tools llama ts [-m metics] [-i interval] [-o output]` | export time series of bookmarked protocols   | e.g. `web3tools llama ts -m TVL -i 7d -o tvl_7d.json`      |
| `web3tools llama top [-m metrics] [-n number]`             | display top `n` protocols depends on metrics | e.g. `web3tools llama -m volumne -n 20 top_20_volumn.json` |

### Snapshot (TBD)

- get DAO, proposals or voting data

### Governance(TBD)

- get voting data from `GovernorBravo` or any similar contracts.

### Coingecko/CMC (TBD)

-

### TheGraph (TBD)

-

### Contributing

- Check [Dashboard](https://github.com/users/ruggedev/projects/2)
- PR
