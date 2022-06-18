from bs4 import BeautifulSoup
import re

# TODO: Extract clean COM Numbers
# TODO: Implement logic (method) to get the search results for the COM Numbers
# TODO: Extract the right (most fitting) search result
# TODO: Extract link from the search result 

from extractor.extractor import COM_Extractor
from html_modifier.modifier import COM_Modifier

com = COM_Extractor("./data/COM(2021)552final.html")
com_list = com.extract_com()

print(com_list)

html = COM_Modifier("./data/COM(2021)552final.html", com_list, "./data_updated/")
html.modify()




  
#COM(2019)640 final
#COM(2020)562 final