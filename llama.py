import os.path
from typing import Annotated
import typer
import utils.defillama as dl
import path as p
import date_helper as dh
import json
import time
import sys

app = typer.Typer()

ITEMS_PER_PAGE = 50


def get_update():
    print("Updating all protocols data...")
    response = dl.get_protocols()

    # Add timestamp
    timestamp = int(time.time())

    # Build the dictionary with the time and the response data
    data = {"time": timestamp, "data": response}

    # Write the dictionary into the file
    with open(p.LLAMA_PROTOCOLS_PATH, mode="w") as f:
        json.dump(data, f)

    print("Done")


def check_llama_protocol_exists():
    if os.path.exists(p.LLAMA_PROTOCOLS_PATH):
        with open(p.LLAMA_PROTOCOLS_PATH, mode="r") as f:
            existing_data = json.load(f)
        print(f'Your data import from {time.ctime(existing_data["time"])}')
    else:
        with open(p.LLAMA_PROTOCOLS_PATH, mode="w") as f:
            initial_data = {"time": time.time(), "data": {}}
            json.dump(initial_data, f)
        print(f"Created new data file at {p.LLAMA_PROTOCOLS_PATH}")


@app.command(help="update protocols data")
def update(args: str = typer.Argument(None)):
    check_llama_protocol_exists()
    if typer.confirm("Do you want to update list?"):
        get_update()
    else:
        print("Data update cancelled.")


def search(query=None):
    with open(p.LLAMA_PROTOCOLS_PATH, "r") as f:
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
    matches = []
    user_selection = str(input("Select an option: [Search, Bookmarked]\n") or "Search")
    print(f"Selected {user_selection}\n")

    if user_selection.lower() == "bookmarked":
        with open(p.LLAMA_PROTOCOLS_BOOKMARK_PATH, "r") as f:
            data = json.load(f)
        slugs = [protocol["slug"] for protocol in data]
        slugs.sort()
        for slug in slugs:
            print(slug)
    else:
        check_llama_protocol_exists()
        with open(p.LLAMA_PROTOCOLS_PATH, "r") as f:
            data = json.load(f)

        last_update_time = dh.timestamp_to_datestr(data["time"])
        print(f"Data was last updated at {last_update_time}.")

        # Ask the user if they want to update the data
        update = str(input("Do you want to update the data? (Y/n): ") or "y")
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
def add(name: str, slug: str):
    slug = slug.lower()
    new_entry = {"name": name, "slug": slug}

    with open(p.LLAMA_PROTOCOLS_BOOKMARK_PATH) as f:
        bookmark_llama_protocol = json.load(f)

    if any(d["slug"] == slug for d in bookmark_llama_protocol):
        print(f"{name} already exists")
        return

    # check if slug exists
    response = dl.get_protocol(slug)
    if response.get("statusCode") == 400:
        print(f"{slug} not found")
    else:
        bookmark_llama_protocol.append(new_entry)
        with open(p.LLAMA_PROTOCOLS_BOOKMARK_PATH, mode="w") as f:
            f.write(json.dumps(bookmark_llama_protocol, indent=2))
        print(f"{name} added to bookmark_llama_protocol.json")
    return


@app.command(help="remove bookmark protocol")
def rm(slug: str):
    with open(p.LLAMA_PROTOCOLS_BOOKMARK_PATH) as f:
        bookmark_llama_protocol = json.load(f)

    if not any(slug.lower() in d["slug"] for d in bookmark_llama_protocol):
        print(f"{slug} not found")
        return

    updated_json = [
        d for d in bookmark_llama_protocol if d["slug"].lower() != slug.lower()
    ]
    with open(p.LLAMA_PROTOCOLS_BOOKMARK_PATH, mode="w") as f:
        f.write(json.dumps(updated_json, indent=2))
    print(f"{slug} removed from bookmark_llama_protocol.json")
    return
