# Python Standard Library
import ast
from contextlib import redirect_stdout
import io
import logging
from multiprocessing import Process
from typing import Literal


# Third-Party Librairies
from flask import Flask, request
import requests
from rich.logging import RichHandler
import typer
import waitress

# Constants
HOST = "127.0.0.1"
PORT = "8000"

app = Flask(__name__)


# TODO: reinstantiate the test eval with ast then eval with exec as a fallback?
#       So that the interaction would "feel" like a Python console...
@app.route("/", methods=["POST"])
def handler() -> str | tuple[str, int]:
    code = request.data.decode("utf-8").strip()
    lines = ["... " + line for line in code.splitlines()]
    lines[0] = ">>> " + lines[0][4:]
    logger.info("\n".join(lines))
    try:
        output_stream = io.StringIO()
        with redirect_stdout(output_stream):
            ast.parse(code, mode="exec")
            exec(code, globals())
        output = output_stream.getvalue()
        logger.info(f"{output}")
    except Exception as e:
        error = f"{type(e).__name__}: {e}"  # TODO: style first part in red + bold
        logger.error(error)
        # logger.exception(error)
        output = error, requests.codes.bad_request
    return output


def send(code: str, port: int = PORT) -> str:
    response = requests.post(
        url=f"http://127.0.0.1:{port}",
        headers={"Content-Type": "text/plain"},
        data=code,
    )
    return response


def spin(
    port: int = PORT,
    log: str = "INFO",
    background: bool = False,
) -> Process | None:
    global logger
    if background:
        p = Process(target=lambda: spin(port=port, log=log), daemon=True)
        p.start()
        return p
    else:
        logging.basicConfig(
            level=log, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
        )

        logger = logging.getLogger("toupie")
        if verbose >= 0:
            logger.info(f"Toupie spinning at http://{HOST}:{port}")
        logging.getLogger("waitress.queue").setLevel(logging.ERROR)
        waitress.serve(app, host=HOST, port=port, threads=1)


def main() -> None:
    return typer.run(spin)
