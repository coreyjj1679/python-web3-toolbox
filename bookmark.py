import typer
import json
import os.path
from user_config import UserConfig

config = UserConfig()
app = typer.Typer()


@app.command(help='open your favourite dapp on browser')
def goto(name: str):
    togo = next(item for item in config.bookmark_list if item["name"].lower() == name.lower())
    typer.launch(togo['url'])


@app.command(help="Add your favourite dapp to bookmark")
def add(name: str, url: str):
    base_path = os.path.dirname(__file__)
    bookmark_path = os.path.join(base_path, 'configs/bookmarks.json')
    new_entry = {"name": name, "url": url}

    with open(bookmark_path) as old_json:
        bookmarks = json.load(old_json)

    if any(name in d['name'].lower() for d in bookmarks):
        print(f'{name} already exists.')
        return

    bookmarks.append(new_entry)
    with open(bookmark_path, mode='w') as f:
        f.write(json.dumps(bookmarks, indent=2))
    print(f'added {name} to bookmarks.json')


@app.command(help='remove bookmark from the list')
def rm(name: str):
    base_path = os.path.dirname(__file__)
    bookmark_path = os.path.join(base_path, 'configs/bookmarks.json')

    with open(bookmark_path) as bookmark_json:
        bookmarks = json.load(bookmark_json)

    if not any(name.lower() in d['name'].lower() for d in bookmarks):
        print(f'{name} not found.')
        return

    updated_json = [d for d in bookmarks if d['name'].lower() != name.lower()]
    with open(bookmark_path, mode='w') as f:
        f.write(json.dumps(updated_json, indent=2))
    print(f'{name} removed from bookmark.')
