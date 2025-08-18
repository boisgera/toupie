import logging
import time

from flask import Flask, request
import waitress

logging.getLogger("waitress.queue").setLevel(logging.ERROR)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def say_hello():
    name = request.data.decode("utf-8").strip()
    time.sleep(10.0)
    return f"Hello {name}\n"

if __name__ == "__main__":
    waitress.serve(app, host="127.0.0.1", port=8000, threads=1)

