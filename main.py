# coding: utf-8

from flask import Flask
from app.controller import service

app = Flask(__name__)
app.register_blueprint(service.app, url_prefix="/sss")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
