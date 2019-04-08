import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.request
import os
import pickle
from pyfiglet import Figlet
# main function for downloading post image


def post_image_save(insta_page_name):

    r = requests.get('https://www.instagram.com/' + insta_page_name)
    soup = BeautifulSoup(r.content, "lxml")
    scripts = soup.find_all('script', type="text/javascript",
                            text=re.compile('window._sharedData'))
    stringified_json = scripts[0].get_text().replace(
        'window._sharedData = ', '')[:-1]

    dic_file = (json.loads(stringified_json)['entry_data']['ProfilePage'][0])

    list_of_posts = (dic_file["graphql"]["user"]
                     ["edge_owner_to_timeline_media"]["edges"])

    name = 1

    for index in range(12):
        post1 = list_of_posts[index]
        link = post1["node"]["display_url"]
        f = open("archive/" + insta_page_name + '/' + str(name) + '.jpg', 'wb')
        f.write(urllib.request.urlopen(link).read())
        f.close()
        name = name + 1

# this class is for checking necessary files and folders in current directory


class Options:
    def __init__(self):
        files = os.listdir()
        if "pages.pickle" not in files:
            dic = {}
            file = open("pages.pickle", "wb")
            pickle.dump(dic, file)
            file.close()
        if "archive" not in files:
            os.mkdir("archive")

# for loading a pickle file from current directory


def pickle_file_load(name):
    file = open(name, "rb")
    file1 = pickle.load(file)
    file.close()
    return file1

# for dumping changed dictionary


def pickle_file_dump(name, dic):
    file = open(name, "wb")
    pickle.dump(dic, file)
    file.close()


def listing_page_names(dic):
    list_of_pages = list(dic.keys())
    num = 1
    for page_name in list_of_pages:
        print("%d.%s" % (num, page_name))
        num += 1
    page = input("please enter number that you want to check > ")
    return list_of_pages[int(page) - 1]

# this option is for checking one particular page for new posts


def option_one():
    dic = pickle_file_load("pages.pickle")
    if dic == {}:
        print("Please first add a page!")
    else:
        page = listing_page_names(dic)
        post_image_save(page)


# for adding a new page to the list of pages
def option_two():
    dic = pickle_file_load("pages.pickle")
    list_of_pages = list(dic.keys())
    page_name = input("Please enter name of the page that you want to add> ")
    if page_name in list_of_pages:
        print("This page was entered before,plese add a new page name")
    else:
        dic[page_name] = []
        pickle_file_dump("pages.pickle", dic)
        os.mkdir("archive/" + page_name)


# option_one()

if __name__ == "__main__":
    main()
