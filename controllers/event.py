# fmt: off
import sys

from werkzeug.utils import redirect
sys.path.append('..\\itudb2130')
from models import Event, Image, Venue
import services.event as eventService
import services.user as userService
import services.evaluation as evaluationService
import services.userEvent as userEventService
import services.favoriteEvents as favoriteEventsService
from services.venue import getVenue
from services.image import getImage
from services.userEvent import isExistByUserAndEvent
from flask import render_template, request
from flask_login.utils import *
from forms import LoginForm, EventForm
# fmt: on

@login_required
def getEvents():
    events = eventService.getEvents()
    return render_template("Events.html", events=events)

@login_required
def getEvent(eventid):
    event = eventService.getEvent(eventid)
    image = event.get()['image']
    venue = event.get()['venue']
    isUserBuyed = isExistByUserAndEvent(session['id'], eventid)
    evaluations = evaluationService.getEventEvaluations(eventid)
    evaluationidCurrentUser = userEventService.getEvaluationId(session['id'],eventid)
    favoritelistidCurrentUser = userService.getFavoriteListId(session['id'])
    eventInFavoriteList = False
    if favoritelistidCurrentUser is not None:
        eventInFavoriteList = favoriteEventsService.isEventInFavoriteList(favoritelistidCurrentUser,eventid)
    
    return render_template("Event.html", event=event, image=image, venue=venue, buyed=isUserBuyed, evaluations = evaluations, evaluationidCurrentUser = evaluationidCurrentUser, favoritelistidCurrentUser = favoritelistidCurrentUser, eventInFavoriteList = eventInFavoriteList)

@login_required
def deleteEvent(eventid):
    event = eventService.getEvent(eventid)
    if event is not None:
        eventService.deleteEvent(eventid)
        return redirect(url_for('events')) 
    return redirect(url_for("event",eventid=eventid))

@login_required
def addEvent():
    if session['role'] == 'admin':
        form = EventForm()
        return render_template("addEvent.html",form=form)
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add events. If you have an admin account please login."])

@login_required
def createEvent():
    if session['role'] == 'admin':
        form = EventForm()
        if form.validate_on_submit():
            title = request.form['title']
            genre = request.form['genre']
            status = request.form['status']
            category = request.form['category']
            price = request.form['price']
            start_date = request.form['date']
            notCertainTime = request.form['notCertainTime'] if 'notCertainTime' in request.form else False
            start_time = request.form['time'] if not notCertainTime else None
            no_start_time = notCertainTime
            venueid = request.form['venue']
            imageid = request.form['image']
            event = Event(None, title, genre, status, category, price, imageid, venueid, start_date, start_time, no_start_time)
            savedid = eventService.saveEvent(event)
            if savedid is not None:
                return redirect(url_for("event",eventid=savedid))
        return render_template("addEvent.html",  form = form ,messages=['Something went wrong with the database'])   
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add events. If you have an admin account please login."])

@login_required
def updateEvent(eventid):
    if session['role'] == 'admin':
        form = EventForm()
        event = eventService.getEvent(eventid)
        form.image.default = event.image.id
        form.venue.default = event.venue.id
        form.status.default = event.status
        form.process()
        event.start_time = str(event.start_time)[0:5]
        return render_template('addEvent.html', form=form, event=event, type='update')
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can update events. If you have an admin account please login."])

@login_required
def saveUpdatedEvent(eventid):
    if session['role'] == 'admin':
        form = EventForm()
        print(request.form['time'])
        if form.validate_on_submit():
            title = request.form['title']
            genre = request.form['genre']
            status = request.form['status']
            category = request.form['category']
            price = request.form['price']
            start_date = request.form['date']
            notCertainTime = request.form['notCertainTime'] if 'notCertainTime' in request.form else False
            start_time = request.form['time'] if not notCertainTime else None
            no_start_time = notCertainTime
            venueid = request.form['venue']
            imageid = request.form['image']
            venue = getVenue(venueid)
            image = getImage(imageid)
            event = Event(None, title, genre, status, category, price, image, venue, start_date, start_time, no_start_time)
            result = eventService.updateEvent(eventid, event)
            if result:
                return redirect(url_for("events"))
        return render_template("addEvent.html",form = form, event = eventService.getEvent(eventid) ,messages=['Something went wrong with the database'], type='update')  
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can update events. If you have an admin account please login."])

