import requests
import datetime
import logging
import json

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)

@app.route('/')
def room_info():
	roomid=2448131363667
	date=datetime.date.today().strftime("%d/%m/%Y")
	uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(roomid)+"?day="+str(date)
	r = requests.get(uri)
	print(r.status_code)
	data = r.json()
	print(data)
	return data

if __name__ == '__main__':
	print("server on "+str(5002))
	app.run(debug=True, port = 5002)
