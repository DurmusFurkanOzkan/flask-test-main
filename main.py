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
		return render_template('main.html')
