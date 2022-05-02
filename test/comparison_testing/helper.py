import csv
import json
import difflib

ipv6_brackets = {']', '['}

def check_severity(difference):
	# discard ipv6 brackets cosmetic difference
	if 'host' in difference.keys():
		h1 = set(difference['host'][0])
		h2 = set(difference['host'][1])
		d = h1.symmetric_difference(h2)
		if d == ipv6_brackets:
			return 1
		return 10

	# parsing error
	if 'scheme' in difference.keys():
		if 'not parsed' in difference['scheme'][1]:
			return 10

	# port difference
	if 'port' in difference.keys():
		return 10

	# encoding difference
	if '%' in difference.values():
		print("Encoding issue.")
		return 10

	return 1

def compare_parser_outputs(url, urllib_output, lib_output):
	mismatch = 0
	difference = {}
	for key, value in urllib_output.items():
		if key == 'port' and value:
			value = int(value)
		if key not in lib_output:
			lib_output[key] = ''
		try:
			if type(value) != int:
				value = value.lower()
			if type(lib_output[key]) != int:
				lib_output[key] = lib_output[key].lower()
			if value != lib_output[key]:
				difference[key] = [value, lib_output[key]]
				mismatch = 1
		except AttributeError as e:
			print("error in comparison for key %s\nurllib = %s\nother = %s" % (key, value, lib_output[key]))
	if mismatch:
		diff = [json.dumps(url), json.dumps(lib_output, indent=1), json.dumps(urllib_output, indent=1)]
		return (check_severity(difference), diff)

	return (0, 0)

def write_to_csv(diff_file, lib, orig_lib, high_severity_diffs, low_severity_diffs):
	with open(diff_file, 'w+') as f:
		header = ['URL', lib, orig_lib]
		writer = csv.writer(f)
		writer.writerow(header)
	
		try:
			writer.writerow(['HIGH SEVERITY', len(high_severity_diffs)])
			for diff in high_severity_diffs:
				writer.writerows([diff])
			writer.writerow([])
			writer.writerow(['LOW SEVERITY', len(low_severity_diffs)])
			for diff in low_severity_diffs:
				writer.writerows([diff])
		except Exception as e:
			print("Exception: ", e)