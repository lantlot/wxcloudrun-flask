import json
import logging
import sys
import threading
import uuid
from datetime import datetime

import requests
from flask import render_template, request
from run import app
from wxcloudrun.dao import update_application_by_uuid, query_application_by_uuid, insert_application, list_application
from wxcloudrun.model import Application
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

logging.basicConfig(level=logging.INFO)

logging.info('Starting...')
class MessageDict(dict):
    def __missing__(self, key):
        return ""

    def __getitem__(self, item):
        return super(MessageDict, self).__getitem__(item)

    def get(self, k, d=None):
        return super(MessageDict, self).get(k, d)

message_dict=MessageDict()

@app.route('/chat',methods=["POST"])
def index():
    """
    :return: 返回index页面
    """
    params = request.get_json()
    res = requests.post(url="https://www.0x3f.top/chat", json=params).text
    return res
@app.route('/createMessage',methods=["POST"])
def create_message():
    params = request.get_json()
    message_id = uuid.uuid4().hex
    thread = threading.Thread(target=get_chat_message, args=(params,message_id))
    thread.start()
    return  make_succ_response(message_id)

@app.route('/pullMessage',methods=["GET"])
def pull_message():
    """
    :return: 返回index页面
    """
    params = request.args.get('uuid')

    return  make_succ_response(message_dict[params])


def get_chat_message(params, message_id):
    res = requests.post(url="https://www.0x3f.top/chat", json=params).text
    message_dict[message_id]=res


@app.route('/adv',methods=["POST"])
def adv():
    params = request.get_json()
    res=requests.post(url="https://www.0x3f.top/adv", json=params).text
    return  res

@app.route('/app/<app_uuid>',methods=["POST"])
def add_app(app_uuid):
    params = request.get_json()
    params.uuid=app_uuid
    insert_application(params)
    return  make_succ_empty_response()
@app.route('/app',methods=["GET"])
def list_app():
    applications = list_application()
    return  json.dumps(applications)

@app.route('/use_app/<app_uuid>',methods=["POST"])
def use_app(app_uuid):
    application=query_application_by_uuid(app_uuid)
    print(application)
    sys.stdout.flush()
    params = request.get_json()
    message_id = uuid.uuid4().hex
    prompt= [{"role": "user", "content": application['prompt'] + params["data"]}]
    thread = threading.Thread(target=get_chat_message, args=(prompt, message_id))
    thread.start()
    return make_succ_response(message_id)



# @app.route('/app/<app_uuid>/',methods=["GET"])
# def get_app(app_uuid):
#     return  query_application_by_uuid(app_uuid)


@app.route('/createAdv',methods=["POST"])
def create_adv_message():
    params = request.get_json()
    message_id = uuid.uuid4().hex
    thread = threading.Thread(target=get_adv_message, args=(params, message_id))
    thread.start()
    return make_succ_response(message_id)


def get_adv_message(params,message_id):
    res = requests.post(url="https://www.0x3f.top/adv", json=params).text
    message_dict[message_id] = res


