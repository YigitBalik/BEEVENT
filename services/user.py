from hashlib import sha256
import sys

from flask import sessions
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from models import User


def updateUser(userid,User):
    query = "UPDATE users SET username=%s, email=%s, country=%s, age=%s WHERE (userid = %s)"
    user = User.get()
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(user['username'],user['email'],user['country'],user['age'],userid))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail

def changePassword(userid,password):
    query = "UPDATE users SET password=%s WHERE (userid = %s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(password,userid))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail

def updateUserRole(userid, role):
    query = "UPDATE users SET role=%s WHERE (userid = %s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(role,userid))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail

def saveUser(User):
    query = "INSERT INTO users (username, email, password, country, age, role) VALUES (%(username)s,%(email)s,%(password)s,%(country)s,%(age)s,%(role)s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            User.setPassword()
            user = User.get()
            user['password'] = User.getPassword()
            cursor.execute(query,user)
            return True

def getUserByUsername(username):
    query = "SELECT * FROM users WHERE (username = %s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query,(username,))
            tuple = cursor.fetchone()
            if tuple is not None:
                entity = dict(tuple)
                user = User(entity['userid'], entity['username'], entity['email'], entity['password'], entity['country'], entity['age'], entity['role'],entity['favorites'])
                return user
    return None

def getUserById(userid):
    query = "SELECT * FROM users WHERE (userid = %s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query,(userid,))
            tuple = cursor.fetchone()
            if tuple is not None:
                entity = dict(tuple)
                user = User(entity['userid'], entity['username'], entity['email'], None, entity['country'], entity['age'], entity['role'],entity['favorites'])
                return user
    return None

def getUsers():
    query = "SELECT userid, username, email, country, age, role, favorites FROM users"
    users = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for userid, username, email, country, age, role, favorites in cursor:
                user = User(userid, username, email, None, country, age, role, favorites)
                users.append(user)
    return users

def deleteUser(userid):
    query = "DELETE FROM users WHERE (userid=%s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (userid,))
                return True
    except:
        return False

def updateFavoriteListId(listid,userid):
    query = "UPDATE users SET favorites = %s WHERE(userid = %s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(listid,userid))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail

def getFavoriteListId(userid):
    query = "SELECT favorites FROM users WHERE (userid = %s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (userid,))
            favlistid = cursor.fetchone()[0]
            if  favlistid is not None:
                return favlistid      
    return None