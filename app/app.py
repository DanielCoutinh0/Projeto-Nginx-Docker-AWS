import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "dev")


@app.route("/")
def home():
    agora = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC")
    return f"""
    <html>
      <head><title>Projeto - DevOps</title></head>
      <body style="font-family: sans-serif; text-align: center; margin-top: 80px;">
        <h1>Projeto: Flask + Docker + Nginx na AWS</h1>
        <p>Versão (commit): <b>{VERSION}</b></p>
        <p>Container (hostname): <b>{socket.gethostname()}</b></p>
        <p>Hora do servidor: <b>{agora}</b></p>
      </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(status="ok", version=VERSION)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
