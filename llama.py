import os.path
from typing import Annotated
import typer
import utils.defillama as dl
import date_helper as dh
import json
import time
import sys

app = typer.Typer()

BASE_PATH = os.path.dirname(__file__)

DATA_FILE_PATH = "data/DefiLlama"
DATA_PATH = os.path.join(BASE_PATH, DATA_FILE_PATH)

BOOKMARK_FILE_PATH = "configs/llama_protocol_bookmark.json"
BOOKMARK_PATH = os.path.join(BASE_PATH, BOOKMARK_FILE_PATH)

PROTOCOLS_LISTS_PATH = "configs/llama_protocol_lists.json"
PROTOCOLS_LISTS = os.path.join(BASE_PATH, PROTOCOLS_LISTS_PATH)


ITEMS_PER_PAGE = 50


def get_update():
    print("Updating all protocols data...")
    response = dl.get_protocols()

    # Add timestamp
    timestamp = int(time.time())

    # Build the dictionary with the time and the response data
    data = {"time": timestamp, "data": response}

    # Write the dictionary into the file
    with open(PROTOCOLS_LISTS, mode="w") as f:
        json.dump(data, f)

    print("Done")


@app.command(help="update protocols data")
def update(args: str = typer.Argument(None)):
    with open(PROTOCOLS_LISTS, mode="r") as f:
        existing_data = json.load(f)

    print(f'Your data import from {time.ctime(existing_data["time"])}')

    if typer.confirm("Do you want to update list?"):
        get_update()
    else:
        print("Data update cancelled.")


def search(query=None):
    with open(PROTOCOLS_LISTS, "r") as f:
        data = json.load(f)
    slugs = [protocol["slug"] for protocol in data["data"]]
    if query:
        slugs = [slug for slug in slugs if query.lower() in slug.lower()]
    slugs.sort()
    return slugs


def paginate(items, page):
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    return items[start:end]


@app.command(help="Search protocols or list all")
def lists(query: str = typer.Option(None, help="Optional search query")):
    with open(PROTOCOLS_LISTS, "r") as f:
        data = json.load(f)

    last_update_time = dh.timestamp_to_datestr(data["time"])
    print(f"Data was last updated at {last_update_time}.")

    # Ask the user if they want to update the data
    update = input("Do you want to update the data? (y/n): ")
    if update.lower() == "y":
        get_update()

    matches = search(query)
    page = 1
    while True:
        page_items = paginate(matches, page)
        if not page_items:
            break

        for item in page_items:
            print(item)
        next_page = input(
            "\nPress Enter to see the next page, 'q' to quit, 's' to search: "
        )

        if next_page.lower() == "q":
            break
        elif next_page.lower() == "s":
            query = input("Enter your search query: ")
            matches = search(query)
            page = 1
        else:
            page += 1
    sys.exit()


@app.command(help="bookmark protocol")
def add(name: str, llama_slug: str):
    llama_slug = llama_slug.lower()
    new_entry = {"name": name, "llama_slug": llama_slug}

    with open(BOOKMARK_PATH) as f:
        bookmark_llama_protocol = json.load(f)

    if any(d["llama_slug"] == llama_slug for d in bookmark_llama_protocol):
        print(f"{name} already exists")
        return

    # check if llama_slug exists
    response = dl.get_protocol(llama_slug)
    if response.get('statusCode') == 400:
        print(f"{llama_slug} not found")
    else:
        bookmark_llama_protocol.append(new_entry)
        with open(BOOKMARK_PATH, mode="w") as f:
            f.write(json.dumps(bookmark_llama_protocol, indent=2))
        print(f"{name} added to bookmark_llama_protocol.json")
    return


@app.command(help="remove bookmark protocol")
def rm(llama_slug: str):
    with open(BOOKMARK_PATH) as f:
        bookmark_llama_protocol = json.load(f)

    if not any(llama_slug.lower() in d["llama_slug"] for d in bookmark_llama_protocol):
        print(f"{llama_slug} not found")
        return

    updated_json = [
        d
        for d in bookmark_llama_protocol
        if d["llama_slug"].lower() != llama_slug.lower()
    ]
    with open(BOOKMARK_PATH, mode="w") as f:
        f.write(json.dumps(updated_json, indent=2))
    print(f"{llama_slug} removed from bookmark_llama_protocol.json")
    return
