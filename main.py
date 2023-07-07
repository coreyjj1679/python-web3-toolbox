import basic
import bookmark
import w3
import typer
import erc20
import llama
import cfg

app = typer.Typer()

app.add_typer(basic.app, name='basic')
app.add_typer(cfg.app, name='config')
app.add_typer(bookmark.app, name='bookmark')
app.add_typer(w3.app, name='w3')
app.add_typer(erc20.app, name='token')
app.add_typer(llama.app, name='llama')


if __name__ == "__main__":
    app()
