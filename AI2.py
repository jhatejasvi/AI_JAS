from __future__ import print_function
import speech_recognition as s
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://mail.google.com/']






sr=s.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
   

 #engine.say('hello i m jessica ')
 #engine.say('how can i please you today')
 engine.say(text)
 engine.runAndWait()

def take_command():

   try:
      
    with s.Microphone(1) as m:
      print('clearing background noises') 
      sr.adjust_for_ambient_noise(m,duration=1)
      print('i m listening you.....') 
      audio=sr.listen(m)
      query=sr.recognize_google(audio,language='eng-in')
      query=query.lower()
      if 'jessica'or "jess" in query:
          query=query.replace('jessica','')
      print(query)
              
   except:
      pass
   return query


def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
   try:
     message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
     print(f"Message Id: %s {message['id']}")
     return message
   except HttpError as  error:
     print(f'An error occurred: {error}') 




def run_alexa():
   query=take_command()
   #print(query)
   if 'play' in query:
      song = query.replace('play', '')
      talk('playing'+ song)
      pywhatkit.playonyt(song)

  
    
   elif 'time' in query:
       time = datetime.datetime.now().strftime('%I:%M %p')
       print(time)
       talk('Current time is ' + time) 
       #if ("launch" in cmd or "run" in cmd or "create" in cmd or "make" in cmd)  and "pod" in cmd:   
   elif ('who is' in query or 'what is' in query or 'tell me about' in query):
        person = query.replace('who is' or 'what is' or 'tell me about', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)   
   elif 'joke' in query:
        talk(pyjokes.get_joke())
   #elif 'schedule' in query:
    #    talk('what   is   your   schedule')
    #   
   
   elif 'mail' in query:
        talk("hello          welcome to my mail service") 
        #talk('whom you want to send the mail.')
        # to = take_command()
        talk('what is the subject?')
        subject=take_command()
        talk('what should i say?')
        message_text=take_command()
        message = MIMEText(message_text)
        message = create_message("me","gaganyoutb4@gmail.com",subject,message_text)
        print(message)
        #service = build('gmail', 'v1', credentials=creds)
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
             flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        try:
             service = build('gmail', 'v1', credentials=creds)
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}') 

      
        send_message(service,"me",message)
      
    

   elif 'assistant' in query:
      talk('yes i know i am your beautiful assistent but my name is jessica ...ammmm by the way you can call me jess')     

   else:
        talk('Please say the command again.') 

while True:          
       
   run_alexa() 



    