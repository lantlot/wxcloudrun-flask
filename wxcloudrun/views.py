from datetime import datetime

import requests
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
@app.route('/chat',methods=["POST"])
def index():
    """
    :return: 返回index页面
    """
    params = request.get_json()
    res=requests.post(url="https://www.0x3f.top/chat", json=params).text
    print(res)
    return  res
