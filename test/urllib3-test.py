import csv
import json
from urllib3.util.url import parse_url

file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/results/urllib3.csv'

def write_to_csv(parsed_urls):
    with open(file, 'w+') as f:
        header = ['URL', 'Py Urllib3']
        writer = csv.writer(f)
        writer.writerow(header)
        try:
            for parsed_url in parsed_urls:
                writer.writerows([parsed_url])
        except Exception as e:
            print("Exception: ", e)

def break_into_key_value_pairs(parsed_url):
    keys = ['scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment']
    r = json.dumps(parsed_url).replace('null', '""')
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

if __name__ == '__main__':
    parsed_urls = []
    with open('/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/tests.json', 'r+') as f:
        data = json.load(f)
    urls = data['urls']

    for url in urls:
        try:
            parsed = parse_url(url)
        except Exception:
            parsed = ''

        if not parsed:
            parsed = {'scheme': 'Not Parsed. Return: false'}
        else:
            parsed = break_into_key_value_pairs(parsed)
        parsed_urls.append([url, json.dumps(parsed, indent=1)])
        
    write_to_csv(parsed_urls)
    print("Done!\nCheck file %s for details." % file)