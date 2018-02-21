import tornado.ioloop
import tornado.web
import tornado.websocket


opened_sockets = {}


# noinspection PyAbstractClass
class SendNotificationHandler(tornado.web.RequestHandler):
    def post(self):
        task_id = self.get_argument('task_id')
        data = self.get_argument('data')

        if task_id in opened_sockets.keys():
            opened_sockets[task_id].write_message(data)

        self.write('done')


# noinspection PyAbstractClass
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    task_id = None

    def open(self):
        task_id = self.get_argument('task_id')

        opened_sockets[task_id] = self
        self.task_id = task_id

        print("WebSocket opened")

    def on_close(self):
        del opened_sockets[self.task_id]

        print("WebSocket closed")

    def check_origin(self, origin):
        return True  # this is test application, not for production server


def make_app():
    return tornado.web.Application([
        (r'/notifications/notify', SendNotificationHandler),
        (r'/notifications/ws', WebSocketHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8078)
    tornado.ioloop.IOLoop.current().start()
