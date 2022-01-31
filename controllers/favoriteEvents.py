# fmt: off
import sys
from werkzeug.utils import redirect
sys.path.append('..\\itudb2130')
from models import FavoriteList, FavoriteEvent
from flask import render_template, request
import services.favoriteList as favoriteListService
import services.favoriteEvents as favoriteEventsService
import services.user as userService
from services.evaluation import createEvaluation
from services.event import getDate
from flask_login.utils import *
from datetime import datetime
from forms import CreateFavoriteListForm
# fmt: on

@login_required
def addEventToFavoriteEvents(favoriteListID,eventid):
    favoriteEvent = FavoriteEvent(favoriteListID,eventid)
    if favoriteEventsService.addEventToFavoriteEvents(favoriteEvent):
        return redirect(url_for("event",eventid=eventid))

@login_required
def getFavoriteEvents(favoriteListID):
    favoriteEvents = favoriteEventsService.getFavoriteEvents(favoriteListID)
    favListIdOfUser = userService.getFavoriteListId(session['id'])
    isMyList = False
    if favoriteListID == favListIdOfUser:
        isMyList = True
    return render_template("favoriteEvents.html",favoriteEvents = favoriteEvents, isMyList = isMyList)

@login_required
def deleteEventFromFavoriteEvents(favoriteListID,eventid):
    favoriteEvent = FavoriteEvent(favoriteListID,eventid)
    if favoriteEventsService.deleteEventFromFavoriteEvents(favoriteEvent):
        return redirect(url_for("event",eventid=eventid))

@login_required
def deleteEventFromFavoriteEventsInFavList(eventid):
    favListIdOfUser = userService.getFavoriteListId(session['id'])
    favoriteEvent = FavoriteEvent(favListIdOfUser,eventid)
    if favoriteEventsService.deleteEventFromFavoriteEvents(favoriteEvent):
        return redirect(url_for("getFavoriteEvents",favoriteListID=favListIdOfUser))
    

