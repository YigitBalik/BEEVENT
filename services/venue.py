# fmt: off
import sys
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from models import Venue
# fmt: on

def saveVenue(Venue):
    query = "INSERT INTO venues (name, city, country, address, timezone) VALUES (%(name)s, %(city)s, %(country)s, %(address)s, %(timezone)s)"\
            "RETURNING venueid"
    venue = Venue.get()
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,venue)
            venueid = cursor.fetchone()[0]
            return venueid

#print(saveVenue(Venue(None,"test","test","test","test","test")))

def getVenue(venueid):
    query = "SELECT * FROM venues WHERE (venueid = %s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query,(venueid,))
            entity = dict(cursor.fetchone());
            venue = Venue(entity['venueid'], entity['name'], entity['city'], entity['country'], entity['address'], entity['timezone'])
            return venue

#print(getVenue(191).get())

def getVenues():
    query = "SELECT * FROM venues"
    venues = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for venueid, name, city, country, address, timezone in cursor:
                venue = Venue(venueid, name, city, country, address, timezone)
                venues.append(venue)
    return venues

def updateVenue(venueid,Venue):
    query = "UPDATE venues SET name=%s, city=%s, country=%s, address=%s, timezone=%s WHERE (venueid = %s)"
    venue = Venue.get()
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(venue['name'],venue['city'],venue['country'],venue['address'],venue['timezone'],venueid))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail

#print(updateVenue(191,Venue(None,"UPDATE_TEST","UPDATE_TEST","UPDATE_TEST","UPDATE_TEST","UPDATE_TEST")))

def deleteVenue(venueid):
    query = "DELETE FROM venues WHERE (venueid=%s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (venueid,))
                return True
    except:
        return False

#print(deleteVenue(191))

def getCountries():
    query = "SELECT DISTINCT country FROM venues"
    countries = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for country in cursor:
                countries.append(country[0])
    return countries
