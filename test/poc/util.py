from urllib3.util.url import parse_url

def is_valid(url):
	'''
	Verify url belongs to whitelisted domain and secure scheme + port
	'''
	parsed = parse_url(url)
	if parsed.scheme == 'https' and parsed.hostname == 'example.com' and parsed.port == 443:
		print("URL valid.")
		return 1
	else:
		return 0