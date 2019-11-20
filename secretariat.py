import requests
import datetime

from flask import Flask
from flask import render_template
from flask import request


class Secretariat:
	def __init__(self):
		self.data=[]

app = Flask(__name__)

@app.route('/secretariat')
def sec_info():


#doesn't do shit yet
