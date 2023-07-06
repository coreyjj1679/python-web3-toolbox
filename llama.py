import os.path
from typing import Annotated
import typer
import utils.defillama as dl
import utils.manage_json as mj
import date_helper as dh
import json

app = typer.Typer()

DATA_PATH = 'data/DefiLlama'
PATH = os.path.join(os.path.dirname(__file__), DATA_PATH)

@app.command(help='bookmark protocol')
def add(name: str, llama_slug: str):
    base_path = os.path.dirname(__file__)
    bookmark_llama_protocol_path = os.path.join(base_path, 'configs/bookmark_llama_protocol.json')
    llama_slug = llama_slug.lower()
    new_entry = { "name": name, "llama_slug": llama_slug }
    
    with open(bookmark_llama_protocol_path) as f:
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
        with open(bookmark_llama_protocol_path, mode='w') as f:
            f.write(json.dumps(bookmark_llama_protocol, indent=2))
        print(f"{name} added to bookmark_llama_protocol.json")
    return

@app.command(help='remove bookmark protocol')
def rm(llama_slug: str):
    base_path = os.path.dirname(__file__)
    bookmark_llama_protocol_path = os.path.join(base_path, 'configs/bookmark_llama_protocol.json')

    with open(bookmark_llama_protocol_path) as f:
        bookmark_llama_protocol = json.load(f)

    if not any(llama_slug.lower() in d['llama_slug'] for d in bookmark_llama_protocol):
        print(f"{llama_slug} not found")
        return

    updated_json = [d for d in bookmark_llama_protocol if d['llama_slug'].lower() != llama_slug.lower()]
    with open(bookmark_llama_protocol_path, mode='w') as f:
        f.write(json.dumps(updated_json, indent=2))
    print(f"{llama_slug} removed from bookmark_llama_protocol.json")
    return


@app.command(help='export time series of bookmarked protocols')
def ts(metics: Annotated[str, typer.Option("--metics", "-m", help='eg: TVL')] = 'TVL',
        interval: Annotated[str, typer.Option("--interval", "-i", help='eg: 7d')] = '7d',
        output: Annotated[str, typer.Option("--output", "-o", help='eg: <file name>.csv')] = None,
        ):

    if output is None:
        timestamp = dh.get_current_timestamp()
        output = f"{metics}_{interval}_{timestamp}.json"

    output = mj.get_unique_filename(output, PATH)  # '.' represents the current directory

    print(output)

    return
