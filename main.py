from flask import Flask,request,render_template,redirect
import requests
from g4f.client import Client
import pandas as pd
import json
app = Flask(__name__)


@app.route('/',methods = ["GET","POST"])


def home():
	if request.method == "GET":
		return render_template('main.html')
	if request.method == "POST":
		file = request.files['file']
		file.save(file.filename)
		data = pd.read_excel(file)
		i=0
		data=data.values.tolist()
		for item in data:
			url = "https://app.xenforum.net/api/forums.json"

			headers = {
				"Token": "5d4e6cbfdb4c1d9a8e3e6ed4e5a17e05",
				"Shop": "lucasgift.myshopify.com"
			}

			response = requests.get(url, headers=headers)
