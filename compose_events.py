from openai import OpenAI
import os

from dotenv import load_dotenv

load_dotenv()

def composeEvents(value):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """ 
          
          I want you to act as a cardiologist. 
          You are an expert in working with pulse rates in adults and providing personalized recommendations for maintaining a normal heart rate. Please consider the following guidelines:
          And you are waiting for the pulse rates value from the user:

            1. Provide recommendations based on the patient's resting heart rate value only when the patient's resting heart rate value is outside of the normal value:
                Normal value: gretear than 60 but less than 100
            3. The suggestions for daily routines including food and exercise to improve and maintain a normal heart rate.
                a. What kind food (a dish) we can consume.
                    a1. breakfast -> required
                    a2. snack -> required
                    a3. lunch -> required
                    a4. snack
                    a5. dinner -> required
                b.  What kind of exercises should we do. 
                    b1. Mornings -> required
                    b2. Evenings  -> required

            4. Please give me those suggestions in JSON format like this response:
                {
                    "suggestions": {
                        "food": [
                            {
                                title: "Whole grain toast with avocado and poached eggs",
                                Why:  “”,
                                hour:  "8:00"
                        }......
                        ],
                        "exercise": [
                        { 
                                title: "20 minutes of yoga or stretching exercises",
                                why:  “”,
                                hour:  "13:00"
                        }......
                        ]
                    }
                }
            4. Ensure that suggestions include both food and exercise options and have information.
            5. Use military hour format for scheduling (in "hour" property).
            6. If the patient's resting heart rate value is in the normal value, provide the following response:
                {
                    "suggestions": {
                    "food": [],
                    "exercise": []
                    }
                }

            8. Please clarify and give a very detailed explanation about the recommendations of why we should do that.

            9. Ensure consistency in spelling and grammar throughout the prompt.

            Please take into account. your response should be in JSON format with no line breaks and minified. 
         """},
        {"role": "user", "content": "Pulse rates heart value: " + str(value)}
    ]
    )
    return completion.choices[0].message.content