# Python Standard Library
import ast
from contextlib import redirect_stdout
import io
import logging
from multiprocessing import Process


# Third-Party Librairies
from flask import Flask, request
import requests
import typer
import waitress

# Constants
HOST = "127.0.0.1"
PORT = "8000"

# State
verbose = 1
count = 0

app = Flask(__name__)


def annotator(type: str, pad: int = 8, gutter: str = " ") -> str:
    if len(type) <= pad:
        message = type + (pad - len(type)) * " "
    else:
        message = type[:8]
        message[-1] = "…"

    def annotate(text: str) -> str:
        lines = text.splitlines()
        if lines == []:
            lines = [""]
        sidebar = [pad * " " for _ in lines]
        sidebar[0] = message
        lines = [s + gutter + l for (s, l) in zip(sidebar, lines)]
        return "\n".join(lines)

    return annotate


INFO = annotator("INFO")
WARNING = annotator("WARNING")
ERROR = annotator("ERROR")
INPUT = annotator("<-")
OUTPUT = annotator("->")


# TODO: factor out server-side information
@app.route("/", methods=["POST"])
def handler() -> str | tuple[str, int]:
    global count
    count += 1
    if verbose >= 1:
        print(60 * "-")
        print(INFO(f"exec #{count}"))

    code = request.data.decode("utf-8").strip()
    if verbose >= 1:
        print(INPUT(code))
    try:
        output_stream = io.StringIO()
        with redirect_stdout(output_stream):
            ast.parse(code, mode="exec")
            exec(code, globals())
        output = output_stream.getvalue()
        if verbose >= 1:
            print(OUTPUT(output))
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        if verbose >= 1:
            print(ERROR(error))
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
    verbose: int = 0,
    background: bool = False,
) -> Process | None:
    if background:
        p = Process(target=lambda: spin(port=port, verbose=verbose), daemon=True)
        p.start()
        return p
    else:
        globals()["verbose"] = verbose
        if verbose >= 0:
            print(f"Toupie spinning at http://{HOST}:{port}")
        logging.getLogger("waitress.queue").setLevel(logging.ERROR)
        waitress.serve(app, host=HOST, port=port, threads=1)


def main() -> None:
    return typer.run(spin)
