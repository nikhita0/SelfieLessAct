#!flask/bin/python
#import pandas as pd
from flask import Flask, jsonify,abort
app = Flask(__name__)
import csv
import time
import hashlib
import re
from flask import make_response
import datetime
from flask import request

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)




#4 Add a user
@app.route('/api/v1/users', methods=['POST'])
def add_user():
	if not request.json or not 'name' in request.json:
		abort(400)
	data={'username':request.json['name'],
		'pass':request.json['pass']
		}
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			if(row[0]==data["username"]):
				flag=1
			if(flag==1):
				return make_response(jsonify(),400)
	hexval=data["pass"]
	pattern = re.compile(r'\b[0-9a-f]{40}\b')
	match = re.match(pattern, hexval)
	f=0
	try:
		if(match.group(0)==hexval):
			f=1
	except:			
		pass
	if(f==1):
		with open('users.csv', 'a') as csvFile:
			writer = csv.writer(csvFile)
			r=[data["username"],data["pass"]]
			writer.writerow(r)
		return jsonify({}),201 
	else:
		return jsonify(),400


#5 Delete a user
@app.route('/api/v1/users/<username>', methods=['DELETE'])
def delete_user(username):
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		flag=0
		for row in csv_reader:
			#print(row)
			if(row[0]==username):
				flag=1
		if(flag==0):
			return make_response(jsonify(),400)
	tl=[]	
	with open('users.csv', 'rb') as f:
		reader = csv.reader(f)
		l = list(reader)
		for line in l:
			if(line[0]!=username):
				tl.append(line)	
	print(tl)
	with open("users.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(tl)
	return jsonify({}), 200


#List all users
@app.route('/api/v1/users',methods=['GET'])
def list_all_users():
	l=[]
	with open('users.csv') as csv_file:
		csv_reader = csv.reader(csv_file)
		for row in csv_reader:
			l.append(row[0])
	return jsonify(l)



if __name__ == '__main__':
    app.run(debug=True,host="127.0.0.1",port=5000)
