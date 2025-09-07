# Python Standard Library
import ast
from contextlib import redirect_stdout
import io
import logging
import sys


# Third-Party Librairies
from flask import Flask, request
import typer
import waitress

# Constants
HOST = "127.0.0.1"
PORT = "8000"

# State
verbose = 1
count = 0

app = Flask(__name__)


def annotator(
        type: str, 
        pad: int = 8, 
        gutter: str = " ") -> str:
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

@app.route("/", methods=["POST"])
def handler() -> str:
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
        output = ""
        if verbose >= 1:
            error = f"{type(e).__name__}: {e}"
            print(ERROR(error))
    return output


def spin(port: int = PORT, verbose: int = 0) -> None:
    globals()["verbose"] = verbose
    if verbose >= 0:
        print(f"Toupie spinning at http://{HOST}:{port}")
    logging.getLogger("waitress.queue").setLevel(logging.ERROR)
    waitress.serve(app, host=HOST, port=port, threads=1)

def main() -> None:
    return typer.run(spin)
