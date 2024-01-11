from bs4 import BeautifulSoup as Soup
import requests

from typing import List
import time
import urllib
import json

headers = {
	"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "en-US;en;q=0.9",
	"Connection": "keep-alive"
}

class Userinfo:
	def __init__(self, username, url):
		self.username = username
		url = url.replace("https://steamcommunity.com/", "")
		url = url.replace("https://steamcommunity.com/", "")
		self.url = url
	def __str__(self):
		return f"{self.username},{self.url}"

	def __repr__(self):
		return f"{self.__str__()}"

class Crawler:
	def __init__(self):
		self.session = requests.Session()
		self.session.headers = headers

		#Visit the website once to get the `sessionid`
		self.session.get("https://steamcommunity.com")
		cookies = self.session.cookies.get_dict()
		self.sessionid = cookies["sessionid"]

	def crawl(self, username, write_html=False, validator=None) -> List[Userinfo]:
		"""
		Args:
			validator: func(username) -> bool
				Omits the userinfo when it returns false
		"""

		username_encoded = urllib.parse.quote(username, safe='')
		#baseurl = f"https://steamcommunity.com/search/users/#page={{}}&text={username_encoded}"
		baseurl = f"https://steamcommunity.com/search/SearchCommunityAjax?text={username}&filter=users&sessionid={self.sessionid}&steamid_user=false&page="
		userinfos = []

		if write_html:
			fout = open(f"output/{username_encoded}_{int(time.time())}.html", "w", encoding="utf-8")
			#Some text's color is `whitesmoke`...
			fout.write("""
				<!DOCTYPE html>
				<html>
					<head>
						<meta charset="utf-8">
						<style>
							body {
								background-color: black;
								color: green;
							}
						</style>
					</head>
					<body>
			""")
		else:
			fout = None

		i = 1
		while i < 501: #For some reason it can't go beyond the page 500
			url = baseurl + str(i)

			req = self.session.get(url)
			json_obj = json.loads(req.text)
			page_obj = Soup(json_obj["html"], "html.parser")

			if fout:
				fout.write(json_obj["html"])

			#"Showing ... of ..."
			paging = page_obj.find("span", class_="community_searchresults_paging")
			paging_text = ' '.join(paging.get_text().split())

			#Does it have the next page?
			has_next_page = '>' in paging_text

			for search_row in page_obj.find_all("div", class_="search_row"):
				name_obj = search_row.find("a", class_="searchPersonaName")
				name = name_obj.get_text()
				href = name_obj["href"]

				if not validator or validator(name):
					userinfos.append(Userinfo(name, href))

			if not has_next_page:
				break

			i += 1
			time.sleep(0.1)

		if fout:
			fout.write("""
					</body>
				</html>
			""")
			fout.close()
		return userinfos