import typer
from .libs.client import Client
from .libs.config import config
from rich import print

app = typer.Typer()
api = Client()


@app.command()
def init():
    linea_root_url = typer.prompt("Your Linea API address (e.g. dev.linea.ai) :")
    api_token = typer.prompt("Your API token: ")

    if not linea_root_url.startswith("http"):
        linea_root_url = f"http://{linea_root_url}"
    config.save_config({"linea_root_url": linea_root_url, "api_token": api_token})


@app.command()
def pipelines():
    print(api.list_pipelines())


@app.command()
def executions(pipeline: str):
    print(api.list_executions(pipeline))


@app.command()
def get_execution(pipeline: str, execution_id: str):
    print(api.get_execution(pipeline, execution_id))
