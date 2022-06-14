from cmath import nan
import pandas as pd
from bs4 import BeautifulSoup
import requests


class fromURL:
    def __init__(self, url):
        self.url = url

    def get(self):
        try:
            pd.read_html(self.url)
            tables = pd.read_html(self.url, header=0)
            doc_name = self.get_doc_name()
            tables_dict = {doc_name: tables}
            return tables_dict
        except ValueError:
            return pd.NA

    def get_doc_name(self):
        r  = requests.get(self.url)
        data = r.text
        soup = BeautifulSoup(data)
        name = soup.find("p", {"class": "Rfrenceinstitutionnelle"}).text
        print(name)

        return name

