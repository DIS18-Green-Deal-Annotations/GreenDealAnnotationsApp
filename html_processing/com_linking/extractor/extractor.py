from bs4 import BeautifulSoup
import re
import os
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import requests


# Extract clean COM Numbers  
# Implement logic (method) to get the search results for the COM Numbers
# Extract the right (most fitting) search result
# TODO: Test if all com numbers getting the right link
# TODO: Add method to manipulate html


class COM_Extractor:

    def __init__(self, file, path):
        self.file = file
        self.path = path

    def extract_com(self):

        """
            This method aims to extract all com numbers with the corresponding footnote,
            wich are not already implemented as a hyperlink
        """
        # Filter out COM numbers wich are already displayed as hyperlink

        html= open(os.path.join(self.path, self.file), "r")
        content = html.read()

        soup = BeautifulSoup(content, 'html.parser')
        footer = soup.find_all("dd")# extract the footer

        extracted_com= []
        for f in footer:

            #print(f)

            if f.find_all("a", {"class": "externalRef"}):  # if a tag with class="externalRef" is already present, ignore it
                continue

            inner_text = f.getText() # get the content (text) from the footer
            com_findings = re.findall(
                "(COM\s?\([0-9][0-9][0-9][0-9]\)\s?\s?\[?[0-9]*\]?\s?(?:final)?)|(COM\s?/[0-9][0-9][0-9][0-9]/\[?[0-9]*\]?\s(?:final)?)",
                 inner_text) #regex for extracting com numbers 

            #print(com_findings)

            for results in com_findings:
                for com in results:
                    if com != '':
                        if com in inner_text:   # check if com number is in the current innertext to extract the corresponding com number
                            footnote_att = f.attrs
                            com_dict = {"footnote": footnote_att["id"], "com_number": com}
                            extracted_com.append(com_dict)

        print(extracted_com)
        print(len(extracted_com))

        com_list = self.add_link(extracted_com)

        return com_list

    def add_link(self, com_list: list):

        updated_list = []
        for com_obj in com_list:
            for key, value in com_obj.items():
                if key == "com_number":
                    link = self.scrape_google(value)
            update_obj = {"link": link}
            com_obj.update(update_obj)
            updated_list.append(com_obj)
            
        return updated_list
            

    def get_source(self, url):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """

        try:
            session = HTMLSession()
            response = session.get(url)
            return response

        except requests.exceptions.RequestException as e:
            print(e)

    def scrape_google(self, com_num: str):

        """Return the found link from the googled com number. 

        Args: 
            com_num (string): com number to search for.

        Returns:
            response (string): the found link. 
        """

        query = urllib.parse.quote_plus(com_num) # pass com number
        response = self.get_source("https://www.google.co.uk/search?q=" + query)

        links = list(response.html.absolute_links)

        # domians to exclude fron the search
        google_domains = ('https://www.google.', 
                        'https://google.', 
                        'https://webcache.googleusercontent.', 
                        'http://webcache.googleusercontent.', 
                        'https://policies.google.',
                        'https://support.google.',
                        'https://maps.google.',
                        'https://translate.google.co',)

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        eur_lex_url = "https://eur-lex.europa.eu/legal-content/"

        extracted_link = ""
        for url in links:
            if eur_lex_url in url:
                #print(url)
                extracted_link = url

        print(extracted_link)
        return extracted_link