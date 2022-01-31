# fmt: off
import sys
sys.path.append('..\\itudb2130')
from config import connectionDSN
import psycopg2 as dbapi2
from psycopg2.extras import RealDictCursor
from models import Image
# fmt: on

def saveImage(Image):
    query = "INSERT INTO images (ratio, source, height, width, alt) VALUES (%(ratio)s, %(source)s, %(height)s, %(width)s, %(alt)s)"\
            "RETURNING imageid"
    image = Image.get()
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query,image)
            imageid = cursor.fetchone()[0]
            return imageid

#print(saveImage(Image(None,"12_2","test",12,2,"test")))

def getImage(imageid):
    query = "SELECT * FROM images WHERE (imageid = %s)"
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor(cursor_factory = RealDictCursor) as cursor:
            cursor.execute(query,(imageid,))
            entity = dict(cursor.fetchone());
            image = Image(entity['imageid'],entity['ratio'], entity['source'], entity['height'], entity['width'], entity['alt'])
            return image

#print(getImage(191).get())

def getImages():
    query = "SELECT * FROM images"
    images = []
    with dbapi2.connect(connectionDSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            for imageid, ratio, source, height, width, alt in cursor:
                image = Image(imageid, ratio, source, height, width, alt)
                images.append(image)
    return images

def updateImage(imageid,Image):
    query = "UPDATE images SET ratio=%s, source=%s, height=%s, width=%s, alt=%s WHERE (imageid = %s)"
    image = Image.get()
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query,(image['ratio'],image['source'],image['height'],image['width'],image['alt'],imageid))
                return True
    except dbapi2.IntegrityError as error:
        return error.diag.message_detail

#print(updateImage(191,Image(None,"12_2","UPDATE_TEST",12,2,"test")))

def deleteImage(imageid):
    query = "DELETE FROM images WHERE (imageid=%s)"
    try:
        with dbapi2.connect(connectionDSN) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (imageid,))
                return True
    except:
        return False

#print(deleteImage(191))