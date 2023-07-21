import typer
import basic
import cfg
import erc20
import llama
import w3
from src.cli.user_config import UserConfig

config = UserConfig()
app = typer.Typer()

app.add_typer(basic.app, name="basic")
app.add_typer(cfg.app, name="config")
app.add_typer(w3.app, name="w3")
app.add_typer(erc20.app, name="token")
app.add_typer(llama.app, name="llama")


@app.command(
    help="Go straight into bookmarked website, avoiding scam results from google."
)
def goto(name: str):
    togo = next(
        item for item in config.bookmark_list if item["name"].lower() == name.lower()
    )
    typer.launch(togo["url"])


if __name__ == "__main__":
    app()
