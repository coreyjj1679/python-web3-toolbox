from rich.console import Console
from user_config import UserConfig
import basic
import bookmark
import w3
import typer


config = UserConfig()
app = typer.Typer()
app.add_typer(basic.app, name='basic')
app.add_typer(bookmark.app, name='bookmark')
app.add_typer(w3.app, name='w3')

if __name__ == "__main__":
    app()
