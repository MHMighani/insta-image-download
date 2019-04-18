# main
from insta_image_download import *


menuItems = [
    {"Check one page for new post": option_one},
    {"Check all pages":option_two},
    {"Add a new page ": option_three},
    {"Delete a page":option_four},
    {"turn video download off":option_five},
    {"Exit": exit}
]

def main():
    while(True):
        option = Options()
        os.system("clear")
        fig = Figlet(font='doom')
        print(fig.renderText("post download"))
        print("ATTENTION: video download option is true as default!\n if you want to turn it off please choose option four :)")
        for item in menuItems:
            print("[" + str(menuItems.index(item)) + "]" + list(item.keys())[0])

        choice = int(input(">> "))
        list(menuItems[choice].values())[0]()

main()	