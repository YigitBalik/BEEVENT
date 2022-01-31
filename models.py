'''
Contains Python Classes for database models

Event, Image, Venue, User, Evaluation, Statistic

TODO:
...
'''
import copy
from hashlib import sha256

class Event(object):
    '''
    Object model of Event data
    '''

    def __init__(self, id, title, genre, status, category, price, image, venue, start_date, start_time, no_start_time):
        self.id = id
        self.title = title
        self.genre = genre
        self.start_date = start_date
        self.start_time = start_time
        self.no_start_time = no_start_time
        self.status = status
        self.category = category
        self.price = price
        self.image = image
        self.venue = venue

    def setID(self, id=None):
        self.id = id
        return self.id

    def toDict(self):
        event = {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'category': self.category,
            'price': self.price,
            'start_date': self.start_date,
            'start_time': self.start_time,
            'no_start_time': self.no_start_time,
            'status': self.status,
            'image': self.image,
            'venue': self.venue,
        }
        return event

    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)


class Image(object):
    '''
    Object model of Image data
    '''

    def __init__(self, id, ratio, source, height, width, alt):
        self.id = id
        self.ratio = ratio
        self.source = source
        self.height = height
        self.width = width
        self.alt = alt

    def setID(self, id=None):
        self.id = id
        return self.id

    def toDict(self):
        image = {
            'id': self.id,
            'ratio': self.ratio,
            'source': self.source,
            'height': self.height,
            'width': self.width,
            'alt': self.alt
        }
        return image

    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)


class Venue(object):
    '''
    Object model of Venue data
    '''

    def __init__(self, id, name, country, city, address, timezone):
        self.id = id
        self.name = name
        self.country = country
        self.city = city
        self.address = address
        self.timezone = timezone

    def setID(self, id=None):
        self.id = id
        return self.id

    def toDict(self):
        venue = {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'address': self.address,
            'timezone': self.timezone
        }
        return venue

    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)

class UserEvent(object):
    '''
    Object model of User Events
    '''
    def __init__(self, user, event, evaluation):
        self.user = user
        self.event = event
        self.evaluation = evaluation
    
    def toDict(self):
        userEvent = {
            'user': self.user,
            'event': self.event,
            'evaluation': self.evaluation
        }
        return userEvent
    
    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)
        
class User(object):
    '''
    Object model of User data
    '''

    def __init__(self, id, username, email, password, country, age, role, favoriteList):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.country = country
        self.age = age
        self.role = role
        self.favoriteList = favoriteList

    def setID(self, id=None):
        self.id = id
        return self.id

    def setPassword(self):
        self.password = sha256(self.password.encode('utf-8')).hexdigest()

    def toDict(self):
        user = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'country': self.country,
            'age': self.age,
            'role': self.role,
            'favoriteList': self.favoriteList
        }
        return user

    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)
    
    def getPassword(self):
        return self.password
    
    def getFavoriteListID(self):
        return self.favoriteList

class Evaluation(object):
    '''
    Object model of Evaluation data
    '''

    def __init__(self, id, timestamp, comment, priceRate, funRate, isCheckedIn):
        self.id = id
        self.timestamp = timestamp
        self.comment = comment
        self.priceRate = priceRate
        self.funRate = funRate
        self.isCheckedIn = isCheckedIn

    def setID(self, id=None):
        self.id = id
        return self.id

    def toDict(self):
        evaluation = {
            'id': self.id,
            'timestamp': self.timestamp,
            'comment': self.comment,
            'priceRate': self.priceRate,
            'funRate': self.funRate,
            'isCheckedIn': self.isCheckedIn
        }
        return evaluation

    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)

class FavoriteList(object):
    '''
    Object model of FavoriteList data
    '''

    def __init__(self, id, listName, description, creationTime, updatedTime, isPublic):
        self.id = id
        self.listName = listName
        self.description = description
        self.creationTime = creationTime
        self.updatedTime = updatedTime
        self.isPublic = isPublic

    def setID(self, id=None):
        self.id = id
        return self.id

    def toDict(self):
        favoriteList = {
            'id': self.id,
            'listName': self.listName,
            'description': self.description,
            'creationTime': self.creationTime,
            'updatedTime': self.updatedTime,
            'isPublic': self.isPublic
        }
        return favoriteList

    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)

    def getID(self):
        return self.id

class FavoriteEvent(object):
    '''
    Object model of FavoriteEvent data
    '''

    def __init__(self,listid,eventid):
        self.listID = listid
        self.eventID = eventid

    def toDict(self):
        favoriteEvent = {
            'listID': self.listID,
            'eventID': self.eventID
        }
        return favoriteEvent

    def get(self):
        return self.toDict()

    def getCopy(self):
        return copy.deepcopy(self)
