# -*- coding: utf-8 -*-
import json
import logging
import time
from flask import Flask, request
from conf import ticket_config
from engine import ticketEngineInstance
from req.ticket_req import TicketReq

app = Flask(__name__)

logger = logging.getLogger("lcc_ticket_info")


@app.route('/ticket/info', methods=['POST'])
def ticket_info():
    req = TicketReq()
    logger.info('request: {0}'.format(json.dumps(request.json)))
    if not req.constructor(request.json):
        return json.dumps({"status": "1", "message": "Invalid request parameters!"})
    start_time = time.time()
    result = ticketEngineInstance.run(req)
    end_time = time.time()
    result = json.dumps(result)
    logger.info(
        'response:{0:.0f}, response:{1} , request:{2}'.format(end_time - start_time, result, json.dumps(request.json)))
    return result


@app.route('/', methods=['GET'])
def hello_world():
    return "hello world"


if __name__ == '__main__':
    port = ticket_config.getint('server', 'port')
    app.run(host="0.0.0.0", port=port, debug="true")
