import os
from tornado import gen
from tornado.escape import json_encode, json_decode, url_escape
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import options, parse_command_line, define
from time import sleep
from uuid import uuid4

@gen.coroutine
def main():
    # give other services a moment to come up in this example
    sleep(1)
    parse_command_line()
    base_url = os.getenv('BASE_GATEWAY_HTTP_URL', 'http://localhost:8080')
    base_ws_url = os.getenv('BASE_GATEWAY_WS_URL', 'ws://localhost:8080')
    
    client = AsyncHTTPClient()
    kernel_id = '05f69731-dc95-49e4-ae45-396baca822d4'
    print('{}/api/kernels/{}/channels'.format(base_ws_url,url_escape(kernel_id)))
    ws_req = HTTPRequest(
        url='{}/api/kernels/{}/channels'.format(base_ws_url,url_escape(kernel_id)),
        auth_username='fakeuser',
        auth_password='fakepass')
    ws = yield websocket_connect(ws_req)
    print('Connected to kernel websocket')
    msg_id = uuid4().hex
    # Send an execute request
    ws.write_message(json_encode({
        'header': {
            'username': '',
            'version': '5.0',
            'session': '',
            'msg_id': msg_id,
            'msg_type': 'execute_request'
        },
        'parent_header': {},
        'channel': 'shell',
        'content': {
            'code': "import matplotlib.pyplot as plt;import matplotlib;plt.scatter([1,2,3],[4,2,5]);plt.show();",
            'silent': False,
            'store_history': False,
            'user_expressions' : {},
            'allow_stdin' : False,
            'metadata' : {
                'image/png': {
                    'width': 640,
                    'height': 480
                },
                'application/json': {
                    'expanded': True
                }
            }
        },
        "metadata": {
            'image/png': {
                'width': 640,
                'height': 480
            },
            'application/json': {
                'expanded': True
            }
        },
        'buffers': {}
    }))
    
    # Look for stream output for the print in the execute
    n = 0
    while 1:
        msg = yield ws.read_message()
        msg = json_decode(msg)
        msg_type = msg['msg_type']
        print('Received message type:', msg_type)
        if msg_type == 'error':
            print('ERROR')
            print(msg)
            break
        else:
            # print('  Content:', msg)
            parent_msg_id = msg['parent_header']['msg_id']
            # if parent_msg_id == msg_id:
            print('  Content:', msg['content'])
        n += 1
        print(n)
        if n>10:
            break


    ws.close()

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
    