# python all-in-one web3 toolbox

All-in-one python toolbox for web3 and cli lovers. Aim to build a toolbox to do
everything inside terminal. Getting rugged or scammed without a browser.

## Roadmap

| scope                | command                                                              | progress |
| -------------------- | -------------------------------------------------------------------- | -------- |
| basic                | block, balance, token balance, convert case/date                     | WIP      |
| on-chain data        | TheGraph, Covalent, Snapshot, DefiLlama                              | TBD      |
| on-chain transaction | contract call, contract interaction, encode/decode                   | TBD      |
| misc                 | custom command, switching between wallet, ...                        | TBD      |
| further              | scheduled contract call, integrating flashbot, on-chain stalker, ... | TBD      |

## Setup

1. Clone the repo and install packages.

```bash
$ git clone <THIS_REPO>
$ pip install -r requirement.txt
```

2. Setup `alias`(Optional)

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

3. Update config (Optional)

| file                                     | description                               | default         |
| ---------------------------------------- | ----------------------------------------- | --------------- |
| [config.ini](configs/config.ini)         | default chain for any command             | avax            |
| [networks.json](configs/networks.json)   | chains info for any command               | avax, bnb       |
| [wallet.json](configs/wallet.json)       | list of wallets (no private key required) | dummy addresses |
| [bookmarks.json](configs/bookmarks.json) | list of bookmark                          | dummy bookmarks |

4. Hello World

```bash
# set alias
$ web3tools --help
or
# no
$ python3 main.py --help
```

## Commands

### Basic

1. convert case

command: `web3tools uc/lc/cs <STRING>`

- uc: convert to UPPERCASE
- lc: convert to LOWERCASE
- cs: convert to `check_sum` address

2. `block`

command: `web3tools block -c <CHAIN_SLUG>`
output:

```bash
$ web3tools block
> latest block: 32192657, chain_id: avax, timestamp: 1688527043

$ web3tools block -c bnb
> latest block: 29686211, chain_id: bnb, timestamp: 1688527050
```

3. convert datestr/timestamp

command:

- timestamp to datestr: `web3tools ts-to-date <TIMESTAMP>`
- datestr to timestamp: `web3tools date-to-ts <TIMESTAMP>`

output:

```bash
$ web3tools ts-to-date 1688527347
> 2023-07-05 11:22:27

$ web3tools date-to-ts "2023-07-05 11:22:27"
> 1688527347
```

4. token balance

command: `web3tools balance [-b block-height] [-a addresses]`

output:

```bash
$ web3tools balance
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ index ┃ name                ┃ address                                    ┃ AVAX balance              ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 0     │ Mia Khalifa         │ 0x9f8c163cBA728e99993ABe7495F06c0A3c8Ac8b9 │ 843204.483109813509968818 │
│ 1     │ Henri Léon Lebesgue │ 0xD6216fC19DB775Df9774a6E33526131dA7D19a2c │ 243132.708886098828550571 │
└───────┴─────────────────────┴────────────────────────────────────────────┴───────────────────────────┘

$ web3tools balance -b  25000000
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ index ┃ name                ┃ address                                    ┃ AVAX balance              ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 0     │ Mia Khalifa         │ 0x9f8c163cBA728e99993ABe7495F06c0A3c8Ac8b9 │ 258716.981498374809692885 │
│ 1     │ Henri Léon Lebesgue │ 0xD6216fC19DB775Df9774a6E33526131dA7D19a2c │ 330132.721365885828550571 │
└───────┴─────────────────────┴────────────────────────────────────────────┴───────────────────────────┘


$ BINANCE=0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7
$ RANDOM_GUY=0xFa76DF8588C1033B671d1861E0E5bDe3c26040c7
$ web3tools balance -b 2500000 -a $BINANCE -a $RANDOM_GUY
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ index ┃ address                                    ┃ AVAX balance               ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 0     │ 0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7 │ 6604845.740067908565481545 │
│ 1     │ 0xFa76DF8588C1033B671d1861E0E5bDe3c26040c7 │ 0.41052                    │
└───────┴────────────────────────────────────────────┴────────────────────────────┘
```

4. bookmark

```bash
$ web3tools bookmark 1inch https://1inch.io/
> added 1inch to bookmarks.json

$ web3tools goto 1inch
(Open the url on browser)

$ web3tools remove-bookmark 1inch
> 1inch removed from bookmark.
```

5. fetch contract abi

command: `web3tools get-abi [-a address] [-c chain] [-n file_name] [-o out_dir]`

```
$ web3tools get-abi -a 0xb4315e873dBcf96Ffd0acd8EA43f689D8c20fB30 -c avax -n JoeLBRouter
> abi of JoeLBRouter saved to abis/avax/JoeLBRouter.json
```
