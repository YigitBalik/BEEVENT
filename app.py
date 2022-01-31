import os
from flask import Flask
from flask_login import LoginManager
from controllers.event import *
from controllers.image import *
from controllers.venue import *
from controllers.user import *
from controllers.userEvent import *
from controllers.evaluation import *
from controllers.favoriteList import *
from controllers.favoriteEvents import *

app = Flask(__name__)
app.secret_key = "in development"
app.config['UPLOAD_FOLDER'] = 'Uploads/'

lm = LoginManager()
lm.init_app(app)
lm.login_view = "/"

@lm.user_loader
def load_user(userid):
    return getUser(userid)
# App url rules

# Account
app.add_url_rule('/',endpoint='login',view_func=login,methods=['GET'])
app.add_url_rule('/register', endpoint='register',view_func=register, methods=['GET'])
app.add_url_rule('/',view_func=loginUser,methods=['POST'])
app.add_url_rule('/register', view_func=registerUser, methods=['POST'])
app.add_url_rule('/logout', endpoint='logout', view_func=logout, methods=['GET'])
app.add_url_rule('/users', endpoint="users",view_func=getUsers,methods=['GET'])
app.add_url_rule('/user/delete/<int:userid>', endpoint='deleteUser', view_func=deleteUser, methods=['GET'])
app.add_url_rule('/user/assign/<int:userid>/<int:role>', endpoint='assignRole', view_func=assignRole, methods=['POST'])

# Event
app.add_url_rule('/events', endpoint='events', view_func=getEvents, methods=['GET'])
app.add_url_rule('/event/<int:eventid>', endpoint='event', view_func=getEvent, methods=['GET'])
app.add_url_rule('/event/delete/<int:eventid>', endpoint='deleteEvent', view_func=deleteEvent, methods=['GET'])
app.add_url_rule('/event/add/', endpoint="addEvent", view_func=addEvent ,methods=['GET'])
app.add_url_rule('/event/add/', view_func=createEvent, methods=['POST'])
app.add_url_rule('/event/update/<int:eventid>', endpoint="updateEvent", view_func=updateEvent, methods=['GET'])
app.add_url_rule('/event/update/<int:eventid>', view_func=saveUpdatedEvent, methods=['POST'])

# Image
app.add_url_rule('/images',endpoint='images',view_func=getImages,methods=['GET'])
app.add_url_rule('/image/delete/<int:imageid>', endpoint='deleteImage', view_func=deleteImage, methods=['GET'])
app.add_url_rule('/image/add/', endpoint="addImage", view_func=addImage ,methods=['GET'])
app.add_url_rule('/image/add/', view_func=createImage, methods=['POST'])
app.add_url_rule('/image/update/<int:imageid>', endpoint='updateImage', view_func=updateImage, methods=['GET'])
app.add_url_rule('/image/update/<int:imageid>', view_func=saveUpdatedImage, methods=['POST'])

# Venue
app.add_url_rule('/venues', endpoint='venues', view_func=getVenues, methods=['GET'])
app.add_url_rule('/venue/delete/<int:venueid>', endpoint='deleteVenue',view_func=deleteVenue, methods=['GET'])
app.add_url_rule('/venue/add/', endpoint='addVenue', view_func=addVenue, methods=['GET'])
app.add_url_rule('/venue/add/', view_func=createVenue, methods=['POST'])
app.add_url_rule('/venue/upload/', endpoint="venueFileUpload", view_func=createVenueFromJSON, methods=['POST'])
app.add_url_rule('/venue/update/<int:venueid>', endpoint='updateVenue', view_func=updateVenue, methods=['GET'])
app.add_url_rule('/venue/update/<int:venueid>', view_func=saveUpdatedVenue, methods=['POST'])

# User_Event
app.add_url_rule('/userEvent/add/<int:eventid>', endpoint="addUserEvent", view_func=addUserEvent, methods=['POST'])
app.add_url_rule('/userEvents', endpoint="userEvents", view_func=getUserEvents, methods=['GET'])

# User Profile
app.add_url_rule('/myprofile',endpoint='profile',view_func=getUserProfile, methods=['GET'])
app.add_url_rule('/myprofile/edit',endpoint='editUserProfile',view_func=updateUserProfile, methods=['GET'])
app.add_url_rule('/myprofile/edit',view_func=saveUpdatedUserProfile, methods=['POST'])
app.add_url_rule('/myprofile/changePassword',endpoint='changePassword',view_func=changeUserPassword, methods=['GET'])
app.add_url_rule('/myprofile/changePassword',view_func=saveChangedUserPassword, methods=['POST'])

#Evaluation
app.add_url_rule('/evaluate/<int:eventid>', endpoint="addEvaluation", view_func=addEvaluation, methods=['GET'])
app.add_url_rule('/evaluate/update/<int:eventid>/<int:evaluationid>', endpoint="updateEvaluation", view_func=updateEvaluation, methods=['GET'])
app.add_url_rule('/evaluate/<int:type>/<int:eventid>', view_func=saveEvaluation, methods=['POST'])
app.add_url_rule('/evaluate/delete/<int:eventid>/<int:evaluationid>', endpoint="deleteEvaluation", view_func=deleteEvaluation, methods=['POST'])

#Favorite List
app.add_url_rule('/favoriteLists/myfavoriteList', endpoint="favoriteList", view_func=getFavoriteList, methods=['GET'])
app.add_url_rule('/favoriteLists/myfavoriteList/create', endpoint="createFavoriteList", view_func=createFavoriteList, methods=['GET'])
app.add_url_rule('/favoriteLists/myfavoriteList/create', view_func=saveCreatedFavoriteList, methods=['POST'])
app.add_url_rule('/favoriteLists/myfavoriteList/update', endpoint="updateFavoriteList", view_func=updateFavoriteList, methods=['GET'])
app.add_url_rule('/favoriteLists/myfavoriteList/update', view_func=saveUpdatedFavoriteList, methods=['POST'])
app.add_url_rule('/favoriteLists/myfavoriteList/delete/<int:favoriteListID>', view_func=deleteFavoriteList, methods=['POST'])
app.add_url_rule('/favoriteLists/publicFavoriteLists', endpoint="publicFavoriteLists", view_func=getPublicFavoriteLists, methods=['GET'])


#Favorite Events
app.add_url_rule('/favoriteEvents/add/<int:favoriteListID>/<int:eventid>', endpoint='addEventToFavoriteEvents', view_func=addEventToFavoriteEvents, methods=['POST'])
app.add_url_rule('/favoriteEvents/<int:favoriteListID>', endpoint="getFavoriteEvents", view_func=getFavoriteEvents, methods=['GET'])
app.add_url_rule('/favoriteEvents/delete/<int:favoriteListID>/<int:eventid>', endpoint="deleteEventFromFavoriteEvents", view_func=deleteEventFromFavoriteEvents, methods=['POST'])
app.add_url_rule('/favoriteEvents/deleteInList/<int:eventid>', endpoint="deleteEventFromFavoriteEventsInList", view_func=deleteEventFromFavoriteEventsInFavList, methods=['POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
