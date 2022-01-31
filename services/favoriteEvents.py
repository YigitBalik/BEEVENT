# fmt: off
import sys

from flask import sessions
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from services.event import getEvent
from services.user import getUserById,updateFavoriteListId
from models import  Event, FavoriteList, UserEvent, FavoriteEvent
# fmt: on

def addEventToFavoriteEvents(favoriteEvent):
    query = "INSERT INTO favorite_events VALUES (%(listID)s,%(eventID)s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                favoriteEventDict = favoriteEvent.get()
                cursor.execute(query,favoriteEventDict)
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail        

def deleteEventFromFavoriteEvents(favoriteEvent):
    query = "DELETE FROM favorite_events WHERE(listid = %(listID)s AND eventid = %(eventID)s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                favoriteEventDict = favoriteEvent.get()
                cursor.execute(query,favoriteEventDict)
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail        


def isEventInFavoriteList(favoritelistidCurrentUser,eventid):
    query = "SELECT * FROM favorite_events WHERE(listid =%s AND eventid = %s )"
    with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(favoritelistidCurrentUser,eventid))
                if(cursor.fetchone() is not None):
                    return True
                else:
                    return False

def getFavoriteEvents(favoriteListID):
    query = "SELECT events.eventid, events.title, events.genre, events.category FROM favorite_events JOIN events ON(favorite_events.eventid = events.eventid) WHERE(favorite_events.listid = %s) ORDER BY events.eventid"
    favoriteEvents = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (favoriteListID,))
            for eventid, title, genre, category in cursor:
                event = Event(eventid, title, genre, None, category, None,None,None,None,None,None)
                event = event.get()
                favoriteEvents.append(event)
    if favoriteEvents:
        return favoriteEvents
    else:
        return None