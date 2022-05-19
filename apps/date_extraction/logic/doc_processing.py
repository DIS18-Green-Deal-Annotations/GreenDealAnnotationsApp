from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import spacy
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class bcolors:
    '''
    Class with custom colors to print text in colors.
    '''
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def check_url(url: str, docname):
    '''
    Check if url is online or not. Prints status of url to the console.
    ARGS: str = url string
    RETURN: None
    '''
    try:
        response = requests.head(url)
    except Exception as e:
        print(f'\n{docname} - {bcolors.FAIL}Error{bcolors.RESET}\n'
              f'Error Code: {bcolors.WARNING}{str(e)}{bcolors.RESET}')
    else:
        if response.status_code == 200:
            print(f'\n{docname} - {bcolors.OK}Online{bcolors.RESET}')
        else:
            print(f'\n{docname} - {bcolors.FAIL}Offline{bcolors.RESET}\n'
            'HTTP response code: {response.status_code}')

def import_url(url: str):
    '''
    Imports all content from url. If URL is not online the string will be empty.
    ARGS: str = url string
    RETURN: str = complete content from the html page (source code)
    '''
    try:
        response = requests.get(url) # Getting the webpage, creating a Response object. 
    except Exception as e:
        print(f'{str(e)}')
        url_source_code = ''
    else:
        url_source_code = response.text # Extracting the source code of the page.
        print(f'-> import_url() ... done')
    return url_source_code

def clean_html(full_html:str):
    """ 
    removes spefific classes and all tables from the html source code
    ARGS: full_html - full source code
    RETURN: str = extracted raw and cleaned text
    """
    delete_classes = [
        "CRRefonteDeleted",
        "CRMarker",
        "CRDeleted",
        "CRRefonteDeleted"
    ]
    soup = BeautifulSoup(full_html, 'html.parser')
    for class_name in delete_classes:
        for div in soup.find_all("div", {'class': class_name}): 
            div.decompose()

    for table in soup.find_all("table"):
        table.decompose()
    text = soup.text
    print('-> clean__html() ... done')
    return text

def extract_sentence(text, nlp):
    lr_newline = []
    no_newline = []

    sent_tokens = sent_tokenize(text)

    for sentence in sent_tokens:
        date_in_sentence = False
        entitys = nlp(sentence)
        for entity in entitys.ents:
            if entity.label_ == "DATE": # only append sentences with date entity in it
                date_in_sentence = True
        if date_in_sentence == True:
            lr_newline.append(sentence)
    '''
    for cleaner_sentence in lr_newline:
        no_newline.append(cleaner_sentence.replace("\n\n\n\n\n\n\n"," ")
                                            .replace("\n\n\n\n\n\n"," ")
                                            .replace("\n\n\n\n\n"," ")
                                            .replace("\n\n\n\n"," ")
                                            .replace("\n\n\n"," ")
                                            .replace("\n\n"," ")
                                            .replace("\n"," "))
    '''
    print('-> extract_sentence() ... done')
    
    return lr_newline

def add_content_to_df(df, docname, docsentences):
    data = pd.DataFrame({'docname': docname, 'sentence': docsentences})
    df = df.append(data, ignore_index=True)
    print('-> add_content_to_df() ... done')
    return df

def main(list, nlp):
    '''
    Step through all the documents one at a time, download, clean, extract content and add single sentences from document to df
    ARGS: list = list of document objects
           nlp = nlp package for spacy
    RETURN: df = [docname, sentence]
    '''
    df = pd.DataFrame()
    for doc in list:
        if doc.type == "html":
            # check url from document.url -(oliver)
            check_url(doc.url, doc.name)

            # import url from document.obj -(oliver)
            full_html = import_url(doc.url)

            # clean html source code and extract text -(oliver, janina)
            clean_text = clean_html(full_html)

            # clean and extract only sentences with date entitys from text and add to doc.sentences -(oliver, janina)
            doc.sentences = extract_sentence(clean_text, nlp)

            # add content to df -(oliver, janina)
            df = add_content_to_df(df, doc.name, doc.sentences)
    return df
