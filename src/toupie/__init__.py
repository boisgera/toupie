# Python Standard Library
import ast
from contextlib import redirect_stdout
import io
import logging
import threading
import time

# Third-Party Librairies
from flask import Flask, request
from yaspin import yaspin
import waitress

# Constants
HOST = "127.0.0.1"
PORT = "8000"



def spinner_task():
    with yaspin(text=f"Toupie running on http://{HOST}:{PORT}... "):
        while True:
            time.sleep(1.0)


threading.Thread(target=spinner_task, daemon=True).start()

app = Flask(__name__)


@app.route("/", methods=["POST"])
def handler():
    code = request.data.decode("utf-8").strip()
    try:
        output_stream = io.StringIO()
        with redirect_stdout(output_stream):
            ast.parse(code, mode="exec")
            exec(code, globals())
        output = output_stream.getvalue()
    except Exception as error:
        output = f"{type(error).__name__}: {error}"
    return output


def main():
    logging.getLogger("waitress.queue").setLevel(logging.ERROR)
    waitress.serve(app, host=HOST, port=PORT, threads=1)
