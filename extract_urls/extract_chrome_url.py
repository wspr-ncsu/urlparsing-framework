import json, os

chrome_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/tmp_chrome.json'
json_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/chrome.json'

def write_to_file(new_data):
    if not os.path.isfile(json_file):
        with open(json_file, 'w+') as f:
            json.dump({"urls":[]}, f, indent=4)
        f.close()

    with open(json_file, 'r+') as f:
        file_data = json.load(f)
        if new_data not in file_data['urls']:
            file_data['urls'].append(new_data)
        f.seek(0)
        json.dump(file_data, f, indent=4)

if __name__ == '__main__':
    output = {"scheme": "", "user": "", "password": "", "host": "", "port": "", "path": "", "query": "", "fragment": ""}
    url = {"input": "", "expected_output": {}}
    
    if os.path.exists(json_file):
        os.remove(json_file)

    f = open(chrome_file)
    data = json.load(f)
    f.close()

    for d in data:
        url["input"] = d["input"]

        keys = list(d)
        for key in keys[1:]:
            if key == "port":
                if d[key].isdigit():
                    output[key] = int(d[key])
                elif d[key] == "-1":
                    output[key] = ""
                elif d[key] == "-2":
                    output[key] = -2
                else:
                    output[key] = d[key]
            else:
                output[key] = d[key]
            if output[key] == "(null)":
                output[key] = ""

        url["expected_output"] = output
        write_to_file(url)