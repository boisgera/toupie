# Python Standard Library
import ast
from contextlib import redirect_stdout, redirect_stderr
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
verbose = False
count = 0

app = Flask(__name__)


def annotate(symbol, text):
    lines = text.splitlines()
    lines = [symbol] + [0 * " " + l for l in lines]
    return "\n".join(lines)


@app.route("/", methods=["POST"])
def handler():
    global count
    count += 1
    if verbose:
        print(60 * "-")
        print(annotate("#️⃣", f"{count}"))

    code = request.data.decode("utf-8").strip()
    if verbose:
        print(annotate("📥", code))
    try:
        output_stream = io.StringIO()
        with redirect_stdout(output_stream):
            ast.parse(code, mode="exec")
            exec(code, globals())
        output = output_stream.getvalue()
        if verbose and output:
            print(annotate("📤", output))
    except Exception as error:
        output = f"{type(error).__name__}: {error}"
        if verbose:
            print(annotate("🚨", output))
    return output


def serve(port: int = PORT, verbose: bool = False):
    globals()["verbose"] = verbose
    print("🌀")
    print(f"Toupie spinning at http://{HOST}:{port}")
    logging.getLogger("waitress.queue").setLevel(logging.ERROR)
    waitress.serve(app, host=HOST, port=port, threads=1)

def main():
    return typer.run(serve)
