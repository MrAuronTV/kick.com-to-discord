#!/usr/bin/env python3
import pickle
import requests
import json
import time
from urllib import request
from urllib.error import HTTPError
from json import loads

PATH = 'YOUR_PATH' #Path where you stock stream id for doesnt spam discord

try:
    id = pickle.load(open("{}/kick".format(PATH), "rb"))

except (OSError, IOError) as e:
    foo = 3
    pickle.dump(foo, open("{}/kick".format(PATH), "wb"))
    
#ENDPOINT YOUR CHANNEL

ENDPOINT = 'https://kick.com/api/v1/channels/YOUR_CHANNEL'

#USED FLARESOLVERR FOR BYPASS CLOUDFLARE https://github.com/FlareSolverr/FlareSolverr

api_url = "http://FLARESOLVERR_IP:PORT/v1"
headers = {"Content-Type": "application/json"}

data = {
    "cmd": "request.get",
    "url": ENDPOINT,
    "maxTimeout": 60000
}

#GET DATA

r = requests.post(api_url, headers=headers, json=data)

reponse = loads(r.text)['solution']['response']

#CLEANING RESPONSE JSON

r1 = reponse
r2 = r1.replace("<html><head></head><body>", '')

r3 = r2
r4 = r3.replace("</body></html>", '')

#PAYLOAD DISCORD
payload = {
    'username':"YOUR_NAME",
    'content': "YOUR_MESSAGE",
    'avatar_url': "BOT_AVATAR",
    'embeds': [
        {
            'title': loads(r4)['livestream']['session_title'],
            'description': 'DESCRIPTION',  
            'url': 'YOUR_KICK_URL',
            "color": 834567, #color embed
	    'author': {'name': 'YOUR_NAME'},
            'timestamp': loads(r4)['livestream']['created_at'],
            "image": {"url": loads(r4)['livestream']['thumbnail']['url']}, 
	    "fields": [
      		{
       		 "name": "Game",
	        "value": loads(r4)['livestream']['categories'][0]['name'],
		"inline": True,
      		},
      		{
        	"name": "Viewers",
        	"value": loads(r4)['livestream']['viewers'],
       		"inline" : True,
            }
            ]
        },
    ]
}

#WEBHOOK DISCORD

WEBHOOK_URL = 'YOUR_WEBHOOK_URL'

headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
}

req = request.Request(url=WEBHOOK_URL,
                      data=json.dumps(payload).encode('utf-8'),
                      headers=headers,
                      method='POST')                    
                      
if loads(r4)['livestream'] is not None:
    if loads(r4)['livestream']['id'] != id:
        response = request.urlopen(req)
        
with open('{}/kick'.format(PATH), 'wb') as f:
    pickle.dump(loads(r4)['livestream']['id'], f)
