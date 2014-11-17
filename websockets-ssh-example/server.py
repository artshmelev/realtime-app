import os, json
from tornado import ioloop, web, websocket

from ssh_worker import SSHWorker

host = 'calcnoqueue.vdi.mipt.ru'
user = '' # username
secret = '' # password
port = 22

settings = {
    'static_path': os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                'static')
}


class MyWebSocketHandler(websocket.WebSocketHandler):
    def open(self, *args):
        print "open MyWebSocketHandler"
        s = json.dumps({'type': 0, 'list': worker.exec_ls()})
        self.write_message(s)

    def on_message(self, message):
        data = json.loads(message)
        print 'on_message', data['target'], data['id']

        if data['id'] == -1:
            worker.exec_write(data['target'], data['text'])
        else:
            if worker.get_filetype(data['target']) == 0:
                worker.exec_cd(data['target'])
                s = json.dumps({'type': 0,
                                'list': worker.exec_ls()})
            else:
                s = json.dumps({'type': 1,
                                'id': data['id'],
                                'text': worker.exec_cat(data['target'])})

            self.write_message(s)


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')


def main():
    global worker
    worker = SSHWorker(host, user, secret, port)

    app = web.Application([
        (r'/', IndexHandler),
        (r'/ws', MyWebSocketHandler)
    ], **settings)
    app.listen(8888)
    try:
        ioloop.IOLoop.instance().start()
    finally:
        print 'OK'
        worker.close()


if __name__ == '__main__':
    main()
