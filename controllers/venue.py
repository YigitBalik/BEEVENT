# fmt: off
import io
import json
import sys
from werkzeug.utils import redirect, secure_filename
sys.path.append('..\\itudb2130')
from models import Venue
import services.venue as venueService
from flask import current_app, render_template, request
from flask_login.utils import *
from forms import LoginForm, VenueForm, UploadFile
# fmt: on

@login_required
def getVenues():
    if session['role'] == 'admin':
        venues = venueService.getVenues()
        return render_template('venues.html', venues = venues)
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can manage venues. If you have an admin account please login."])

@login_required
def deleteVenue(venueid):
    if session['role'] == 'admin':
        Venue = venueService.getVenue(venueid)
        if Venue is not None:
            venueService.deleteVenue(venueid)
            return redirect(url_for('venues'))
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can delete a venue. If you have an admin account please login."])

@login_required
def addVenue():
    if session['role'] == 'admin':
        form = VenueForm()
        fileUploader = UploadFile()
        return render_template("addVenue.html", form=form, fileUploader=fileUploader)
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add venues. If you have an admin account please login."])

@login_required
def createVenue():
    if session['role'] == 'admin':
        form = VenueForm()
        fileUploader = UploadFile()
        if form.validate_on_submit():
            name = request.form['name']
            country = request.form['country']
            city = request.form['city']
            address = request.form['address']
            timezone = request.form['timezone']
            venue = Venue(None, name, country, city, address, timezone)
            venueid = venueService.saveVenue(venue)
            if venueid is not None:
                return redirect(url_for('venues'))
        return render_template("addVenue.html",form = form , fileUploader=fileUploader) 
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add venues. If you have an admin account please login."])

ALLOWED_EXTENSIONS = {'json'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def correctSize(venue):
    result = False
    try:
        name = 5 <= len(venue["name"]) <= 100
        country = 5 <= len(venue["country"]) <= 50
        city = 5 <= len(venue["city"]) <= 50
        address =  5 <= len(venue["address"]) <= 100
        timezone = 5 <= len(venue["timezone"]) <= 50
        result = name and country and city and address and timezone
    except (Exception):
        result = False
    return result

@login_required
def createVenueFromJSON():
    if session['role'] == 'admin':
        form = VenueForm()
        fileUploader = UploadFile()
        if fileUploader.validate_on_submit():
            filename = secure_filename(fileUploader.file.data.filename)
            if allowed_file(filename):
                try: 
                    fstream = fileUploader.file.data.stream
                    venues_bytes = fstream.read()
                    venues_json = venues_bytes.decode('utf8').replace("'",'"')
                    venues = json.loads(venues_json)
                    if venues_json[0] == '[':
                        lastSaved = "Nothing saved"
                        for venue in venues:
                            if correctSize(venue):
                                venueService.saveVenue(Venue(None, venue["name"], venue["country"], venue["city"], venue["address"], venue["timezone"]))
                                lastSaved = venue["name"] 
                            else:
                                print(lastSaved)
                                return render_template("addVenue.html",form = form , fileUploader=fileUploader, fileError="Invalid size", last=lastSaved) 
                    else:
                        if correctSize(venues):
                            venueService.saveVenue(Venue(None, venues["name"], venues["country"], venues["city"], venues["address"], venues["timezone"]))
                        else:
                            return render_template("addVenue.html",form = form , fileUploader=fileUploader, fileError="Invalid size") 
                    return redirect(url_for('venues'))
                except (Exception):
                    return render_template("addVenue.html",form = form , fileUploader=fileUploader, fileError="Incorrect JSON format, please correct it.") 
            else:
                return render_template("addVenue.html",form = form , fileUploader=fileUploader, fileError="File type must be JSON.") 
        return render_template("addVenue.html",form = form , fileUploader=fileUploader, fileError="Invalid inputs.") 
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add venues. If you have an admin account please login."])

@login_required
def updateVenue(venueid):
    if session['role'] == 'admin':
        form = VenueForm()
        venue = venueService.getVenue(venueid)
        return render_template('addVenue.html', form=form, venue=venue, type='update')
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add venues. If you have an admin account please login."])

@login_required
def saveUpdatedVenue(venueid):
    if session['role'] == 'admin':
        form = VenueForm()
        if form.validate_on_submit():
            name = request.form['name']
            country = request.form['country']
            city = request.form['city']
            address = request.form['address']
            timezone = request.form['timezone']
            venue = Venue(None, name, country, city, address, timezone)
            result = venueService.updateVenue(venueid, venue)
            if result:
                return redirect(url_for("venues"))
        return render_template("addVenue.html",form = form, venue = venueService.getVenue(venueid) ,messages=['Something went wrong with the database'], type='update')  
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add images. If you have an admin account please login."])
