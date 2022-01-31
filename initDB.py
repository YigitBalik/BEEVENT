from hashlib import sha256
import sys
import psycopg2 as dbapi2
from config import connectionDSN
from fetch import fetch
from pathlib import Path
import json
import random

dataFile = Path("data.json")


statementDict = {
    'createImagesTable': """CREATE TABLE IF NOT EXISTS IMAGES(
        imageID SERIAL PRIMARY KEY,
        ratio VARCHAR(10),
        source VARCHAR(150),
        height INTEGER,
        width INTEGER,
        alt VARCHAR(200)
    )""",
    'createVenuesTable': """CREATE TABLE IF NOT EXISTS VENUES (
        venueID SERIAL PRIMARY KEY,
        name VARCHAR(100),
        city VARCHAR(50),
        country VARCHAR(50),
        address VARCHAR(100),
        timezone VARCHAR(50)
    )""",
    'createEventsTable': """CREATE TABLE IF NOT EXISTS EVENTS (
        eventID SERIAL PRIMARY KEY,
        title VARCHAR(200), 
        genre VARCHAR(50), 
        status VARCHAR(20), 
        category VARCHAR(20),
        price FLOAT, 
        venue INTEGER, 
        image INTEGER DEFAULT 1,
        start_date DATE,
        start_time TIME,
        no_start_time BOOLEAN,
        FOREIGN KEY (image) REFERENCES IMAGES (imageID) ON DELETE SET DEFAULT ON UPDATE CASCADE,
        FOREIGN KEY (venue) REFERENCES VENUES (venueID) ON DELETE RESTRICT ON UPDATE CASCADE
    )""",
    'createEvaluationTable': """CREATE TABLE IF NOT EXISTS EVALUATIONS(
        evaluationID SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        comment VARCHAR(500),
        price_rate INTEGER DEFAULT 0,
        fun_rate INTEGER DEFAULT 0,
        checkedin BOOLEAN DEFAULT FALSE,
        CHECK ((price_rate >= 0) AND (price_rate <= 10)),
        CHECK ((fun_rate >= 0) AND (fun_rate <= 10))
    )""",
    'createFavTable': """CREATE TABLE IF NOT EXISTS FAVORITE_LISTS(
        listID SERIAL PRIMARY KEY,
        list_name VARCHAR(80),
        description VARCHAR(300),
        creation_time TIMESTAMP,
        updated_time TIMESTAMP,
        public BOOLEAN
    )""",
    'createUsersTable': """CREATE TABLE IF NOT EXISTS USERS(
        userID SERIAL PRIMARY KEY,
        username VARCHAR(20) UNIQUE,
        email VARCHAR(50) UNIQUE,
        password VARCHAR(256),
        country VARCHAR(50),
        age INTEGER,
        role INTEGER DEFAULT 2,
        favorites INTEGER,
        CHECK ((role >= 0) AND (role <= 2)),
        CHECK (age >= 0),
        FOREIGN KEY (favorites) REFERENCES FAVORITE_LISTS (listID) ON DELETE SET NULL ON UPDATE CASCADE
    )""",
    'createFavEventsTable': """CREATE TABLE IF NOT EXISTS FAVORITE_EVENTS(
        listID INTEGER NOT NULL,
        eventID INTEGER NOT NULL,
        PRIMARY KEY (listID,eventID),
        FOREIGN KEY (listID) REFERENCES FAVORITE_LISTS (listID) ON DELETE CASCADE,
        FOREIGN KEY (eventID) REFERENCES EVENTS (eventID) ON DELETE CASCADE
    )""",
    'createAppTable': """CREATE TABLE IF NOT EXISTS USER_EVENTS(
        userID INTEGER NOT NULL,
        eventID INTEGER NOT NULL,
        evaluationID INTEGER,
        PRIMARY KEY (userID,eventID),
        FOREIGN KEY (userID) REFERENCES USERS (userID) ON DELETE CASCADE,
        FOREIGN KEY (eventID) REFERENCES EVENTS (eventID),
        FOREIGN KEY (evaluationID) REFERENCES EVALUATIONS (evaluationID) ON DELETE SET NULL
    )""",
    'insertImage': """INSERT INTO IMAGES (ratio, source, height, width, alt) VALUES (%(ratio)s,%(source)s,%(height)s,%(width)s,%(alt)s)""",
    'insertVenue': """INSERT INTO VENUES (name, city, country, address, timezone) VALUES (%(name)s,%(city)s,%(country)s,%(address)s,%(timezone)s)""",
    'insertEvent': """INSERT INTO EVENTS (title, genre, status, category, price, venue, image,start_date, start_time, no_start_time) VALUES (%(name)s,%(genre)s,%(status)s,%(category)s,%(price)s,%(venue)s,%(image)s,%(start_date)s, %(start_time)s, %(no_start_time)s)""",
    'insertUser': """INSERT INTO USERS (username, email, password, country, age, role) VALUES (%(username)s, %(email)s, %(password)s, %(country)s, %(age)s,%(role)s)""",
    'dropAll': ["""DROP TABLE IF EXISTS USER_EVENTS CASCADE""","""DROP TABLE IF EXISTS EVALUATIONS CASCADE""","""DROP TABLE IF EXISTS USERS CASCADE""",
                """DROP TABLE IF EXISTS EVENTS CASCADE""","""DROP TABLE IF EXISTS FAVORITE_LISTS CASCADE""","""DROP TABLE IF EXISTS VENUES CASCADE""","""DROP TABLE IF EXISTS IMAGES CASCADE""",
                """DROP TABLE IF EXISTS FAVORITE_EVENTS CASCADE"""]
}


