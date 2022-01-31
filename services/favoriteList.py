# fmt: off
import sys

from flask import sessions
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from services.event import getEvent
from services.user import getUserById,updateFavoriteListId
from models import  Event, FavoriteList, UserEvent
# fmt: on



def getFavoriteList(userid):
    user = getUserById(userid)
    favListID = user.getFavoriteListID()
    if(favListID):
        query = "SELECT * FROM favorite_lists WHERE(listid = %s)"
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor(cursor_factory = RealDictCursor) as cursor:
                cursor.execute(query,(favListID,))
                tuple = cursor.fetchone()
                if tuple is not None:
                    entity = dict(tuple)
                    favoriteList = FavoriteList(entity['listid'], entity['list_name'], entity['description'],entity['creation_time'], entity['updated_time'], entity['public'])
                    return favoriteList
                return None
    else:
        return None

def saveCreatedFavoriteList(favoriteList,userid):
    query = "INSERT INTO favorite_lists(list_name, description, creation_time, public) VALUES (%(listName)s,%(description)s,%(creationTime)s,%(isPublic)s) RETURNING listid"
    listid = 0
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            favoriteListDict = favoriteList.get()
            cursor.execute(query,favoriteListDict)
            listid = cursor.fetchone()[0]
    added = updateFavoriteListId(listid,userid)
    if(added):
        return True
    else:
        return False

def saveUpdatedFavoriteList(favoriteList,userid):
    query = "UPDATE favorite_lists SET list_name = %(listName)s, description = %(description)s, updated_time =  %(updatedTime)s, public = %(isPublic)s WHERE(listid = %(id)s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                favoriteListDict = favoriteList.get()
                cursor.execute(query,favoriteListDict)
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail 

def deleteFavoriteList(favoriteListID):
    query = "DELETE FROM favorite_lists WHERE(listid = %s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(favoriteListID,))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail 
    

def getPublicFavoriteLists():
    query = "SELECT listid, list_name, description, creation_time, updated_time FROM favorite_lists WHERE(public = true) ORDER BY listid"
    publicFavoriteLists = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for listid, list_name, description, creation_time, updated_time in cursor:
                favoriteList = FavoriteList(listid, list_name, description, creation_time, updated_time,None)
                favoriteList = favoriteList.get()
                publicFavoriteLists.append(favoriteList)
    if publicFavoriteLists:
        return publicFavoriteLists
    else:
        return None
