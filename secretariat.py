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

app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)
sec = Secretariat()

@app.route('/secretariat')
def sec_info():
	sec.readDB()
	print(sec.dictionary)
	return sec.dictionary

if __name__ == '__main__':
	print("Server running on port: "+str(5001))
	app.run(debug=True, port=5001)