def init():
    imageID = 1
    venueID = 0
    dateID = 0
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                for query in statementDict['dropAll']:
                    cursor.execute(query)
                cursor.execute(statementDict["createImagesTable"])
                cursor.execute(statementDict['createVenuesTable'])
                cursor.execute(statementDict['createEventsTable'])
                cursor.execute(statementDict['createFavTable'])
                cursor.execute(statementDict['createUsersTable'])
                cursor.execute(statementDict['createFavEventsTable'])
                cursor.execute(statementDict['createEvaluationTable'])
                cursor.execute(statementDict['createAppTable'])
                cursor.execute(statementDict['insertImage'], {
                                'ratio': '301_170',
                                'source': 'https://github.com/balik18/test/blob/main/logo.png?raw=true',
                                'height': 301,
                                'width': 170,
                                'alt': 'logo'
                            })
                if not dataFile.exists():
                    fetch()
                with open("data.json", encoding="utf-8") as data:
                    events = json.load(data)
                    for event in events:
                        print(event['id'])
                        image = event['images'][0]
                        if "_embedded" in event:
                            venue = event['_embedded']['venues'][0]
                            date = event['dates']
                            venueID += 1
                            imageID += 1
                            dateID += 1
                            cursor.execute(statementDict['insertImage'], {
                                'ratio': image['ratio'] if ('ratio' in image) else None,
                                'source': image['url'] if ('url' in image) else None,
                                'height': image['height'] if ('height' in image) else None,
                                'width': image['width'] if ('width' in image) else None,
                                'alt': event['name'] + ' image'
                            })
                            cursor.execute(statementDict['insertVenue'], {
                                'name': venue['name'] if ('name' in venue) else None,
                                'city': venue['city']['name'] if ('city' in venue) else None,
                                'country': venue['country']['name'] if ('country' in venue) else None,
                                'address': venue['address']['line1'] if ('address' in venue) else None,
                                'timezone': venue['timezone'] if ('timezone' in venue) else None
                            })
                            cursor.execute(statementDict['insertEvent'], {
                                'name': event['name'],
                                'genre': event['classifications'][0]['genre']['name'] if('classifications' in event and ('genre' in event['classifications'][0])) else None,
                                'status': event['dates']['status']['code'],
                                'category': event['classifications'][0]['segment']['name'] if('classifications' in event and ('segment' in event['classifications'][0])) else None,
                                'start_date': date['start']['localDate'] if ('localDate' in date['start']) else None,
                                'start_time': date['start']['localTime'] if ('localTime' in date['start']) else None,
                                'no_start_time': date['start']['noSpecificTime'] if ('noSpecificTime' in date['start']) else False,
                                'price': random.randint(100,300),
                                'venue': venueID,
                                'image': imageID
                            })
                cursor.execute(statementDict['insertUser'],{
                    'username': 'balik18',
                    'email': 'balik18@itu.edu.tr',
                    'password': sha256('admin1'.encode('utf-8')).hexdigest(),
                    'country': 'Turkey',
                    'age': 21,
                    'role': 2
                })
                cursor.execute(statementDict['insertUser'],{
                    'username': 'kocakm18',
                    'email': 'kocakm18@itu.edu.tr',
                    'password': sha256('admin2'.encode('utf-8')).hexdigest(),
                    'country': 'Turkey',
                    'age': 21,
                    'role': 2
                })
    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(
            error))


if __name__ == "__main__":
    init()
