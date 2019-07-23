import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.request
import os
import pickle
from pyfiglet import Figlet
import shutil
import video_downloader


dir_name = os.path.dirname(os.path.realpath(__file__))

# main function for downloading post image
def post_image_save(insta_page_name, dic):
    try:
        list_of_post_ids = dic[insta_page_name]

        r = requests.get('https://www.instagram.com/' + insta_page_name)
        soup = BeautifulSoup(r.content, "lxml")
        scripts = soup.find_all('script', type="text/javascript",
                                text=re.compile('window._sharedData'))
        stringified_json = scripts[0].get_text().replace(
            'window._sharedData = ', '')[:-1]

        dic_file = (json.loads(stringified_json)['entry_data']['ProfilePage'][0])

        list_of_posts = (dic_file["graphql"]["user"]
                         ["edge_owner_to_timeline_media"]["edges"])

        number_of_posts = len(list_of_posts)
        new_post_num = 0
        for index in range(number_of_posts):
            post1 = list_of_posts[index]
            id = post1["node"]["id"]
            if id not in list_of_post_ids:
                if(post1["node"]["is_video"] and Options.video_download):
                    shortcode = post1["node"]["shortcode"]
                    save_location = dir_name + "/archive/" + insta_page_name + "/"
                    video_downloader.video_downloader(
                        "https://www.instagram.com/p/" + shortcode, save_location)
                else:
                    link = post1["node"]["display_url"]
                    f = open("archive/" + insta_page_name +
                             '/' + str(id) + '.jpg', 'wb')
                    f.write(urllib.request.urlopen(link).read())
                    f.close()
                list_of_post_ids.append(id)
                new_post_num += 1

            else:
                break

        list_of_post_ids = list_of_post_ids[-12:]
        dic[insta_page_name] = list_of_post_ids
        pickle_file_dump("pages.pickle", dic)
        if new_post_num != 0:
            print("\n%d posts are added to %s page, go and check it out!!" %
                  (new_post_num, insta_page_name))
        else:
            print("\nsorry no new posts are added to %s page :(" % insta_page_name)

    except:
        print("This page is private")

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
    
    video_download = False

    

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
    while True:
        try:
            list_of_pages = list(dic.keys())
            num = 1
            for page_name in list_of_pages:
                print("%d.%s" % (num, page_name))
                num += 1
            page = input("please enter number that you want to check > ")
            insta_page_name = list_of_pages[int(page) - 1]
            return insta_page_name
        except IndexError:
            clearScreen()
            print("Please Enter a number that is in the range!")
        except:
            clearScreen()
            print("Please Enter a valid charachter!")


def delete_page():
    while True:
        try:
            print("choose page that you want to delete from list>>\n")
            dic = pickle_file_load("pages.pickle")
            page_name = listing_page_names(dic)
            del dic[page_name]
            pickle_file_dump("pages.pickle", dic)

            option = input(
                "Do you want to delete user images from archive too?? (Y/N) > ")
            if option.lower()=="y":
                shutil.rmtree("archive/" + page_name)
            else:
                pass
            if not continueFunction():
                break

        except IndexError:
            print("Not valid number!\nPlease enter valid number!!")

def continueFunction():
    while True:
        choice = input("Do you want to continue(y/n)")
        if choice.lower()=="y":
            return 1
        elif choice.lower()=="n":
            return 0
        else:
            print("Please enter valid input!")

def clearScreen():
    os.system("clear")


#---------------------------main options-----------------------------------------------------------------

# this option is for checking one particular page for new posts


def option_one():
    dic = pickle_file_load("pages.pickle")
    if dic == {}:
        print("Please first add a page!")
    else:
        page = listing_page_names(dic)
        post_image_save(page, dic)
    input("\nPress any keys to go back to main menu > ")


# to check all pages for new post and archive them
def option_two():
    dic = pickle_file_load("pages.pickle")
    if dic == {}:
        print("Please first add a page")
    else:
        for page in list(dic.keys()):
            post_image_save(page, dic)
            print(page)
    input("\nAll pages are checked,press any keys to go back to main menu")

# for adding a new page to the list of pages

# TODO:check if a page is private or not and then give permission to be added
def option_three():
    while True:
        try:
            dic = pickle_file_load("pages.pickle")
            list_of_pages = list(dic.keys())
            page_name = input("Please enter name of the page that you want to add> ")
            if page_name in list_of_pages:
                print("This page was entered before,plese add a new page name")
            else:
                dic[page_name] = []
                pickle_file_dump("pages.pickle", dic)
                os.mkdir("archive/" + page_name)
            if not continueFunction():
                break
        except:
            print("This page does not exist,please enter a valid page name!")



# for deleting particular page from list
def option_four():
    delete_page()

#for turning video download on
def option_five():
	Options.video_download = True

def option_six():
    dic = pickle_file_load("pages.pickle")
    page_name = listing_page_names(dic)
    os.system("feh -F archive/" + page_name)


if __name__ == "__main__":
    main()
