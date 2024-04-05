from flask import Flask, request
from auth import readTokenCredUser
from service_events import gettingCurrentEvents, creatingEvents
from googleapiclient.errors import HttpError
import json

app = Flask(__name__);

@app.route("/api/assistant-pulse-rate", methods=['POST'])
def api():
    try:
        data = json.loads(request.data)
        creds = readTokenCredUser()
        
        if not creds: 
            raise Exception("There is not any token.json credentials file")

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
                }, 200
            )
        else :
            return (
                {
                    "status": 202,
                    "message": "Everything is okay with this patient"
                }, 200
            )
            
    except HttpError as error:
        return {
            "status": 400,
            "error": "HttpError"
         }, 400
    except: return {
         "status": 500,
            "error": "Something wrong happpend in the server"
         }, 500
    
  