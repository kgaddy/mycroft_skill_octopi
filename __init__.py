from os.path import dirname, join
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import requests
import json

logger = getLogger(__name__)

__author__ = 'kgaddy'


class PrinterStatusSkill(MycroftSkill):
 
    def __init__(self):
        super(PrinterStatusSkill, self).__init__(name="PrinterStatusSkill")

    def initialize(self):
        intent = IntentBuilder("PrinterStatusIntent").require("PrinterStatusCommand").build()
        self.register_intent(intent, self.handle_intent)

    def handle_intent(self, message):
	API_KEY = "YOUR_KEY_HERE"

	headers = {
    		'Accept': 'application/json',
    		'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary',
    		'X-Api-Key': API_KEY
	}

	uri = 'http://octopi.local/api/printer'
	
        state = requests.get(uri, headers=headers)
	logger.debug(state)
	data = json.loads(state.text)
	currentState = data['state']['text']
	nozzel = data['temperature']['tool0']['actual']
	bed = data['temperature']['bed']['actual']
	self.speak("The Printer is currently "+str(currentState)+".")
	if currentState == "Printing":
		jobUri = 'http://octopi.local/api/job'
		job = requests.get(jobUri, headers=headers)
		jobData = json.loads(job.text)
		jpercent = jobData['progress']['completion']
		ipercent = int(float(jpercent))
		self.speak("The print is "+str(ipercent) +"percent complete.")
        self.speak("The nozzel temperature is "+ str(nozzel)+".")
	self.speak("And the bed temperature is "+ str(bed)+".")
    def stop(self):
        pass


def create_skill():
    return PrinterStatusSkill()
