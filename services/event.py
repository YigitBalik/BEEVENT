# fmt: off
from datetime import datetime, time
import sys
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from models import  Event, Image, Venue
# fmt: on


def getEvents():
    query = "SELECT events.eventid, events.title, events.status, images.imageid, images.source, images.height, images.width, images.alt, venues.venueid, venues.name "\
            "AS venue, events.start_date as date FROM events, images, venues WHERE ((events.image = images.imageid) AND (events.venue = venues.venueid))"\
            "ORDER BY events.start_date"
    events = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for eventid, title, status, imageid, source, height, width, alt, venueid, venue, date in cursor:
                event = Event(eventid,title, None, status, None, None, Image(imageid,None,source,height,width,alt), Venue(venueid,venue,None,None,None,None),date,None,None)
                events.append(event)
    return events

def getEvent(id):
    query = "SELECT * FROM events, venues, images WHERE ((events.eventid = %s) AND (events.venue = venues.venueid) AND (events.image = images.imageid))"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query,(id,))
            tuple = cursor.fetchone()
            if tuple is not None:
                entity = dict(tuple)
                venue = Venue(entity['venueid'],entity['name'], entity['country'], entity['city'], entity['address'], entity['timezone'])
                image = Image(entity['imageid'],entity['ratio'], entity['source'], entity['height'], entity['width'], entity['alt'])
                event = Event(entity['eventid'],entity['title'], entity['genre'],  entity['status'], entity['category'], entity['price'], image, venue, entity['start_date'], entity['start_time'], entity['no_start_time'])
                return event
    return None

def deleteEvent(id):
    query = "DELETE FROM events WHERE (eventid=%s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                return True
    except:
        return False

def updateEvent(id,Event):
    query = "UPDATE events SET title=%s, genre=%s,  status=%s, category=%s, price=%s,image=%s, venue=%s, start_date=%s, start_time=%s, no_start_time=%s WHERE (eventid=%s)"
    event = Event.get()
    venue = event['venue'].get()
    image = event['image'].get()
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(event['title'], event['genre'],  event['status'], event['category'], event['price'], image['id'], venue['id'], event['start_date'], event['start_time'], event['no_start_time'], id))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail

def saveEvent(Event):
    query = "INSERT INTO events (title, genre,  status, category, price, venue, image, start_date, start_time, no_start_time)"\
            "VALUES (%(title)s,%(genre)s,%(status)s,%(category)s,%(price)s,%(venue)s,%(image)s,%(start_date)s,%(start_time)s,%(no_start_time)s)"\
            "RETURNING eventid"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            event = Event.get()
            cursor.execute(query,event)
            eventid = cursor.fetchone()[0]
            return eventid

def getStatuses():
    query = "SELECT DISTINCT status FROM events"
    statuses = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for status in cursor:
                statuses.append(status[0])
    return statuses

def getDate(eventid):
    query = "SELECT start_date, start_time, no_start_time FROM events where (eventid=%s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (eventid, ))
            result = cursor.fetchone()
            if not result[2]:
                return datetime.combine(result[0], result[1])
            else:
                return datetime.combine(result[0], time(0,0))
