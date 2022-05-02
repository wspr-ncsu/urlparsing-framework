from requests import get
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=safari'

def get_row_data(tr):
	cve = []
	for td in tr.find_all('td'):
		cve.append(td.get_text(strip=True))
		link = td.find('a')
		if link:
			cve.append('https://cve.mitre.org' + link.get('href'))
	return cve

if __name__ == '__main__':
	response = get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	table = soup.find('div', {'id': 'TableWithRules'})
	
	url_cve = []
	for row in table.find_all('tr')[1:]:
		cve = get_row_data(row)
		
		if any(u in cve[2] for u in ['URL', 'url']):
			url_cve.append(cve)

	dataframe = pd.DataFrame(url_cve, columns=['CVE', 'Link', 'Description'])
	dataframe.to_excel('url-cve-safari.xlsx', index=False)
