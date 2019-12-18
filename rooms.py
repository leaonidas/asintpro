import requests
import datetime
import logging
import json
import socket

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
logging.basicConfig(filename='logs.log',level=logging.DEBUG)

@app.route('/')
def room_info():
	#FA1 2448131363667
	roomid=request.data.decode("utf-8", "strict")
	date=datetime.date.today().strftime("%d/%m/%Y")
	uri = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"+str(roomid)+"?day="+str(date)
	r = requests.get(uri)
	print(r.status_code)
	if r.status_code==404:
		return render_template("roomsError.html")
	elif r.status_code==200:
		data = r.json()
		return data

if __name__ == '__main__':
	print("Server running on port: "+str(5002))
	app.run(debug=True, port = 5002)
