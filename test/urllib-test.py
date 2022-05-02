import csv
import json
from urllib.parse import urlparse

file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/results/urllib.csv'

def write_to_csv(parsed_urls):
	with open(file, 'w+') as f:
		header = ['URL', 'Py Urllib']
		writer = csv.writer(f)
		writer.writerow(header)
		try:
			for parsed_url in parsed_urls:
				writer.writerows([parsed_url])
		except Exception as e:
			print("Exception: ", e)

def break_into_key_value_pairs(parsed_url):
	keys = ['scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment']
	res = {}
	for i in range(len(keys)):
		if i < len(parsed_url):
			res[keys[i]] = parsed_url[i] if parsed_url[i] != None else ''
		else:
			res[keys[i]] = ''
	# values = [val if val != None else '' for val in parsed_url]
	# return dict(zip(keys, values))
	return res

if __name__ == '__main__':
	parsed_urls = []
	with open('/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/tests.json', 'r+') as f:
		data = json.load(f)
		urls = data['urls']
	for url in urls:
		try:
			parsed_url = urlparse(url)
			try:
				parsed = [parsed_url.scheme, parsed_url.username, parsed_url.password, parsed_url.hostname, parsed_url.port, parsed_url.path,parsed_url.query, parsed_url.fragment]
			except ValueError as e:
				parsed = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.query, parsed_url.fragment]
			parsed = break_into_key_value_pairs(parsed)
		except Exception:
			parsed = ''
		
		if not parsed:
			parsed = {'scheme': 'Not Parsed. Return: false'}
		parsed_urls.append([url, json.dumps(parsed, indent=1)])
	
	write_to_csv(parsed_urls)
	print("Done!\nCheck file %s for details." % file)