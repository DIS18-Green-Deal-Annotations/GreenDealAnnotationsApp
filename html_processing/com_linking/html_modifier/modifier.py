from bs4 import BeautifulSoup as bs
import re
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import requests
import os


# Extract clean COM Numbers  
# Implement logic (method) to get the search results for the COM Numbers
# Extract the right (most fitting) search result
# TODO: Solve problem when two COM Numbers are in one footnote



class COM_Modifier:

    def __init__(self, file, com_list, path):
        self.file = file
        self.com_list = com_list
        self.path = path

    def modify(self):
        print(self.file)
        print(self.com_list)

        html=open(os.path.join(self.path, self.file))

        # Parse HTML file in Beautiful Soup
        soup = bs(html, 'html.parser')
        
        # Give location where text is 
        # stored which you wish to alter
        for obj in self.com_list:
            footnote = obj["footnote"]
            old_text = soup.find("dd", {"id": footnote})
            children = old_text.findChildren("span" , recursive=True)
            print("-------------------------------------------------")
            for x in children:
                regexp = re.compile(r"(COM\s?\([0-9][0-9][0-9][0-9]\)\s?\s?\[?[0-9]*\]?\s?(?:final)?)|(COM\s?/[0-9][0-9][0-9][0-9]/\[?[0-9]*\]?\s(?:final)?)")
                if regexp.search(x.text):
                    a_tag = soup.new_tag('a')
                    a_tag.attrs["href"] = obj["link"]
                    wrapped = x.wrap(a_tag)
                    print(" ## ## ## ## ## ## ")
                    print(x, " ## ## ")
                    print(wrapped, " ## ## ")
                    print(" ## ## ## ## ## ## ")

        with open(os.path.join(self.path, self.file), "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))

            # new_tag = soup.new_tag('div')
            # wrapped = old_text.wrap(new_tag)

            #print(wrapped)

        
        # Replace the already stored text with 
        # the new text which you wish to assign
        # new_text = old_text.find(text=re.compile(
        #     'Geeks For Geeks')).replace_with('Vinayak Rai')
        
        # # Alter HTML file to see the changes done
        # with open("gfg.html", "wb") as f_output:
        #     f_output.write(soup.prettify("utf-8"))