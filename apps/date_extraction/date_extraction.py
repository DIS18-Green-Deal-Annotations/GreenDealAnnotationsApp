import os, sys
from bs4 import BeautifulSoup
import pandas as pd
from regex import P
import requests
import re
import spacy
import numpy as np
import datetime as dt
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import init_doc_obj

from models import DateExtraction


class bcolors:
    '''
    Class with custom colors to print text in colors.
    '''
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def check_url(url: str, docname: str):
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
    Removes spefific classes and all tables from the html text
    ARGS: str = full html source code
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
    """ 
    Extracts sentences with dates in it. 
    ARGS: str, nlp-module
    RETURN: list 
    """
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

def add_content_to_df(df, name, sentence):
    """ 
    Add the data from doc object to df.
    ARGS: df, str, str
    RETURN: df = name, sentence
    """
    data = pd.DataFrame({'name': name, 'sentence': sentence})
    df = df.append(data, ignore_index=True)
    print('-> add_content_to_df() ... done')
    return df

def extract_date(df, nlp): # vera
    '''
    Adds new column to df with raw Date label from sentence. 
    ARGS: df = name, sentence
    RETURN: df = name, sentence, datelabel
    '''
    vera_df = pd.DataFrame()
    list = [] # empty list to store date entitys to append to df
    
    for index, row in df.iterrows():
        sentence = row['sentence']
        entitys = nlp(sentence)
        
        for entity in entitys.ents:
            if entity.label_ == "DATE":
                vera_df = vera_df.append(row)
                list.append(entity.text)

    vera_df['datelabel'] = list
    print('-> extract_date() ... done')
    return vera_df

def normalize_date(df): # helga
    ''' 
    function first converts strings with relative temporal expressions in given column to timestamp strings
    writes output in new column 'Date'
    function then converts all date strings in column 'Date' to short ISO format YYYY-MM-DD
    writes output in new column 'Isodate'
    invalid data converted to 'NaT' (not a time)
    ARGS: df = name, sentence, datelabel
    RETURN: df = name, sentence, datelabel, isodate
    '''
    # create a dictionary of relative temporal expressions
    # for working purposes, we will use datetime.now() for the prototype; needs to be replaced with document date later
    # keys will be collected successively from extracted relative temporal expressions later on
    relTempExp = {
        'this year':[str(dt.datetime.now().year)],
        'next year':[str(dt.datetime.now().year+1)],
        'last year':[str(dt.datetime.now().year-1)],
        'today':[str(dt.datetime.now())]
        }
    
    # set all strings to lower case to match with relTempExp dictionary
    df['datelabel'] = df['datelabel'].str.lower()

    # replace relative temporal expressions with date string values based on dictionary
    df = df.replace({'datelabel': relTempExp})

    # transform datelabel into isodate
    df['isodate'] = pd.to_datetime(df['datelabel'], errors='coerce').dt.date
    
    print('-> normalize_date() ... done')
    return df 

def clean_df(df):
    '''
    Delets all NaT and sorts df
    ARGS: df 
    RETURN: df
    '''
    df = df[pd.notnull(df['isodate'])] # delete all NaT (not null)
    df = df.sort_values(by=['isodate'], ascending = False) # sort df
    print('-> clean_df() ... done')
    return df

def add_data_to_db(df):

    # schreibe die Daten aus dem df in die db
    data = DateExtraction.objects.all()
    print(f'{data}')
    print('-> add_data_to_db() ... done')
    return 

def process(doc, nlp, df):
    '''
    Takes document object, download, clean, extract content, extract single sentences, extract date and normalize date 
    ARGS:   doc = document object
            nlp = nlp package for spacy
            df = empty df to add the data
    RETURN: None
    '''

    if doc.type == "html":
        # check if url is online
        check_url(doc.url, doc.name)

        # extract html text
        html_text = import_url(doc.url)

        # clean html text and extract the clean text
        clean_text = clean_html(html_text)

        # clean and extract only sentences with date entitys from text and add to doc.sentences object
        doc.sentences = extract_sentence(clean_text, nlp)

        # add sentences to df -(oliver, janina)
        df = add_content_to_df(df, doc.name, doc.sentences)

        # extract date from sentence and create column
        df = extract_date(df,nlp)

        # add new colum with normalize date
        df = normalize_date(df)

        # 
        df = clean_df(df)

        add_data_to_db(df)

def main():

    # Load English tokenizer, tagger, parser and NER for spacys
    nlp = spacy.load("en_core_web_sm") 

    # empty df to load the data from every doc into it
    df = pd.DataFrame()

    # creates list of objects for every document entry in init_doc_obj.py
    list_of_doc = init_doc_obj.main() 

    for doc in list_of_doc:
        # fills df with all sentences from document
        # extract and normalize date from sentence
        # add data to django db
        process(doc, nlp, df)
    
if __name__=="__main__":
    main()