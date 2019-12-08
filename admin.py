import requests
import datetime
import pickle
import os.path as path
import json
import logging

from flask import Flask
from flask import render_template
from flask import request

class Admin:
	def __init__(self):
		self.dictionary = {}
		self.dictionary['sect'] = []
		self.uname='admin'
		self.password='admin'
		self.secname=''
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

	def verifyInDB(self):
		print(self.dictionary)
		for item in self.dictionary['sect']:
			if item["name"] == admin.secname:
				print("Encontrou!\n")
				return True
			else:
				pass
		return False

	def readLogs(self):
		data = ''
		with open('logs.log', 'r') as file:
			data = file.read()
		return data


app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)
admin = Admin()

@app.route("/admin")
def adminPage():
	return render_template('admin.html')

@app.route('/action')
def action():
	if request.args.get("choice")=="service":
		return render_template('loginError.html')
	elif request.args.get("choice")=="edit":
		admin.secname=request.args.get("secname")
		admin.readDB()
		admin.dbToList()
		if admin.verifyInDB() == True:
			return render_template('editSec.html', secname=admin.secname)
		else:
			return render_template('loginError.html')
	elif request.args.get("choice")=="add":
		return render_template('addSec.html')
	elif request.args.get("choice")=="logs":
		logs=admin.readLogs()
		return render_template('logs.html', data=logs)

@app.route('/add')
def addSec():
	admin.readDB()
	admin.dbToList()
	name = request.args.get("name")
	building = request.args.get("building")
	schedule = request.args.get("schedule")
	description = request.args.get("description")
	print(name + ' ' + building + ' ' + schedule + ' ' + description + '\n')

	#JSON stuff
	admin.dictionary['sect'].append({
		"name" : name,
		"building" : building,
		"schedule" : schedule,
		"description" : description
		})
	with open('database.txt', 'w') as outfile:
		json.dump(admin.dictionary, outfile)

	return render_template("admin.html")

@app.route('/edit')
def editSec():
	admin.readDB()
	admin.dbToList()
	for item in admin.dictionary["sect"]:
		if item["name"] == admin.secname:
			item["building"] = request.args.get("building")
			item["schedule"] = request.args.get("schedule")
			item["description"] = request.args.get("description")

	with open('database.txt', 'w') as outfile:
		json.dump(admin.dictionary, outfile)

	return render_template("admin.html")


if __name__ == "__main__":
	app.run(debug=True)

