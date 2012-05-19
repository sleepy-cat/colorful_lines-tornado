import tornado.web

from linesapp import Dao

MYTOKEN = 352480

class BaseHandler(tornado.web.RequestHandler):
    def is_ajax(self): 
        return ("X-Requested-With" in self.request.headers) and (self.request.headers['X-Requested-With'] == "XMLHttpRequest")

    def RedirectHome(self):
        self.redirect("/colorful_lines/")

class IndexHandler(BaseHandler):
    def get(self):
        self.render("home.html")

class GetTokenHandler(BaseHandler):
    def post(self):
        if self.is_ajax():
            self.write(str(MYTOKEN))
        else:
            self.RedirectHome()

class GetHighScoresHandler(BaseHandler):
    def post(self):
        if self.is_ajax():
            high_scores = []
            for s in Dao.HIGH_SCORES_DAO.FetchHighScores():
                high_scores.append(dict(name=s.name, score=s.score))                

            response = {
                'success':  True,
                'scores':   high_scores,
            }
            self.write(response)
        else:
            self.RedirectHome()

class SubmitScoreHandler(BaseHandler):
    def post(self):
        if self.is_ajax():
            newname = self.get_argument('name', '')
            newscore = int(self.get_argument('score', '0'))
            token = int(self.get_argument('token', '0'))

            if token != MYTOKEN:
                self.write("")
                return

            Dao.HIGH_SCORES_DAO.SubmitHighScore(newname, newscore)
            response = {
                'success':  True,
            }
            self.write(response)
        else:
            self.write("")
