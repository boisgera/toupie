import ast
from contextlib import redirect_stdout
import io
import logging
import threading
import time

from flask import Flask, request
from yaspin import yaspin
import waitress

logging.getLogger("waitress.queue").setLevel(logging.ERROR)

app = Flask(__name__)

def spinner_task():
    """This runs continuously in a separate thread."""
    with yaspin(text="Toupie running... "):
        while True:
            time.sleep(1.0)

threading.Thread(target=spinner_task, daemon=True).start()

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
    waitress.serve(app, host="127.0.0.1", port=8000, threads=1)
