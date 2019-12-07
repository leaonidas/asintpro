import requests
import datetime
import pickle
import os.path as path
import json

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
		#if path.exists('database'):
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
		"""else:
			print("nada")
			pass"""

	def dbToList(self):
		#temp = Secretariat()
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
sec = Secretariat()

@app.route('/secretariat')
def sec_info():
	return render_template('secretariat.html', uname = sec.uname, password = sec.password)

@app.route('/submit')
def submit():
	print("User name:", str(request.args.get("user")))
	if request.args.get("user")=='admin' and request.args.get("pass")=='admin':
		return render_template('admin.html')
	elif request.args.get("user")=='' and request.args.get("pass")=='':
		sec.readDB()
		sec.dbToList()
		return render_template('showSec.html', name=sec.name, building=sec.building, schedule=sec.schedule, 
			description=sec.description, size=sec.getSize())
	else:
		return render_template('loginError.html')

@app.route('/admin')
def admin():
	if request.args.get("choice")=="show":
		sec.readDB()
		sec.dbToList()
		return render_template('showSec.html', name=sec.name, building=sec.building, schedule=sec.schedule, 
			description=sec.description, size=sec.getSize())
	elif request.args.get("choice")=="edit":
		return render_template('loginError.html')
	elif request.args.get("choice")=="add":
		return render_template('addSec.html')

@app.route('/add')
def addSec():
	name = request.args.get("name")
	building = request.args.get("building")
	schedule = request.args.get("schedule")
	description = request.args.get("description")
	print(name + ' ' + building + ' ' + schedule + ' ' + description + '\n')

	#JSON stuff
	sec.dictionary['sect'].append({
		"name" : name,
		"building" : building,
		"schedule" : schedule,
		"description" : description
		})
	with open('database.txt', 'w') as outfile:
		json.dump(sec.dictionary, outfile)

	return render_template("admin.html")

@app.route('/show')
def showSec():
	print("In here")

if __name__ == '__main__':
	app.run(debug=True)
