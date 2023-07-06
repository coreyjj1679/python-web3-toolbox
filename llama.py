import os.path
from typing import Annotated
import typer
import utils.defillama_API as dl
import utils.manage_json as mj
import date_helper as dh
import json

app = typer.Typer()

BASE_PATH = os.path.dirname(__file__)

DATA_FILE_PATH = 'data/DefiLlama'
DATA_PATH = os.path.join(BASE_PATH, DATA_FILE_PATH)

BOOKMARK_FILE_PATH = 'configs/bookmark_llama_protocol.json'
BOOKMARK_PATH = os.path.join(BASE_PATH, BOOKMARK_FILE_PATH)


@app.command(help='bookmark protocol')
def add(name: str, llama_slug: str):
    
    llama_slug = llama_slug.lower()
    new_entry = { "name": name, "llama_slug": llama_slug }
    
    with open(BOOKMARK_PATH) as f:
        bookmark_llama_protocol = json.load(f)
    
    if any(d['llama_slug'] == llama_slug for d in bookmark_llama_protocol):
        print(f"{name} already exists")
        return

    # check if llama_slug exists
    response = dl.get_protocol(llama_slug)
    
    if response.get('statusCode') == 400:
        print(f"{llama_slug} not found")
    else:
        bookmark_llama_protocol.append(new_entry)
        with open(BOOKMARK_PATH, mode='w') as f:
            f.write(json.dumps(bookmark_llama_protocol, indent=2))
        print(f"{name} added to bookmark_llama_protocol.json")
    return

@app.command(help='remove bookmark protocol')
def rm(llama_slug: str):

    with open(BOOKMARK_PATH) as f:
        bookmark_llama_protocol = json.load(f)

    if not any(llama_slug.lower() in d['llama_slug'] for d in bookmark_llama_protocol):
        print(f"{llama_slug} not found")
        return

    updated_json = [d for d in bookmark_llama_protocol if d['llama_slug'].lower() != llama_slug.lower()]
    with open(BOOKMARK_PATH, mode='w') as f:
        f.write(json.dumps(updated_json, indent=2))
    print(f"{llama_slug} removed from bookmark_llama_protocol.json")
    return


@app.command(help='export time series of bookmarked protocols')
def ts(metics: Annotated[str, typer.Option("--metics", "-m", help='eg: TVL')] = 'TVL',
        interval: Annotated[str, typer.Option("--interval", "-i", help='eg: 1w')] = '1w',
        output: Annotated[str, typer.Option("--output", "-o", help='eg: <file name>.csv')] = None,
        ):

    if output is None:
        timestamp = dh.get_current_timestamp()
        output = f"{metics}_{interval}_{timestamp}.json"

    output = mj.get_unique_filename(output, DATA_PATH)  # '.' represents the current directory

    # get bookmarked protocols
    
    with open(BOOKMARK_PATH) as f:
        bookmark_llama_protocol = json.load(f)
    slug_lists = [d['llama_slug'] for d in bookmark_llama_protocol]
    print(slug_lists)
    
    for slug_list in slug_lists:
        response = dl.get_v2_historicalChainTvl(slug_list)
        print(response)
    
    
    return
