import os
from xxlimited import new

from com_linking.extractor.extractor import COM_Extractor
from com_linking.html_modifier.modifier import COM_Modifier
from crawler.crawler import get_new


#execute crawler
#Crawler.get_new()


def crawl_and_process_com():

    old_files = False

    print(old_files)

    if os.path.isdir('./html_processing/crawler/html/'):
        files = os.listdir("./html_processing/crawler/html/") # returns list
        old_files = files
        print(old_files)

    get_new()
    new_files = os.listdir("./html_processing/crawler/html/") #
    print(new_files)

    if old_files < new_files:
        for file in new_files:
            if file not in old_files:
                com = COM_Extractor(file, "./html_processing/crawler/html/")
                com_list =com.extract_com()
                html = COM_Modifier(file, com_list, "./html_processing/crawler/html/")
                html.modify()

# print(com_list)


if __name__ == '__main__':
    crawl_and_process_com()