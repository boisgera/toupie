# Python Standard Library
import ast
from contextlib import redirect_stdout
import io
import logging
import threading
import time

# Third-Party Librairies
from flask import Flask, request
import typer
from yaspin import yaspin
import waitress

# Constants
HOST = "127.0.0.1"
PORT = "8000"

# State
verbose = False


def spinner(port=PORT):
    def spin():
        with yaspin(text=f"Toupie spinning at http://{HOST}:{port}. "):
            while True:
                time.sleep(1.0)
    return spin


app = Flask(__name__)

@app.route("/", methods=["POST"])
def handler():
    code = request.data.decode("utf-8").strip()
    if verbose:
        print("<-")
        print(code)
    try:
        output_stream = io.StringIO()
        with redirect_stdout(output_stream):
            ast.parse(code, mode="exec")
            exec(code, globals())
        output = output_stream.getvalue()
    except Exception as error:
        output = f"{type(error).__name__}: {error}"
    if verbose:
        print("->")
        print(output) 
    return output

def serve(port: int = PORT, verbose: bool = False):
    globals()["verbose"] = verbose
    threading.Thread(target=spinner(port), daemon=True).start()
    logging.getLogger("waitress.queue").setLevel(logging.ERROR)
    waitress.serve(app, host=HOST, port=port, threads=1)

def main(): 
    return typer.run(serve)