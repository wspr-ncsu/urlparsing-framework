from urllib.parse import urlparse
import json
import argparse
from helper import *

lib_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/'
diff_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/comparison_testing/diffs/diff_urllib_'

def break_into_key_value_pairs(parsed_url):
    keys = ['scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment']
    values = [val if val != None else '' for val in parsed_url]
    return dict(zip(keys, values))

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Testing Urllib")
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
        input_url = url['input']
        try:
            total_count += 1
            parsed_url = urlparse(input_url)
            
            try:
                parsed = [parsed_url.scheme, parsed_url.username, parsed_url.password, parsed_url.hostname, parsed_url.port, parsed_url.path,parsed_url.query, parsed_url.fragment]
            except ValueError as e:
                parsed = [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.query, parsed_url.fragment]

            parsed = break_into_key_value_pairs(parsed)
        except Exception:
            url['expected_output'] = ''
        
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
    write_to_csv(diff_file, lib, 'urllib', high_severity_diffs, low_severity_diffs)