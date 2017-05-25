# coding: utf-8

from flask import Blueprint, request, jsonify
from app.model.output import fetch_report, fetch_group_report

app = Blueprint(__name__, "service")

@app.route('/report', methods=["GET", "POST"])
def group():
    """ グループでの取得 """
    if request.method == "POST":
        return "Not Implemented"

    elif request.method == "GET":
        _date = request.args.get("date", default=None)
        if _date:
            return fetch_group_report(_date)
        else:
            return fetch_group_report()
