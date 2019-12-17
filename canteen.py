import requests
import datetime
import logging

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)

@app.route('/canteen')
def show_menu():
	js={}
	today = datetime.date.today().strftime("%d/%m/%Y")
	if today[0] == '0':
		today = today[1:]
	uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/canteen"
	r = requests.get(uri)
	print(r.status_code)
	data = r.json()
	for menu in data:
		if menu["day"]==today:
			js=menu
	print(js)
	return js

if __name__ == '__main__':
	app.run(debug=True, port=5003)