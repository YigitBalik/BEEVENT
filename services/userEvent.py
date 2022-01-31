# fmt: off
import sys

from flask import sessions
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from services.event import getEvent
from services.user import getUserById
from models import  Event, UserEvent,Evaluation
# fmt: on

def getUserEvents(userid):
    query = "SELECT * FROM user_events JOIN events ON (user_events.eventid = events.eventid) JOIN evaluations ON (user_events.evaluationid = evaluations.evaluationid) WHERE (user_events.userid = %s)"
    userEvents = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query, (userid, ))
            for row in cursor.fetchall():
                entity = dict(row)
                userEvents.append(UserEvent(userid, Event(entity['eventid'],entity['title'], entity['genre'],  entity['status'], entity['category'], entity['price'], None, None, entity['start_date'], entity['start_time'], entity['no_start_time']),
                Evaluation(entity['evaluationid'],entity['timestamp'],None,None,None,entity['checkedin'])))
    return userEvents

def updateUserEvent(userEvent):
    query = "UPDATE user_events SET evaluationid = %(evaluation)s WHERE(userid = %(user)s AND eventid = %(event)s)"\
            "RETURNING evaluationid"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            userEvent = userEvent.get()
            cursor.execute(query,userEvent)
            evaluationid = cursor.fetchone()[0]
            return evaluationid


def deleteUserEvent(userid, eventid):
    query = "DELETE from user_events WHERE (userid=%s AND eventid=%s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (userid, eventid))
                return True
    except:
        return False

def saveUserEvent(UserEvent):
    query = "INSERT INTO user_events VALUES (%(user)s, %(event)s, %(evaluation)s) RETURNING eventid"
    userEvent = UserEvent.get()
    if getUserById(userEvent['user']) is None:
        return False
    if getEvent(userEvent['event']) is None:
        return False
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, userEvent)
            eventid = cursor.fetchone()[0]
            if eventid is not None:
                return True
    return False

def isExistByUserAndEvent(user, event):
    query = "SELECT * FROM user_events WHERE (userid = %s and eventid=%s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (user, event))
            if cursor.fetchone() is not None:
                return True
    return False

def getEventStartDate(user, event):
    query = "SELECT start_date FROM user_events JOIN events ON (user_events.eventid = events.eventid) WHERE (user_events.userid = %s and user_events.eventid=%s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query, (user, event))
            entity = cursor.fetchone()['start_date']
    return entity

def getEvaluationId(user, event):
    query = "SELECT evaluationid FROM user_events WHERE (userid = %s and eventid=%s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query, (user, event))
            entity = cursor.fetchone()
            if  entity is not None:
                return entity['evaluationid']      
    return None


    
