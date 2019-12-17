import requests
import datetime
import pickle
import os.path as path
import json
import logging

from flask import Flask
from flask import render_template
from flask import request

import rooms

#Classes for Rooms service
class Lessons:
	def __init__(self):
		self.start=[]
		self.end=[]
		self.course=[]
		self.info=[]

	def less_num(self):
		return len(self.start)

class Generic:
	def __init__(self):
		self.start=[]
		self.end=[]
		self.title=[]

	def gen_num(self):
		return len(self.start)

class Rooms:
	def __init__(self):
		self.room_name=""
		self.campus=""
		self.lessons=Lessons()
		self.generic=Generic()

#Classes for Canteen service
class Canteen:
	def __init__(self):
		self.meal=[]
		self.menu=[]
		self.name=[]
		self.type=[]

	def getSize(self):
		print(len(self.menu))
		return len(self.menu)

#Classes for secretariat service
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

#Classes for admin
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
		print("ADMIN: ",self.dictionary['sect'])

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

#######################
#App starts here      #
#######################

app = Flask(__name__)
admin = Admin()
sec=Secretariat()
logging.basicConfig(filename='logs.log',level=logging.DEBUG)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/action')
def action():
	print('action')
	#Rooms Service
	if request.args.get('choice')=='rooms':
		room = Rooms()
		room_name=request.args.get('room_name')
		date=datetime.date.today().strftime("%d/%m/%Y")
		uri = "http://127.0.0.1:5002"
		r = requests.get(uri, params=room_name)
		print("STATUS CODE: ",r.status_code)
		print(r)
		data = r.json()
		print("Room name:", data["name"])
		room.room_name=data["name"]
		elem = data["topLevelSpace"]
		print("Campus: ", elem["name"])
		room.campus=elem["name"]

		for this in data["events"]:
			if(this["type"]=="LESSON" and this["day"]==date):
				print(this["type"]+"\n"+this["info"]+"\n"+this["start"]+"\n"+this["end"]+"\n"+this["day"])
				course=this["course"]
				course_name=course["name"]
				room.lessons.start.append(this["start"])
				room.lessons.end.append(this["end"])
				room.lessons.course.append(course_name)
				room.lessons.info.append(this["info"])
			elif(this["type"]=="GENERIC" and this["day"]==date):
				print(this["type"]+"\n"+this["start"]+"\n"+this["end"]+"\n"+this["title"]+"\n")
				room.generic.start.append(this["start"])
				room.generic.end.append(this["end"])
				room.generic.title.append(this["title"])
			elif(this["type"]=="TEST"):
				#print(this)
				pass

		return render_template('rooms.html', name=room.room_name, campus=room.campus,
			lessons_course=room.lessons.course, lessons_info=room.lessons.info, lessons_start=room.lessons.start, lessons_end=room.lessons.end, num_lessons=room.lessons.less_num(),
			generic_title=room.generic.title, generic_start=room.generic.start, generic_end=room.generic.end, num_generic=room.generic.gen_num())

	#Canteen Service
	elif request.args.get('choice')=='canteen':
		#Variables
		can = Canteen()
		today = datetime.date.today().strftime("%d/%m/%Y")
		if today[0] == '0':
			today = today[1:]
		#Request
		uri = "http://127.0.0.1:5003/canteen"
		print("URI " + uri)
		r = requests.get(uri)
		print("STATUS CODE: ",r.status_code)
		data = r.json()
		print(data)

		for food in data["meal"]:
			print("\n")
			print("Refeição:", food["type"])
			can.meal.append(food["type"])
			for elem in food["info"]:
				print("Menu: ", elem['menu'])
				print("Prato: ", elem['name'])
				print("Tipo: ", elem['type'])
				can.menu.append(elem["menu"])
				can.name.append(elem["name"])
				can.type.append(elem["type"])

		return render_template('canteen.html', day=today, meal=can.meal, menu=can.menu, name=can.name, mtype=can.type, size=can.getSize())

	#Secretariat Service
	elif request.args.get('choice')=='sec':
		#sec=Secretariat()
		uri = "http://127.0.0.1:5001/secretariat"
		print("URI " + uri)
		r = requests.get(uri)
		print("STATUS CODE: ",r.status_code)
		sec.dictionary = r.json()
		sec.dbToList()
		return render_template('secretariat.html', name=sec.name, building=sec.building, schedule=sec.schedule, 
			description=sec.description, size=sec.getSize())

@app.route('/submit')
def submit():
	print('submit')
	if request.args.get("user")=='admin' and request.args.get("pass")=='admin':
		"""uri = "http://127.0.0.1:5004/admin"
		r = requests.get(uri)"""
		return render_template('admin.html')
	else:
		return render_template('loginError.html')

@app.route('/admin')
def choice():
	if request.args.get("choice")=="service":
		link = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/"
		service = request.args.get("servicename")
		uri = link + service
		print(uri)
		r = requests.get(uri)
		data =  r.json()
		print(r.status_code)
		if r.status_code == 200:
			return render_template("newService.html", data=data, service=service)
		else:
			return render_template("serviceError.html")
	elif request.args.get("choice")=="edit":
		admin.secname=request.args.get("secname")
		admin.readDB()
		admin.dbToList()
		if admin.verifyInDB() == True:
			return render_template('editSec.html', secname=admin.secname)
		else:
			return render_template('editError.html')
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
	print("reached the end")
	return render_template("admin.html")

if __name__ == '__main__':
	app.run(debug=True, port=5000)

