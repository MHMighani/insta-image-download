import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.request
import os

insta_page_name = input("enter public insta page >> ")

if insta_page_name not in os.listdir():
	os.mkdir(insta_page_name)

r = requests.get('https://www.instagram.com/' + insta_page_name)
soup = BeautifulSoup(r.content,"lxml")
scripts = soup.find_all('script', type="text/javascript", text=re.compile('window._sharedData'))
stringified_json = scripts[0].get_text().replace('window._sharedData = ', '')[:-1]

dic_file = (json.loads(stringified_json)['entry_data']['ProfilePage'][0])

list_of_posts = (dic_file["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"])

name = 1

for index in range(12):
    post1 = list_of_posts[index]
    link = post1["node"]["display_url"]
    f = open(insta_page_name + '/' + str(name) + '.jpg','wb')
    f.write(urllib.request.urlopen(link).read())
    f.close()
    name = name + 1