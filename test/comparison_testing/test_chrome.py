import json
import argparse
from helper import *

lib_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/'
chrome_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/comparison_testing/chrome/'
diff_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/comparison_testing/diffs/diff_chrome_'

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Testing Urllib")
    parser.add_argument('--lib', action='store', dest='lib', type=str, required=True)
    lib = parser.parse_args().lib
    diff_file = diff_file + lib + '.csv'
    lib_file = lib_file + lib + '.json'
    chrome_file = chrome_file + lib + '.json'

    with open(lib_file, 'r+') as f:
        data = json.load(f)
    lib_urls = data['urls']

    with open(chrome_file, 'r+') as f:
        data = json.load(f)
    chrome_urls = data['urls']

    total_count = 0
    high_severity_diffs = []
    low_severity_diffs = []
    
    for index, url in enumerate(lib_urls):
        input_url = url['input']
        total_count += 1
        severity, diff = compare_parser_outputs(input_url, chrome_urls[index]["output"], url['expected_output'])
        
        if not diff:
            continue
        if severity == 10:
            high_severity_diffs.append(diff)
        else:
            low_severity_diffs.append(diff)

    diff_count = len(high_severity_diffs) + len(low_severity_diffs)
    print("Out of total %s found %s differences in parsing.\nHigh Severity = %s\nLow Severity = %s\nCheck file %s for details." % (total_count, diff_count, len(high_severity_diffs), len(low_severity_diffs), diff_file))
    write_to_csv(diff_file, lib, 'chrome', high_severity_diffs, low_severity_diffs)