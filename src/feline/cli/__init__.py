# src/feline/cli.py

import datetime
import importlib
import os
import platform
import shutil
import socket
import sys
import rich_click as click
from rich.console import Console
import uvicorn
import importlib.metadata as metadata
import requests

from importlib.metadata import version as importlib_version, PackageNotFoundError

from rich.traceback import install

install(show_locals=True)


def get_local_version(package: str = "feline") -> str:
    try:
        return importlib_version(package)
    except PackageNotFoundError:
        return "Pacote não instalado via pip"


def get_pypi_version(package: str) -> str:
    try:
        res = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=5)
        if res.status_code == 200:
            data = res.json()
            return data["info"]["version"]
        else:
            return "Erro ao consultar PyPI"
    except Exception as e:
        return f"Erro: {e}"


@click.group()
def cli() -> None:
    """🐱 Feline CLI — Framework rápido, mágico e fofo."""
    pass


@cli.command(help="🐾 Inicia o servidor ASGI com um app.")
@click.argument("import_path")
@click.option(
    "--reload", is_flag=True, default=False, help="🔁 Ativa recarregamento automático."
)
@click.option(
    "--host", default="127.0.0.1", help="🌐 Host para rodar (padrão: 127.0.0.1)"
)
@click.option("--port", default=8000, help="🚪 Porta para rodar (padrão: 8000)")
def run(import_path, reload, host, port):
    if ":" not in import_path:
        click.echo("❌ Formato inválido. Use o formato: módulo:app (ex: app:app)")
        return

    module_name, app_name = import_path.split(":")

    if "" not in sys.path and os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    try:
        mod = importlib.import_module(module_name)
        app = getattr(mod, app_name)
    except ModuleNotFoundError as e:
        console = Console()
        console.log(f"❌ Módulo não encontrado: {e.name}")
        console.print_exception()
        click.echo(f"❌ Módulo não encontrado: {e.name}")
        return
    except AttributeError:
        click.echo(f"❌ O objeto '{app_name}' não existe no módulo '{module_name}'")
        return
    except Exception as e:
        click.echo(f"❌ Erro inesperado: {e}")
        raise e

    click.echo(f"🚀 Rodando {import_path} em http://{host}:{port} ...")
    uvicorn.run(import_path, host=host, port=port, reload=reload)


@cli.command(help="📦 Cria uma estrutura básica de projeto Feline.")
@click.argument("name")
def init(name: str) -> None:
    """Cria estrutura base de projeto Feline com config e rotas separadas."""
    base = os.path.join(os.getcwd(), name)
    os.makedirs(f"{base}/routes", exist_ok=True)
    os.makedirs(f"{base}/templates", exist_ok=True)

    # app.py com apenas a configuração e chamada do app
    with open(f"{base}/app.py", "w") as f:
        f.write(
            "from feline import App, Config\n"
            "config = Config()\n"
            "config.debug = True\n"
            "config.secret_key = 'CHANGE_ME!'\n\n"
            "app = App(config)\n"
        )

    # rota inicial separada
    with open(f"{base}/routes/index.py", "w") as f:
        f.write("def get():\n" "    return 'Hello from Feline!'\n")

    click.echo(f"🐣 Projeto '{name}' criado com sucesso!")


@cli.command(help="🧼 Limpa __pycache__ (Nan bro meus olhos ardem quando eu dou tree)")
@click.argument("path")
def clean(path: str = ".") -> None:
    removed = 0
    for dirpath, dirnames, filenames in os.walk(path):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                print(f"Removed: {pycache_path}")
                removed += 1
            except Exception as e:
                print(f"Failed to remove {pycache_path}: {e}")
    print(f"\nTotal __pycache__ directories removed: {removed}")


def get_ip_info():
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "Desconhecido"

    return ip


@cli.command(help="ℹ️ Mostra informações úteis do ambiente atual.")
def info():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    python_version = platform.python_version()
    machine = platform.node()
    cwd = os.getcwd()
    ip = get_ip_info()

    try:
        feline_version = metadata.version("feline")
    except metadata.PackageNotFoundError:
        feline_version = "Não instalado via PyPI"

    click.echo("🐾 Feline Diagnostic Info")
    click.echo("-" * 30)
    click.echo(f"📅 Hora atual: {now}")
    click.echo(f"🐍 Python: {python_version}")
    click.echo(f"🧶 Feline: {feline_version}")
    click.echo(f"📁 Diretório: {cwd}")
    click.echo(f"💻 Máquina: {machine}")
    click.echo(f"🌐 IP Local: {ip}")


@cli.command(help="🔢 Mostra a versão local e do PyPI.")
def version() -> None:
    local_version = get_local_version("feline")
    pypi_version = get_pypi_version("feline")
    click.echo(f"🐾 Feline versão local: {local_version}")
    click.echo(f"📦 Versão no PyPI: {pypi_version}")


def main() -> None:
    cli()
