#-*- encoding:utf-8 -*-
import sys
import os
Path = os.getcwd() + "/controllers"
sys.path.append(Path)

import os
import tornado.ioloop
import tornado.web
import Home
import Login
import User
import CreatePost

from tornado.options import define, options
define("port", default = 8824, help = "run on the given port", type = int)

settings = {
        "cookie_secret" : "61oEyeqXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "login_url"     : "/login",
        "static_path"   : os.path.join(os.path.dirname(__file__), "static"),
        "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
        #"xsrf_cookies"  : True,
        "debug" : True,
        }

if __name__ == '__main__':
        tornado.options.parse_command_line()
        app=tornado.web.Application(
                handlers=[
                        (r'/',Home.IndexHandler),
                        (r'/login',Login.LoginHandler),
                        (r'/user',User.IndexHandler),
                        (r'/createPost',CreatePost.CreatePostHandler),
                        (r'/createExistPost',CreatePost.CreateExistPostHandler),
                        (r'/savePost',CreatePost.SavePostHandler),
                        (r'/saveExistPost',CreatePost.SaveExistPostHandler),
                        (r'/alterPost',CreatePost.AlterPostHandler),
                        (r'/alterExistPost',CreatePost.AlterExistPostHandler),
                        (r'/delPost',CreatePost.DelPostHandler),
                        (r'/getPostList',CreatePost.ListPostHandler),
                        (r'/post/(.*)',CreatePost.ViewPostHandler),
                      #  (r'/f/(.*)',Home.TopHandler),
                       # (r'/new/(.*)',Home.NewHandler)
            ],**settings
        )

        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
