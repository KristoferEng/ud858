Conference Application

What is it?
———————————
The Conference application is the fourth project in the Full Stack Web Developer Nanodegree. The application is designed to use the Google Endpoints API. Users have the ability to create and retrieve conferences and sessions.


The Latest Version
——————————————————
The latest version of the application can be found at https://github.com/slikqaz/ud858/final_project/00_conference_central.


Configuration Instructions
——————————————————————————
The libraries and APIs used are: Google App Engine/Endpoints, ProtoRPC, webapp2, datetime, httplib, json, os, time, and uuid.

Installation and Run Instructions
—————————————————————————————————
0. Download the Google App Engine SDK.
1. Update the value of `application` in `app.yaml` to the app ID you have registered in the App Engine admin console and would like to use to host your instance of this sample.
2. Update the values at the top of `settings.py` to reflect the respective client IDs you have registered.
3. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
4. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address.
5. Deploy your application.

Operating Instructions
——————————————————————
To test APIs via web app (Only conference functionality per instructions):

	Home Page: http://localhost:8080/ or https://<Your client id>.appspot.com/

To test APIs:

	API: http://localhost:8080/_ah/api/exploroer or https://<Your client id>.appspot.com/_ah/api/explorer

Task 1 - Explain your design choices
____________________________________
Created a new Session class from ndb.model. Since every session belonged to a Conference, made every session's parent the Conference from the websafeConferenceKey that is passed in on creation. A new class was necessary since a session required many (7) properties.

Task 2 - Wishlist
_________________
Changed the Profile to include sessionKeysWishList, which is a list of keys of the sessions a user wants to go to. Using the API, a user can put the session key and it will be added to the sessionKeysWishList. Using the API, a user can retrieve all sessions in their wishlist.

Task 3 - 2 additional queries and problem
_________________
Created two Session queries to find sessions less than a certain duration and find ones with a highlight desired.

The query problem is that you can't filter by too many inequalities otherwise datastore throws an error. So, I just made one inequality query and an equality query. If the entity in the equality query is in the inequality query, I would not add it otherwise I would.

Task 4 - Memcache
_________________
If the speaker comes up more than once, then I memcached it and created an endpoint with Memcache for faster response time.
