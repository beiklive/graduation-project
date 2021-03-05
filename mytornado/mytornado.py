import tornado.web
import tornado.ioloop
import my_admin_login
from tornado.options import define, options

define("port", default=8765, help="运行端口", type=int)

# http://localhost:8888/admin_login?type=login&admin_name=nas&admin_pw=root
class AdminLoginHandler(tornado.web.RequestHandler):
    def get(self):
        msg_type = self.get_argument("type")
        admin_name = self.get_argument("admin_name")
        admin_pw = self.get_argument("admin_pw")
        # self.write("get")
        my_admin_login.msg_process(self, msg_type, admin_name, admin_pw)
        
if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r"/admin_login", AdminLoginHandler),
        ],
    )
    app.listen(options.port)
    print("http://localhost:{}/".format(options.port))
    tornado.ioloop.IOLoop.current().start()
