import os
import sys

tornado_dir = os.path.join(os.path.dirname(__file__), "tornado")
if os.path.exists(tornado_dir):
    sys.path.append(tornado_dir)

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

import linesapp.Handlers
import linesapp.Dao

if __name__ == "__main__":
    linesapp.Dao.Init(os.path.dirname(__file__))
    linesapp.Dao.HIGH_SCORES_DAO.CreateSchema()

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/colorful_lines/?", linesapp.Handlers.IndexHandler),
                                            (r"/colorful_lines/get_token/?", linesapp.Handlers.GetTokenHandler),
                                            (r"/colorful_lines/get_highscores/?", linesapp.Handlers.GetHighScoresHandler),
                                            (r"/colorful_lines/submit_score/?", linesapp.Handlers.SubmitScoreHandler),
                                           ],
                                  template_path=os.path.join(os.path.dirname(__file__), "templates"),
                                  static_url_prefix="/colorful_lines/media/",
                                  static_path=os.path.join(os.path.dirname(__file__), "media")
                                 )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
