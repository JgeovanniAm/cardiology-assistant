import os
import flask
from service_events import gettingCurrentEvents, creatingEvents
from service_profile import gettingUserInfot
from googleapiclient.errors import HttpError
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow

stateApp = {}

app = flask.Flask(__name__)

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json";

# This OAuth 2.0 access scope allows for full read/write access to the
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/userinfo.profile']


# Trasnform google auth credentials to a dictonary
def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes
          }

@app.route("/", methods=['GET'])
def index():
    if 'credentials' not in stateApp:
        return flask.redirect('authorize')
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **stateApp['credentials'])
    # Save credentials back to session in case access token was refreshed.
    stateApp['credentials'] = credentials_to_dict(credentials)
    # Getting info user
    profile = gettingUserInfot(credentials)
    return flask.render_template("index.html", profile=json.loads(profile))

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        # include_granted_scopes='true',
        prompt='select_account'
    )

    # Store the state so the callback can verify the auth server response.
    stateApp['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = stateApp['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  credentials = flow.credentials
  stateApp['credentials'] = credentials_to_dict(credentials)

  return flask.redirect(flask.url_for('index'))


@app.route("/clear")
def clear():
    stateApp.clear()
    return (
            {
                "status": 203,
                "message": "Data cleared"
            }, 203
        )

@app.route("/api/assistant-pulse-rate", methods=['POST'])
def api():
    try:
        data = json.loads(flask.request.data)
  
        if 'credentials' not in stateApp:
            return flask.redirect('authorize')
        
        # Transform dictonary to google auth credential format
        creds = google.oauth2.credentials.Credentials(**stateApp['credentials'])
        events = gettingCurrentEvents(creds)
        
        if(len(events) > 0):
             return {
                "status": 200,
                "message": "There are already plans and events created for the user"
            }, 200
            
        # creating events 
        result = creatingEvents(creds, data.get("value"))
        
        if result:
            return (
                {
                    "status": 201,
                    "message": "We just created plans and events for the user, good job"
                }, 201
            )
        else :
            return (
                {
                    "status": 202,
                    "message": "Everything is okay with this patient"
                }, 202
            )
            
    except HttpError as error:
        return {
            "status": 400,
            "error": "HttpError"
         }, 400
    except Exception as e: 
        print(e)
        return {
            "status": 500,
            "error": "Something wrong happened in the server",
            "details": str(e)
        }, 500

 
if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  app.run('127.0.0.1', 5000, debug=True)
    
  