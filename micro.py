"""
Rooms: https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131363667?day=21/02/2014
	location(Campi and building)
	timetable
Secretariats: ?
	location
	name
	description
	opening hours
Canteen: https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen
	menu
"""

import requests
import datetime

def canteen():
	today = datetime.date.today().strftime("%d/%m/%Y")
	print("Today bich:", today)
	uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
	r = requests.get(uri)
	print(r.status_code)
	data = r.json()
	for menu in data:
		if menu["day"]==today:
			#print(menu.meal.info.menu)
			for papa in menu["meal"]:
				print("\n")
				print("Refeição:", papa["type"])
				for elem in papa["info"]:
					print("Menu: ", elem['menu'])
					print("Cenas: ", elem['name'])
					print("Tipo: ", elem['type'])

def rooms():
	roomid=2448131363667
	date="21/02/2014"
	uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(roomid)+"?day="+str(date)
	r = requests.get(uri)
	print(r.status_code)
	data = r.json()
	print("Room name:", data["name"])
	elem = data["topLevelSpace"]
	print("Campus: ", elem["name"])

	for this in data["events"]:
		if(this["type"]=="LESSON" and this["day"]==date):
			print(this["type"]+"\n"+this["info"]+"\n"+this["start"]+"\n"+this["end"]+"\n"+this["day"])
			course=this["course"]
			print(course["name"])
		elif(this["type"]=="GENERIC" and this["day"]==date):
			print(this["type"]+"\n"+this["start"]+"\n"+this["end"]+"\n"+this["title"]+"\n")
		elif(this["type"]=="TEST"):
			print(this)
				
def main():
	cantina = canteen()
	room = rooms()

main()	

"""
- secretaria
- que informação e por que datas
- para onde esta informação vai(HTML?)
"""

