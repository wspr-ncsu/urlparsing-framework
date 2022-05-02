import sys, json
import util
import subprocess
import requests
from urllib.parse import urlparse

url = sys.argv[1]

if util.is_valid(url):
	parsed = urlparse(url)
	remote = 'http://' + parsed.hostname + ':' + str(parsed.port) + parsed.path
	
	# Upload file
	file = {'file': open(parsed.path)}
	response = requests.post(remote, files=file)
	print("File uploaded at URL: ", response.url)
	
	# Download file
	response = requests.get(remote)
	print("File downloaded from URL: ", response.url)
else:
	print("Invalid Request.")