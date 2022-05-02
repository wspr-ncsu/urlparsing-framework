import sys, json
from urllib.parse import urlparse
from urllib3.util.url import parse_url

url = sys.argv[1]
urllib = urlparse(url)
urllib3 = parse_url(url)

def break_urllib(parsed):
	keys = ['scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment']
	res = {}
	for i in range(len(keys)):
		if i < len(parsed):
			res[keys[i]] = parsed[i] if parsed[i] != None else ''
		else:
			res[keys[i]] = ''
	return res

def break_urllib3(parsed):
    keys = ['scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment']
    r = json.dumps(parsed).replace('null', '""')
    r = json.loads(r)
    user = r[1].split(':')
    if len(user) == 2:
        r[1] = user[0]
        r.insert(2, user[1])
    elif len(user) == 1:
        r.insert(2, "")
    else:
        r.insert(2, "cannot break username and password")
    return dict(zip(keys, r))

u1 = break_urllib([urllib.scheme, urllib.username, urllib.password, urllib.hostname, urllib.port, urllib.path, urllib.query, urllib.fragment])
u2 = break_urllib3(urllib3)

print("urllib = ", u1)
print("urllib3 = ", u2)