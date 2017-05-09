# coding: utf-8

from flask import Blueprint, request, jsonify
from app.model.output import fetch_report, fetch_group_report

app = Blueprint(__name__, "service")

@app.route('/report', methods=["GET", "POST"])
def group():
    """ グループでの取得 """
    if request.method == "POST":
        return "not implemented"
        # TODO: エラートラップきちんとしよう

        if request.headers['Content-Type'] != 'application/json':
            return jsonify(res='error'), 500
        return 'POST'

    elif request.method == "GET":
        return fetch_group_report()

