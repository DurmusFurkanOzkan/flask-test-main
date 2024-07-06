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
			forum_id = ''
			for forum_main in response.json()['forums']:
				for forum_child in forum_main['children']:
					if item[1] == forum_child['title']:
						print(forum_child['title'])
						forum_id = forum_child['id']

			client = Client()
			content = "Please write a paragraph at least 1500 english (not chinese) word with answering " + item[0] + "? this question"

			while True:
				response = client.chat.completions.create(
				model="gpt-3.5-turbo",
				messages=[{"role": "user", "content": content}],
				)
				if response.choices[0].message.content.split(",")[0]!="sorry" and response.choices[0].message.content.split(".")[0]!="I apologize for the mistake earlier":
					break
			destination1 = "https://lucasgift.com/pages/search-results-page?q=" + item[3]
			destination2 = "https://lucasgift.com/pages/search-results-page?q=" + item[3]
			description1 = "Best " + item[3] +  "collection"
			description2 = "Best " + item[3] + "collection"
			link1 ='<a href="{0}">{1}</a>'.format(destination1, description1)
			link2 ='<a href="{0}">{1}</a>'.format(destination2, description2)
			main_content=item[0] +"?" +	"<p>If you don't feel like reading much now and want to see some gift items, you can jump on to seeing " + item[1] + " directly, check out:" + link1 + "</p>" + "<p>" +  response.choices[0].message.content +  "</p>" + "<p>Thank you so much for reading all the way down here and if you want to see some gift items, you can jump on to seeing " + item[1] + "in our website, check out:" + link2 + "</p>"
			"""data[i][0] = response.choices[0].message.content"""
			"""i=i+1"""
			print(data)
			url = "https://app.xenforum.net/api/topics/create.json"
			data2 = {'user_id': '170128', 'forum_id': forum_id, 'title': item[0],'content':main_content}

			headers = {'Content-type': 'application/json', 'Accept': 'text/plain',"Token": "5d4e6cbfdb4c1d9a8e3e6ed4e5a17e05","Shop": "lucasgift.myshopify.com"}
			r = requests.post(url, data=json.dumps(data2), headers=headers)
		return render_template('main.html')
