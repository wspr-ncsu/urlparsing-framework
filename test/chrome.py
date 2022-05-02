import sys
import json

file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/browsers/chromium/src/url/test_chrome.txt'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: python chrome.py <parser-name>")
		exit(1)

	with open('/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/' + sys.argv[1] + '.json', 'r+') as f:
		data = json.load(f)
		urls = data['urls']
	
	with open(file, 'a') as f:
		f.write("\n\n")
		f.write(sys.argv[1])
		f.write("----------------\n")
		for url in urls:
			line = '{"' + url["input"].replace('"', r'\"') + '"},\n'
			f.write(line)

	print("Done!\nCheck file %s for details." % file)