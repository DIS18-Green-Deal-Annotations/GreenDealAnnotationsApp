from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
from pathlib import Path
import spacy
import datetime as dt
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

import django
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append('./')
settings.configure(
    DJANGO_SETTINGS_MODULE='GreenDealAnnotations.settings',
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'GreenDealAnnotations/db.sqlite3',
        }
    },
)
django.setup()

# django imports
from django.core.management.base import BaseCommand
from core.models import DateExtraction

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
    
    list = [doc_1, doc_2, doc_3]

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
    relTempExp = {'this year':['2021'],
        'next year':['2022'],
        'last year':['2020'],
        'today':['14-07-2021'],
        'the current day':[str(dt.datetime.now())],
        'the last two years':['14-07-2019'],
        'the past 10 years':['14-07-2011'],
        'the past years':['14-07-2016'],
        'the next years':['14-07-2026'],
        'this decade':['01-01-2020'],
        'the next decade':['01-01-2030'],
        'the coming decade':['01-01-2030'],
        'the next decades':['01-01-2030'],
        'the coming decades':['01-01-2030'],
        'the last decade':['01-01-2010'],
        'the past two decades':['01-01-2000'],
        'the last decades':['01-01-2000'],
        'the past decades':['01-01-2000'],
        '2021-2027':['01-01-2021'],
        'recent years':['14-07-2016'],
        '2025-2032':['01-01-2025'],
        'the last 16 years':['01-01-2005'],
        'the period 2023 to 2025':['01-01-2023'],
        'later in the year':['15-10-2021'],
        'later this year':['15-10-2021'],
        'the final quarter':['01-10-2021'],
        'later in the century':['01-01-2050'],
        'the coming years':['01-01-2022'],
        'the period 2021 to 2030':['01-01-2021'],
        'the beginning of 2021':['01-01-2021'],
        'end-2019':['31-12-2019'],
        '13 november 2020 to 5':['13-11-2020'],
        '2016-2018':['01-01-2016'],
        '2026-2030':['01-01-2026'],
        'the years 2021, 2022':['01-01-2021'],
        'the years 2026':['01-01-2026'],
        '2021-2025':['01-01-2021'],
        'the years 2016, 2017':['01-01-2016'],
        'years 2021, 2022':['01-01-2021'],
        '2026-2029':['01-01-2026'],
        'the end of 2025':['31-12-2025'],
        'post-2030':['01-01-2031'],
        'the end of 2017':['31-12-2017'],
        'the second period 2026-2030':['01-01-2026'],
        'the years 2026 to 2030':['01-01-2026'],
        'mid-2024':['01-07-2024'],
        '2030 38':['01-01-2030'],
        '2021 to 2025':['01-01-2025'],
        'no later than 2025':['31-12-2025'],
        'no later than 31 december 2017':['31-12-2017'],
        'post-2035':['01-01-2036'],
        '2030 47':['01-01-2030'],
        '2023 to 2024':['01-01-2023'],
        '2030 below 1990':['01-01-2030'],
        'the 2026 year':['01-01-2026'],
        '2030 65':['01-01-2030'],
        'the years 2021 to':['01-01-2021'],
        '29 october 2020 to 26 november 2020':['29-10-2020'],
        'the years 2023 to 2030':['01-01-2023'],
        'the years 2023, 2024':['01-01-2023'],
        'the years 2005':['01-01-2005'],
        '2016 to 2018':['01-01-2016'],
        'the years 2021, 2022 and':['01-01-2021'],
        '2023-2027':['01-01-2023'],
        '2021-2030':['01-01-2023'],
        'the years of 2026 to 2030':['01-01-2026'],
        'the years 2021':['01-01-2021'],
        '2019 to 2020':['01-01-2019'],
        'the years from 2021 to 2030':['01-01-2021'],
        'the years 2016, 2017 and 2018':['01-01-2016'],
        'the years 2025 to 2030':['01-01-2025'],
        'the years 2021 to 2025':['01-01-2021'],
        'the period 2026 to 2030':['01-01-2026'],
        'as of end of 2019':['31-12-2019'],
        '3 august to 21 september 2020':['03-08-2020'],
        'the 10 of march 2021':['10-03-2021'],
        'between 2014 and':['01-01-2014'],
        'the end of 2019':['3-12-2019'],
        'the periods 2021 to 2025 and 2026 to 2030':['01-01-2021'],
        'the period 2021 to 2025':['01-01-2021'],
        '2020-2030':['01-01-2020'],
        'the years 2021 to 2027':['01-01-2021'],
        'september to october 2020':['01-09-2020'],
        '2020 44':['01-01-2020'],
        '2050 ⇦':['01-01-2050'],
        'years 2017, 2018':['01-01-2017'],
        '2050 70':['01-01-2050'],
        'up to 31 december 2023':[],
        'the period 2021 to':['01-01-2021'],
        'december 2030 ⇨ ':['31-12-2030'],
        'the year 2019':['01-01-2019'],
        'the last three years':['01.01.2018'],
        '2018, 2019':['01-01-2018'],
        'the period 2015 to 2019':['01-01-2015'],
        '2017-2019':['01-01-2017'],
        'between 2013 and 2020':['01-01-2013'],
        'the year 2021':['01-01-2021'],
        '2017-23':['01-01-2017'],
        'between 3 july 2020 and 28':['03-07-2020'],
        'between 1 october 2020':['01-10-2020'],
        'year 2024':['01-01-2024'],
        '2021-2023':['01-01-2021'],
        'the year 2024':['01-01-2024'],
        'year 2023':['01-01-2023'],
        'the year 2023':['01-01-2023'],
        '2021-23':['01-01-2021'],
        '2019-20':['01-01-2019'],
        'the period 2021 to 2023':['01-01-2021'],
        'the period 2024 to 2026':['01-01-2024'],
        'the period 2027 to 2029':['01-01-2027'],
        'the period 2033 to 2035':['01-01-2033'],
        '2019-2020':['01-01-2019'],
        'august to october 2020':['01-08-2020'],
        'the period 2021':['01-01-2021'],
        '2 july 2020 to 10 september 2020':['02-07-2020'],
        '18 august 2020 to 18 september 2020':['18-08-2020'],
        'between 10 july 2020 and 1 december 2020':['10-07-2020'],
        'between 2023 and 2030':['01-01-2023'],
        'post-2020':['01-01-2021'],
        'the years before 2025':['31-12-2024'],
        'december 2020 to february 2021':['01-12-2020'],
        'october 2018 to november 2019':['01-10-2018'],
        'the end of 2026':['31-12-2026'],
        'a)1 january 2025':['01-01-2025'],
        '31 december of the years 2025, 2030 and':['31-12-2025'],
        'the end of 2020':['31-12-2020'],
        '2020 13':['01-01-2020'],
        '2030 14':['01-01-2030'],
        'the second half of this decade':['01-01-2026'],
        'between 2021 and 2030':['01-01-2021'],
        '2025-2050':['01-01-2025'],
        'early 2021':['01-03-2021'],
        'early 2020':['01-03-2020'],
        '2014-2020':['01-01-2014'],
        'the end of 2021 and':['31-12-2021'],
        '2023 and 2025':['01-01-2023'],
        '1 january 2023 to 31 december 2025':['01-01-2023'],
        'the period 2023':['01-01-2023'],
        '2023 to 2025':['01-01-2023'],
        'the past 15 years':['01-01-2006'],
        '22 july 2020 to 14 october 2020':['22-07-2020'],
        'between 2020 and 2035':['01-01-2020'],
        '2023 ⇦':['01-01-2023'],
        'no later than 31 december 2009':['31-12-2009'],
        'no later than 1 january 2007':['01-01-2007'],
        'years 2020-2024':['01-01-2020'],
        'the first half of 2021':['30-06-2021'],
        'years 2021-23':['01-01-2021'],
        'year 2021':['01-01-2021'],
        'five-year-forecast-2020-2024':['01-01-2020'],
        '13 november 2020 to 5 february 2021':['13-11-2020'],
        '2025-32':['01-01-2025'],
        '2025-2027':['01-01-2025'],
        'the period 2025 to 2032':['01-01-2025'],
        'end-june 2024':['30-06-2024'],
        'the years 2025-2027':['01-01-2025'],
        'the years 2028-2032':['01-01-2028'],
        'the years 2025, 2026':['01-01-2025'],
        '2025 to 2032':['01-01-2025'],
        'mid-2023':['01-07-2023'],
        'late 2023':['01-10-2023'],
        'early 2025':['01-03-2025'],
        'mid-2025':['01-07-2025'],
        '2030 39':['01-01-2030'],
        'the end of 2021':['31-12-2021'],
        '2013-2018':['01-01-2013'],
        '2003-2007':['01-01-2003']
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
    # save data
    for index, row in df.iterrows():
        model = DateExtraction()
        model.docname = row['name']
        model.docsentence = row['sentence']
        model.datelabel = row['datelabel']
        model.isodate = row['isodate']
        model.save()
    return print('-> add_data_to_db() ... done')

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

    # first delet all data in dateextraction table
    model = DateExtraction.objects.all()
    model.delete()

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