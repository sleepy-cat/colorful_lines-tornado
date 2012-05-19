import os
import collections
import sqlite3

DB_FILE_NAME = "scores.db"
DB_FILE_PATH = ""
MAX_FETCHED_HIGHSCORES = 10

HighScore = collections.namedtuple('HighScore', 'name, score')

HIGH_SCORES_DAO = None

def Init(db_file_path):
    global DB_FILE_PATH 
    DB_FILE_PATH = db_file_path
    global HIGH_SCORES_DAO
    HIGH_SCORES_DAO = HighScoresDao() 

class HighScoresDao:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DB_FILE_PATH, DB_FILE_NAME))
        # Enable WAL
        # http://stackoverflow.com/questions/4393936/setting-sqlite-i-o-priority-from-python-module-speeding-up-sqlite-commits
        # http://www.sqlite.org/wal.html
        cur = self.conn.cursor()
        cur.execute("PRAGMA synchronous=off")
        cur.close()

    def Close(self):
        if (conn != None):
            conn.close()

    def CreateSchema(self):
        curs = self.conn.cursor()
        curs.execute("""CREATE TABLE IF NOT EXISTS scores (
                        name text, 
                        score int,
                        PRIMARY KEY(name))""")
        curs.close()

    def SubmitHighScore(self, name, score):
        curs = self.conn.cursor()
        curs.execute("REPLACE INTO scores(name, score) VALUES(?, ?)", (name, score))
        self.conn.commit()
        curs.close()

    def FetchHighScores(self):
        curs = self.conn.cursor()
        curs.execute("SELECT name, score from scores ORDER BY score desc LIMIT %d" % MAX_FETCHED_HIGHSCORES)
        result = [x for x in map(HighScore._make, curs.fetchall())]
        curs.close()
        return result
