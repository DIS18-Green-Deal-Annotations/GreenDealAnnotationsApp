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

# django imports
from django.core.management.base import BaseCommand, CommandError
from apps.date_extraction.models import DateExtraction

def init_doc_obj():
    """
    Creates an object for every document with sepcific attributs.
    ARGS: None
    RETURN: List = List of document objects
    """
    class doc:
        def __init__(self, name, typedudocument,titreobject, url, type, date):
            self.name = name
            self.typedudocument = typedudocument
            self.titreobject = titreobject
            self.url = url
            self.type = type
            self.sentences = []
            self.date = date

    doc_1 = doc("Communication: 'Fit for 55' - delivering the EU's 2030 climate target on the way to climate neutrality",
                "COMMUNICATION FROM THE COMMISSION TO THE EUROPEAN PARLIAMENT, THE COUNCIL, THE EUROPEAN ECONOMIC AND SOCIAL COMMITTEE AND THE COMMITTEE OF THE REGIONS EMPTY",
                "'Fit for 55': delivering the EU's 2030 Climate Target on the way to climate neutrality",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021DC0550&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
    )
    doc_2 = doc("Revision of the Regulation on the inclusion of greenhouse gas emissions and removals from land use, land use change and forestry",
                "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "amending Regulations (EU) 2018/841 as regards the scope, simplifying the compliance rules, setting out the targets of the Member States for 2030 and committing to the collective achievement of climate neutrality by 2035 in the land use, forestry and agriculture sector, and (EU) 2018/1999 as regards improvement in monitoring, reporting, tracking of progress and review",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0554&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
    )
    doc_3 = doc("Effort Sharing Regulation",
                "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "amending Regulation (EU) 2018/842 on binding annual greenhouse gas emission reductions by Member States from 2021 to 2030 contributing to climate action to meet commitments under the Paris Agreement",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0555&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
    )
    doc_4 = doc("Amendment to the Renewable Energy Directive to implement the ambition of the new 2030 climate target",
                "DIRECTIVE OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "amending Directive (EU) 2018/2001 of the European Parliament and of the Council,  Regulation (EU) 2018/1999 of the European Parliament and of the Council and Directive 98/70/EC of the European Parliament and of the Council  as regards the promotion of energy from renewable sources, and repealing Council Directive (EU) 2015/652",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0557&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
                
    )
    doc_5 = doc("Proposal for a Directive on energy efficiency (recast)",
                "DIRECTIVE OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "on energy efficiency (recast)",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0558&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
    )
    doc_6 = doc("Revision of the EU Emission Trading System for Aviation",
                "DIRECTIVE OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "amending Directive 2003/87/EC as regards aviation's contribution to the Union’s economy-wide emission reduction target and appropriately implementing a global market-based measure",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0552&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
    )
    doc_7 = doc("ReFuelEU Aviation – sustainable aviation fuels",
                "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "on ensuring a level playing field for sustainable air transport",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0561&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
    )
    doc_8 = doc("FuelEU Maritime – green European maritime space",
                "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "on the use of renewable and low-carbon fuels in maritime transport and amending Directive 2009/16/EC",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0562&from=EN",
                "html",
                "2021-07-14" #"14.7.2021"
)
    doc_9 = doc("Revision of the Directive on deployment of the alternative fuels infrastructure",
                "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                "on the deployment of alternative fuels infrastructure, and repealing Directive 2014/94/EU of the European Parliament and of the Council",
                "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0559&from=en",
                "html",
                "2021-07-14" #"14.7.2021"
    )
    doc_10 = doc("Strategic rollout plan to support rapid deployment of alternative fuels infrastructure",
                 "COMMUNICATION FROM THE COMMISSION TO THE EUROPEAN PARLIAMENT, THE COUNCIL, THE EUROPEAN ECONOMIC AND SOCIAL COMMITTEE AND THE COMMITTEE OF THE REGIONS EMPTY",
                 "A strategic rollout plan to outline a set of supplementary actions to support the rapid deployment of alternative fuels infrastructure",
                 "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021DC0560&from=nl",
                 "html",
                 "2021-07-14" #"14.7.2021"
    )
    doc_11 = doc("Carbon border adjustment mechanism",
                 "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                 "establishing a carbon border adjustment mechanism",
                 "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0564&from=en",
                 "html",
                 "2021-07-14" #"14.7.2021"
    )
    doc_12 = doc("Revision of the Energy Tax Directive",
                 "COUNCIL DIRECTIVE",
                 "restructuring the Union framework for the taxation of energy products and electricity (recast)",
                 "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0563&from=en",
                 "html",
                 "2021-07-14" #"14.7.2021"
    )
    doc_13 = doc("Notification on the Carbon Offsetting and Reduction Scheme for International Aviation (CORSIA)",
                 "DECISION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                 "amending Directive 2003/87/EC as regards the notification of offsetting in respect of a global market-based measure for aircraft operators based in the Union",
                 "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0567&from=en",
                 "html",
                 "2021-07-14" #"14.7.2021"
    )
    doc_14 = doc("Revision of the Market Stability Reserve",
                 "DECISION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                 "amending Decision (EU) 2015/1814 as regards the amount of allowances to be placed in the market stability reserve for the Union greenhouse gas emission trading scheme until 2030",
                 "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0571&from=en",
                 "html",
                 "2021-07-14" #"14.7.2021"
    )
    doc_15 = doc("Social Climate Fund",
                 "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                 "establishing a Social Climate Fund",
                 "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021PC0568&from=en",
                 "html",
                 "2021-07-14" #"14.7.2021"
    )
    doc_16 = doc("Communication: New EU Forest Strategy for 2030",
                 "COMMUNICATION FROM THE COMMISSION TO THE EUROPEAN PARLIAMENT, THE COUNCIL, THE EUROPEAN ECONOMIC AND SOCIAL COMMITTEE AND THE COMMITTEE OF THE REGIONS EMPTY",
                 "New EU Forest Strategy for 2030",
                 "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52021DC0572&from=EN",
                 "html",
                 "2021-07-16" #"16.7.2021"
    )
    doc_17 = doc("Amendment of the Regulation setting CO2 emission standards for cars and vans 1",
                 "REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                 "amending Regulation (EU) 2019/631 as regards strengthening the CO2 emission performance standards for new passenger cars and new light commercial vehicles in line with the Union’s increased climate ambition",
                 "https://eur-lex.europa.eu/resource.html?uri=cellar:870b365e-eecc-11eb-a71c-01aa75ed71a1.0001.01/DOC_1&format=PDF",
                 "pdf",
                 "2021-07-14" #"14.7.2021"
    )
    doc_18 = doc("Amendment of the Regulation setting CO2 emission standards for cars and vans 2",
                 "Proposal for a REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                 "amending Regulation (EU) 2019/631 as regards strengthening the CO2 emission performance standards for new passenger cars and new light commercial vehicles in line with the Union’s increased climate ambition",
                 "https://eur-lex.europa.eu/resource.html?uri=cellar:870b365e-eecc-11eb-a71c-01aa75ed71a1.0001.01/DOC_2&format=PDF",
                 "pdf",
                 "2021-07-14" #"14.7.2021"
    )
    doc_19 = doc("Revision of the EU Emission Trading System",
                 "DIRECTIVE OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL",
                 "amending Directive 2003/87/EC establishing a system for greenhouse gas emission allowance trading within the Union, Decision (EU) 2015/1814 concerning the establishment and operation of a market stability reserve for the Union greenhouse gas emission trading scheme and Regulation (EU) 2015/757",
                 "https://ec.europa.eu/info/sites/default/files/revision-eu-ets_with-annex_en_0.pdf",
                 "pdf",
                 "2021-07-14" #"14.7.2021"
    )
    
    list = [doc_1]

    return list

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

    model_instances = [DateExtraction(
    docname = record[0],
    docsentence = record[1],
    datelabel = record[2],
    isodate = record[3]
    ) for record in df]

    DateExtraction.objects.bulk_create(model_instances)

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

        # add sentences to df
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
    list_of_doc = init_doc_obj() 

    for doc in list_of_doc:
        # fills df with all sentences from document
        # extract and normalize date from sentence
        # add data to django db
        process(doc, nlp, df)
    
if __name__=="__main__":
    main()

class Command(BaseCommand):
    def handle(self, *args, **options):
        main()