import googleapiclient

# Import JSON module
import json

def gettingUserInfot(creds):
    people_service = googleapiclient.discovery.build('people', 'v1', credentials=creds)
    profile = people_service.people().get(resourceName='people/me', personFields='names,emailAddresses,photos').execute()
    return json.dumps(profile)
