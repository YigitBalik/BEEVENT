import sys
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from models import Evaluation

def createEvaluation(Evaluation):
    query = "INSERT INTO evaluations(timestamp, comment, price_rate, fun_rate, checkedin) VALUES(%(timestamp)s,%(comment)s,%(priceRate)s,%(funRate)s,%(isCheckedIn)s)"\
            "RETURNING evaluationid"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            evaluation = Evaluation.get()
            cursor.execute(query,evaluation)
            evaluationid = cursor.fetchone()[0]
            return evaluationid

def deleteEvaluation(evaluationid):
    query= "DELETE FROM evaluations WHERE(evaluationid = %s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,(evaluationid,))


def saveEvaluation(Evaluation):
    query = "UPDATE evaluations SET timestamp = %(timestamp)s, comment = %(comment)s, price_rate = %(priceRate)s, fun_rate = %(funRate)s, checkedin = %(isCheckedIn)s "\
            "WHERE(evaluationid = %(id)s)"\
            "RETURNING evaluationid"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            evaluation = Evaluation.get()
            cursor.execute(query,evaluation)
            evaluationid = cursor.fetchone()[0]
            return evaluationid


def getEventEvaluations(eventid):
    query = "SELECT evaluations.evaluationid, evaluations.timestamp, evaluations.comment, evaluations.price_rate, evaluations.fun_rate, evaluations.checkedin FROM user_events JOIN evaluations ON(user_events.evaluationid = evaluations.evaluationid) WHERE(eventid = %s) ORDER BY evaluations.timestamp DESC"
    evaluations = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (eventid,))
            for evaluationid, timestamp, comment, price_rate, fun_rate, checkedin in cursor:
                evaluation = Evaluation(evaluationid, timestamp, comment, price_rate, fun_rate, checkedin)
                evaluation = evaluation.get()
                evaluations.append(evaluation)
    return evaluations

def getEvaluation(evaluationid):
    query = "SELECT * FROM evaluations WHERE(evaluationid = %s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query,(evaluationid,))
            tuple = cursor.fetchone()
            if tuple is not None:
                entity = dict(tuple)
                evaluation = Evaluation(entity['evaluationid'], entity['timestamp'], entity['comment'],entity['price_rate'], entity['fun_rate'], entity['checkedin'])
                return evaluation
            return None