import requests
import datetime
import logging

from flask import Flask
from flask import render_template
from flask import request

class Canteen:
	def __init__(self):
		self.meal=[]
		self.menu=[]
		self.name=[]
		self.type=[]

	def getSize(self):
		print(len(self.menu))
		return len(self.menu)

app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)

@app.route('/canteen')
def show_menu():
	can = Canteen()
	today = datetime.date.today().strftime("%d/%m/%Y")
	if today[0] == '0':
		today = today[1:]
	uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
	r = requests.get(uri)
	print(r.status_code)
	data = r.json()
	for menu in data:
		print(menu)
		if menu["day"]=="6/12/2019":
			for papa in menu["meal"]:
				print("\n")
				print("Refeição:", papa["type"])
				can.meal.append(papa["type"])
				for elem in papa["info"]:
					print("Menu: ", elem['menu'])
					print("Prato: ", elem['name'])
					print("Tipo: ", elem['type'])
					can.menu.append(elem["menu"])
					can.name.append(elem["name"])
					can.type.append(elem["type"])

	return render_template('canteen.html', day=today, meal=can.meal, menu=can.menu, name=can.name, mtype=can.type, size=can.getSize())

if __name__ == '__main__':

	app.run(debug=True)