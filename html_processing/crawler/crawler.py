from bs4 import BeautifulSoup
from .check_new import Check




def get_new():
    #initally download all html files or check if new ones are avaiable
    check = Check()
    check.check()


#check_new.check()