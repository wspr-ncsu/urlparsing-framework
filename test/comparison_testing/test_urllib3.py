from urllib3.util.url import parse_url
import json
import argparse
from helper import *

lib_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/'
diff_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/comparison_testing/diffs/diff_urllib3_'

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
    parser = argparse.ArgumentParser("Testing Urllib3")
    parser.add_argument('--lib', action='store', dest='lib', type=str, required=True)
    lib = parser.parse_args().lib
    diff_file = diff_file + lib + '.csv'
    lib_file = lib_file + lib + '.json'

    with open(lib_file, 'r+') as f:
        data = json.load(f)
    urls = data['urls']

    total_count = 0
    high_severity_diffs = []
    low_severity_diffs = []

    for url in urls:
        total_count += 1
        input_url = url['input']
        try:
            parsed = parse_url(input_url)
        except Exception as e:
            parsed = ['Not Parsed. Error: %s' % e]
            
        parsed = break_into_key_value_pairs(parsed)
        if not url['expected_output']:
            url['expected_output'] = {'scheme': 'Not Parsed. Return: false'}
        
        severity, diff = compare_parser_outputs(input_url, parsed, url['expected_output'])
        
        if not diff:
            continue
        if severity == 10:
            high_severity_diffs.append(diff)
        else:
            low_severity_diffs.append(diff)
        
    diff_count = len(high_severity_diffs) + len(low_severity_diffs)
    print("Out of total %s found %s differences in parsing.\nHigh Severity = %s\nLow Severity = %s\nCheck file %s for details." % (total_count, diff_count, len(high_severity_diffs), len(low_severity_diffs), diff_file))
    write_to_csv(diff_file, lib, 'urllib3', high_severity_diffs, low_severity_diffs)