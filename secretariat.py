import requests
import datetime
import pickle
import os.path as path
import json
import logging

from flask import Flask
from flask import render_template
from flask import request

class Secretariat:
	def __init__(self):
		self.dictionary = {}
		self.dictionary['sect'] = []
		self.uname='admin'
		self.password='admin'
		self.name = []
		self.building = []
		self.description = []
		self.schedule = []

	def readDB(self):
		self.dictionary = {}
		self.dictionary['sect'] = []
		with open('database.txt', 'r') as file:
			data = json.load(file)
			for i in data['sect']:
				self.dictionary['sect'].append({
					"name" : i["name"],
					"building" : i["building"],
					"schedule" : i["schedule"],
					"description" : i["description"]
				})
		print(self.dictionary['sect'])

	def dbToList(self):
		self.name = []
		self.building = []
		self.schedule = []
		self.description = []
		for i in self.dictionary['sect']:
			self.name.append(i["name"])
			self.building.append(i["building"])
			self.schedule.append(i["schedule"])
			self.description.append(i["description"])

	def getSize(self):
		return(len(self.name))

app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)
sec = Secretariat()

@app.route('/secretariat')
def sec_info():
	sec.readDB()
	print(sec.dictionary)
	return sec.dictionary

if __name__ == '__main__':
	app.run(debug=True, port=5001)
