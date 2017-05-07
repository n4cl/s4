# coding: utf-8

from flask import Blueprint, request

app = Blueprint(__name__, "service")

@app.route('/', methods=["GET", "POST"])
def api():
    if request.method == "POST":
        return 'POST'
    elif request.method == "GET":
        return "GET"

