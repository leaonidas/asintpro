import requests
import datetime
import logging

from flask import Flask
from flask import render_template
from flask import request

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

app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)

@app.route('/rooms')
def room_info():
	room = Rooms()
	roomid=2448131363667
	#date="21/02/2014"
	date=datetime.date.today().strftime("%d/%m/%Y")
	uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(roomid)+"?day="+str(date)
	r = requests.get(uri)
	print(r.status_code)
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

if __name__ == '__main__':
	app.run(debug=True)


#objecto de objectos ->listas