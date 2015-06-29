import requests
import json
import re

def search(keyword):
	res = requests.get("https://www.google.com.tw/search?q=site:en.wikipedia.org+" + keyword + "&bav=on.2,or.&cad=b&fp=8d02688dbcaec00c&biw=808&bih=667&dpr=1&tch=1&ech=1&psi=1d6QVe-XHs798AW5kqnABg.1435557589508.3")
	content = res.text.split('/*""*/')[1]
	dic = json.loads(content)
	links = re.findall('/url\?q=https://en.wikipedia.org/wiki/(.+?)"', dic['d'])
	results = []
	for link in links:
		if link.find("%23") == -1:
			keyword = link.split("&amp;")[0]
			results.append('https://en.wikipedia.org/wiki/' + keyword)
	return results

if __name__ == '__main__':
	print search('test')