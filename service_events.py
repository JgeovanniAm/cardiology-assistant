import uuid
from datetime import date
from googleapiclient.discovery import build
from compose_events import composeEvents

# Import JSON module
import json


def gettingCurrentEvents(creds):
  # Call the Calendar API  
  service = build("calendar", "v3", credentials=creds)
  
  # Getting today's events 
  events_result = (
    service.events().list(
          calendarId="primary",
          # etag="cardiology-assistant",
          timeMax=str(date.today())+"T23:59:00.00-06:00",
          timeMin=str(date.today())+"T00:00:00.00-06:00",
          # timeZone= 'America/Costa_Rica',
          singleEvents=True,
          orderBy="startTime",
      ).execute()
  )
  
  # Destructuring the dictionary and getting items props
  allEvents = events_result.get("items")
  
  cardiologyEvents = []
  
  for event in allEvents :
    if "Cardiology Assistant" in event.get("summary"):
      cardiologyEvents.append(event)
  
  return cardiologyEvents


def creatingEvents(creds, body):
  # Call the Calendar API  
  service = build("calendar", "v3", credentials=creds)
  
  result = json.loads(composeEvents(body))
  
  print(result)
    
  suggestionsFood = result.get("suggestions").get("food")
  suggestionsExercises = result.get("suggestions").get("exercise")
  
  if len(suggestionsFood) == 0 or len(suggestionsExercises) == 0:
    return False
  
  # suggestionsExercises = [{'title': 'Cardio workout (e.g., jogging, cycling)', 'why': 'Cardio exercises help improve heart health and lower the resting heart rate.', 'hour': '07:00'}, {'title': 'Strength training (e.g., weight lifting)', 'why': 'Building muscle helps increase metabolism and overall heart health.', 'hour': '18:00'}]
  # suggestionsFood =[{'title': 'Oatmeal with fresh fruits and nuts', 'why': 'Oatmeal is a good source of fiber and fruits provide essential vitamins and minerals for heart health.', 'hour': '07:00'}, {'title': 'Greek yogurt with berries', 'why': 'Greek yogurt is high in protein and berries are rich in antioxidants, both beneficial for heart health.', 'hour': '10:00'}, {'title': 'Grilled chicken salad with vinaigrette dressing', 'why': 'Lean protein from chicken and nutrients from veggies make this a heart-healthy lunch option.', 'hour': '13:00'}, {'title': 'Mixed nuts or a piece of fruit', 'why': 'Nuts are rich in healthy fats and fruits provide a quick energy boost without spiking blood sugar levels.', 'hour': '16:00'}, {'title': 'Baked salmon with quinoa and steamed vegetables', 'why': 'Salmon is a great source of omega-3 fatty acids, quinoa is high in protein, and vegetables are rich in vitamins and minerals.', 'hour': '19:00'}]
  
  batch = service.new_batch_http_request()
  
  for exercise in suggestionsExercises:
    event = {
      'summary': "Cardiology Assistant 🫀 - Exercising Time",
      'description':f'<h3>{exercise.get("title")}</h3><p>{exercise.get("why")}</p>',
      'start': {
        'dateTime': str(date.today())+'T'+ exercise.get("hour")+':00-06:00',
        'timeZone': 'America/Costa_Rica',
      },
      'colorId':"3",
      'end': {
        'dateTime': str(date.today())+'T'+ exercise.get("hour")+':00-06:00',
        'timeZone': 'America/Costa_Rica',
      },
      'sequence': 0,
      'reminders': {'useDefault': False}, 'eventType': 'default'
    }
    
    batch.add(service.events().insert(calendarId='primary', body=event))
  
  for food in suggestionsFood:
    event = {
      'summary': "Cardiology Assistant 🫀 - Eating Time",
      'description':f'<h3>{food.get("title")}</h3><p>{food.get("why")}</p>',
      'colorId': "9",
      'start': {
        'dateTime': str(date.today())+'T'+food.get("hour")+':00-06:00',
        'timeZone': 'America/Costa_Rica',
      },
      'end': {
        'dateTime': str(date.today())+'T'+food.get("hour")+':00-06:00',
        'timeZone': 'America/Costa_Rica',
      },
      'sequence': 0,
      'reminders': {'useDefault': False}, 'eventType': 'default'
    }
    
    batch.add(service.events().insert(calendarId='primary', body=event))

  # will call all the batches and execute them.
  result = batch.execute();
  
  return True
  

