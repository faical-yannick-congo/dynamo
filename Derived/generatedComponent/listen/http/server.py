from flask import Flask
from flask import request, Response
from flask.ext.api import status
import json
from datetime import datetime, date
import sys
import os

app = Flask(__name__)

def schedule(content):
	stamp = "{:%Y%m%d%H%M%S%f}".format(datetime.now())
	data = {}
	data["stamp"] = stamp
	data["component"] = content["component"]
	data["protocol"] = "HTTP"
	data["status"] = "scheduled"
	data["message"] = {}
	data["message"]["head"] = content["head"]
	data["message"]["data"] = content["data"]
	# print "Data: "+str(data)
	# print os.system("pwd")
	with open("../requests/"+stamp+".request","w") as request_file: # Add ../ if testing from http folder.
		request_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
	return "Success: Request scheduled as ["+stamp+".request]"

@app.route('/dynamicderivation/v1/process/gen/comp00/', methods=['POST'])
def process():
	if request.method == 'POST':
		data = json.loads(request.data)
		response = schedule(data)
		# print "Response: "+str(response)
		return Response(response, status.HTTP_200_OK)

if __name__ == '__main__':
	HOST, PORT = "localhost", 5000
	if len(sys.argv) == 3:
		HOST, PORT = sys.argv[1], int(sys.argv[2])
	app.run(host=HOST, port=PORT)