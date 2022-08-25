# -*- coding: utf-8 -*-
import os
import csv
import pandas as pd
import spacy
import re

import sys
from pathlib import Path

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

from pandarallel import pandarallel
from django.core.management.base import BaseCommand, CommandError
from core.models import Paragraphs, Document

pandarallel.initialize()

def persist_to_db(df):
    for index, row in df.iterrows():
        model = Paragraphs()
        model.header = row['header']
        model.header2 = row['header2']
        model.body = row['body']
        model.doctype = row['doctype']
        model.titreobjet = row['titreobjet']
        model.comnumber = Document.objects.get(com_id__exact=row['comnumber'])
        model.structure = row['structure']
        model.cleanbody = row['clean_body']
        model.weightedsimilarities = row['weighted_similarities']
        model.deskriptor = row['deskriptor']
        model.save()


def check_string_contains_token(search_string):
    tokens = []
    searchWords = ['legal', 'basis', 'proposal', 'annex', 'annexes', 'resolution', 'law', 'general', 'guidline]][|s',
                   'policy', 'treaty', 'implementing', 'decision', 'conclusion', 'principles', 'report', 'conditions',
                   'contributions', 'communication', 'regulation', 'Regulations', 'directive', 'council', 'decision',
                   'COMMUNICATION', 'REGULATION', 'DIRECTIVE', 'COUNCIL', 'DIRECTIVE', 'DECISION']
    for word in searchWords:
        if search_string.find(word) != -1:
            if word in ['legal'] and ['basis'] and 'Legal Basis' not in tokens:
                tokens.append('Legal Basis (legally binding)')
            if word in ['proposal'] not in tokens:
                tokens.append('Proposal')
            if word in ['annex'] not in tokens:
                tokens.append('Annex')
            if word in ['conclusion'] not in tokens:
                tokens.append('Conclusion')
            if word in ['principles'] not in tokens:
                tokens.append('Principles')
            if word in ['report'] not in tokens:
                tokens.append('Report')
            if word in ['conditions'] not in tokens:
                tokens.append('Conditions')
            if word in ['regulation'] not in tokens:
                tokens.append('Regulation (legally binding)')
            if word in ['Regulations'] not in tokens:
                tokens.append('Regulation')
            if word in ['contributions'] not in tokens:
                tokens.append('Contributions')
            if word in ['annexes'] not in tokens:
                tokens.append('Annexes')
            if word in ['COMMUNICATION'] and 'Communication' not in tokens:
                tokens.append('Communication')
            if word in ['REGULATION'] and 'Regulation' not in tokens:
                tokens.append('Regulation (legally binding)')
            if word in ['Regulations'] and 'Regulation (legally binding)' not in tokens:
                tokens.append('Regulation (legally binding)')
            if word in ['DECISION'] and 'Decision' not in tokens:
                tokens.append('Decision')
            if word in ['DIRECTIVE'] and ['COUNCIL'] and 'Council directive' not in tokens:
                tokens.append('Council directive')
            if word in ['DIRECTIVE'] and 'Directive' not in tokens:
                tokens.append('Directive')
            if word in ['evaluation'] and 'evaluation' not in tokens:
                tokens.append('evaluation')
            if word in ['report'] and 'report' not in tokens:
                tokens.append('report')
            if word in ['correction'] and 'correction' not in tokens:
                tokens.append('correction')
            if word in ['summary'] and 'summary' not in tokens:
                tokens.append('summary')
            if word in ['announcement'] and 'announcement' not in tokens:
                tokens.append('announcement')
            if word in ['impact assessment'] and 'impact assessment' not in tokens:
                tokens.append('impact assessment')
            if word in ['draft decision'] and 'draft decision' not in tokens:
                tokens.append('draft decision')
            if word in ['assasement'] and 'assasement' not in tokens:
                tokens.append('assasement')
            if word in ['reference'] and 'reference' not in tokens:
                tokens.append('reference')
            if word in ['provision'] and 'provision' not in tokens:
                tokens.append('provision')
            if word in ['proportionality'] and 'proportionality' not in tokens:
                tokens.append('proportionality')
            if word in ['subsidiarity'] and 'subsidiarity' not in tokens:
                tokens.append('subsidiarity')
            if word in ['corrigendum'] and 'corrigendum' not in tokens:
                tokens.append('corrigendum')
            if word in ['protocol'] and 'protocol' not in tokens:
                tokens.append('protocol')
            if word in ['opinion'] and 'opinion' not in tokens:
                tokens.append('opinion')
            if word in ['budget'] and 'budget' not in tokens:
                tokens.append('budget')
            if word in ['announcements'] and 'announcements' not in tokens:
                tokens.append('announcements')
            if word in ['information'] and 'information' not in tokens:
                tokens.append('information')
            if word in ['note'] and 'note' not in tokens:
                tokens.append('note')
            if word in ['judgment'] and 'judgment' not in tokens:
                tokens.append('judgment')
            if word in ['guideline'] and 'guideline' not in tokens:
                tokens.append('guideline')
            if word in ['recommendation'] and 'recommendation' not in tokens:
                tokens.append('recommendation')
            if word in ['ex-post-evaluation'] and 'ex-post-evaluation' not in tokens:
                tokens.append('ex-post-evaluation')
    return tokens

def remove_tags(tuples):
    for item in tuples:
        cleaned_string = ''
        for entry in item:
            cleaned_string = cleaned_string + entry
        item = cleaned_string
        item = item.strip()
        item = re.sub('(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\xa2)|\\n|<\/p|\'\',|\'\'|(<.*?>)', '',
                              item)
        return item

def analyse_documents():
    f = open('classificationresults.csv', 'w')
    writer = csv.writer(f, delimiter=";")
    # names of rows
    writer.writerow(['header', 'header2', 'body', 'doctype', 'titreobjet', 'comnumber', 'structure'])

    # dokument count/ necessity to name it like dokument1, dokument2, document3 etc. when crawling
    dir_path = r'./crawler/html'
    for filename in os.listdir(dir_path):
        dok = open(os.path.join(dir_path, filename))
        dokstring = str(dok.read())
        # because the hmtl headings are unstructured, there are different Versions:
        # for Dok1 applies: <p class="li Heading1" id="_GoBack"> and <p class="li Heading1">
        # for (Dok2, Dok3, Dok6, Dok7, Dok8, Dok9, Dok12, Dok13, Dok15, Dok16, Dok17) applies: <p class="li ManualHeading1"> <p class="li ManualHeading2"> <p class="li ManualHeading3"> (Dok3 has not: <p class="li ManualHeading2"> but: <span>• </span>) (mix from: <p class="li ManualHeading2"> and <span>• </span> also by Dok4)
        # for Dok5 applies: <p id="_GoBack" class="Exposdesmotifstitre"> and next it goes on with: <span>1.</span> <span>2.</span> and insite it can have: <span>•</span>

        # regex will find all of these different headings

        matches1 = re.findall(
            '(<p.*?ManualHeading1[^°]+?.??<.*?ManualHeading1)|(<p.*?Heading1[^°]+?.??</p.*?)|'
            '(<p\sid="_GoBack"\sclass="li\sHeading1">)([^°]+?.??<p\sclass="li\sHeading1">)|'
            '(<p\sid="_GoBack"\sclass="Exposdesmotifstitre>)([^°]+?.??<p\sclass="li\sHeading1">)|'
            # '(<p\sclass="li\sHeading1">)([^°]+?.??<p\sclass="li\sHeading1">)|'
            # '(<p\sclass="li\sManualHeading1">[^°]+?.??)<p\sclass="li\sManualHeading1">|'
            '(<p\sclass="li\sManualHeading1">)([^°]+?.??<dl\sid="footnotes">)|'
            '(<p\sclass="li\sHeading1">)([^°]+?.??<dl\sid="footnotes">)',
            dokstring)
        fullMatches1 = []
        if matches1:
            for submatches in matches1:
                for submatch in submatches:
                    if submatch != '':
                        fullMatches1.append(str(submatch))
            # there is also information on structure in the tag typedudocument
            typedudocument = re.findall('<p\sclass="Typedudocument_cp">.*?([^°]+?.??)</p>', dokstring)
            # also information in the titreobjet-tag
            titreobjet = re.findall('<p\sclass="Titreobjet_cp">.*?([^°]+?.??)</p>', dokstring)
            # also information in the rfrenceinstitutionelle-tag
            rfrenceinstitutionelle = re.findall('<p\sclass="Rfrenceinstitutionnelle">.*?([^°]+?.??)</p>', dokstring)
            cleaned_comnumbers = []
            for comnumber in rfrenceinstitutionelle:
                cleaned_comnumbers.append(comnumber.strip())
            rfrenceinstitutionelle = cleaned_comnumbers
            # there are not only heading1 but heading2 in the dokument, so we need to find these headings2 and exclude non-essential characters
            for match in fullMatches1:
                liHeaders2 = []
                # h1 = re.findall('(<p\sid="_GoBack"\sclass="li\sHeading1">\\\\n.*?\\\\n)|'
                # ('(ManualHeading1[^°]+?.??</p>)|(Heading1[^°]+?.??</p>)', match))

                h1 = str(re.findall('(<p.*?ManualHeading1[^°]+?.??</p>)|(<p.*?Heading1[^°]+?.??</p>)', match))
                headers2 = re.findall('(<p.*?ManualHeading2[^°]+?.??</p)|(<p.*?Heading2[^°]+?.??<.*?Heading2)|'
                                      '(<p\sid="_GoBack"\sclass="li\sHeading2">[^°]+?.??)<p\sclass="li\sHeading2">|'
                                      '(<p\sid="_GoBack"\sclass="Exposdesmotifstitre>[^°]+?.??)<p\sclass="li\sHeading2">|'
                                      '(?<=<p\sclass="li\sHeading2">)([^°]+?.??)(?<=<p\sclass="li\sHeading2">)|'
                                      '<p\sclass="li\sManualHeading2">([^°]+?.??)<p\sclass="li\sManualHeading2">|'
                                      '(<p\sclass="li\sManualHeading2">)([^°]+?.??<dl\sid="footnotes">)|'
                                      '(<p\sclass="li\sHeading2">)([^°]+?.??<dl\sid="footnotes">)', match)

                tokens = check_string_contains_token(str(typedudocument))
                tokens += check_string_contains_token(str(titreobjet))
                tokens += check_string_contains_token(str(rfrenceinstitutionelle).strip())
                if not headers2:
                    headers2 = re.findall(
                        '<span>(\s•\d\.[^°]+?.??)(?<=<span>\d\.)|'
                        '<span>(\s•\d\.[^°]+?.??)[^°](?=<p\sclass="li\sManualHeading1">)|'
                        '<span>(\s•\s[^°]+?.??)</span>', match)
                    for header2 in headers2:
                        for subheader2 in headers2:
                            if subheader2 != '':
                                liHeaders2.append(str(subheader2))
                else:
                    liHeaders2 = headers2[0]

                if liHeaders2:
                    liHeaders2 = list(set(liHeaders2))
                    for header2 in liHeaders2:
                        if header2 == '':
                            header2 = re.findall(
                                '(<p.*?ManualHeading3[^°]+?.??</p)|(<p.*?Heading3[^°]+?.??<.*?Heading3)|'
                                '(<p\sid="_GoBack"\sclass="li\sHeading3">[^°]+?.??)<p\sclass="li\sHeading3">|'
                                '(<p\sid="_GoBack"\sclass="Exposdesmotifstitre>[^°]+?.??)<p\sclass="li\sHeading3">|'
                                '(?<=<p\sclass="li\sHeading3">)([^°]+?.??)(?<=<p\sclass="li\sHeading3">)|'
                                '<p\sclass="li\sManualHeading3">([^°]+?.??)<p\sclass="li\sManualHeading3">|'
                                '(<p\sclass="li\sManualHeading3">)([^°]+?.??<dl\sid="footnotes">)|'
                                '(<p\sclass="li\sHeading3">)([^°]+?.??<dl\sid="footnotes">)|'
                                '(<span\sclass="num">[^°]+?.??</p)', match)
                        cleaned_header2 = []
                        if type(header2) is list:
                            cleaned_header2 = remove_tags(header2)
                        else:
                            header2 = header2.strip()
                            header2 = re.sub('(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\xa2)|\\n|\n|(</p\')|('',)|(<.*?>)|([\[\]])', '',
                                                      header2)
                            cleaned_header2.append(header2)
                        header2 = re.sub('(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\xa2)', '', str(header2))
                        tokens += check_string_contains_token(h1)
                        tokens += check_string_contains_token(header2)
                        # tokens = filter(None, tokens)
                        h1 = h1.strip()
                        h1 = re.sub(
                            '(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\xa2)|\\n|\n|(</p\')|('',)|(<.*?>)|([\[\]])', '',
                            h1)
                        cleaned_headers2 = remove_tags(headers2)
                        writer.writerow(
                            [h1, cleaned_header2, cleaned_headers2, typedudocument, titreobjet, rfrenceinstitutionelle, tokens])
                else:
                    cleaned_matches = remove_tags(matches1)
                    match = match.strip()
                    match = re.sub('(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\xa2)|\\n|\n|(</p\')|('',)|(<.*?>)|([\[\]])',
                                     '',
                                     match)
                    tokens += check_string_contains_token(str(matches1))
                    filter(None, tokens)
                    writer.writerow(
                        [cleaned_matches, [], match, typedudocument, titreobjet, rfrenceinstitutionelle, tokens])

        # if html-tags wanted to be delated in header, header2 and in body:
        heading1 = []
        for header in heading1:
            heading1.append(re.sub('(<.*?>)|(\\\\n)|(\\\\r)|(\\n)|(\\\\xe2\\\\x80\\\\x99S)', '', str(header)))

        heading2 = []
        for header in heading2:
            heading2.append(re.sub('(<.*?>)|(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\x..)', '', str(header2)))
            match = re.sub('(<.*?>)|(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\x..)', '', str(match))
    f.close()


def get_context_labels():
    ## Final Code ##

    # !pip install spacy
    # !python -m spacy download en_core_web_lg

    nlp = spacy.load("en_core_web_sm")

    df = pd.read_csv("classificationresults.csv", sep=";", encoding="utf-8")
    df = df.replace({"comnumber": ["\[", "\]", "'", ",.*"]}, {"comnumber": ""}, regex=True)
    df = df.replace({"body": ["\\\\\\\\*\w{3}", "\\\\"]}, {"body": " "}, regex=True)

    EUDESK = {
        "COM(2021) 550 final": ["innovation", "clean technology", "adaption to climate change", "emission trading",
                                "carbon", "climate change", "greenhouse gas", "green economy", "carbon neutrality",
                                "EU energy policy"],
        "COM(2021) 554 final": ["pollution control measures", "environmental monitoring", "adaption to climate change",
                                "land use", "EU Member State", "greenhouse gas", "EU environmental policy",
                                "farming sector", "European forestry policy", "carbon neutrality"],
        "COM(2021) 555 final": ["pollution control", "environmental monitoring", "international agreement",
                                "adaptation to climate change", "EU emission allowance", "EU Member State",
                                "climate change", "greenhouse gas", "EU environmental policy",
                                "reduction of gas emissions"],
        "COM(2021) 557 final": ["energy consumption", "pollution control measures", "energy production",
                                "renewable resources", "greenhouse gas", "reduction of gas emissions", "energy saving",
                                "energy efficiency", "renewable energy", "EU energy policy"],
        "COM(2021) 558 final": ["energy consumption", "adaption to climate change", "energy cooperation", "energy use",
                                "reduction of gas emissions", "energy saving", "energy efficiency", "EU energy policy"],
        "COM(2021) 552 final": ["pollution control measures", "environmental protection", "emission trading",
                                "EU emission allowance", "air transport", "auction sale", "greenhouse gas",
                                "tradeable emission permit", "EU environmental policy", "reduction of gas emissions"],
        "COM(2021) 561 final": ["air quality", "aviation fuel", "air transport", "greenhouse gas",
                                "reduction of gas emissions", "sustainable mobility", "renewable energy", "biofuel"],
        "COM(2021) 562 final": ["pollution from ships", "energy resources", "renewable resources", "maritime transport",
                                "greenhouse gas", "reduction of gas emissions", "marine fuel"],
        "COM(2021) 559 final": ["hydrogen", "transport infrastructure", "motor vehicle pollution", "clean technology",
                                "electric vehicle", "substitute fuel", "reduction of gas emissions",
                                "sustainable mobility", "renewable energy"],
        "COM(2021) 564 final": ["third country", "originating product", "import(EU)", "adaption to climate change",
                                "emission trading", "carbon", "climate change", "greenhouse gas",
                                "surveillance concerning imports", "carbon neutrality"],
        "COM(2021) 563 final": ["fiscal policy", "energy-generating product", "environmental tax", "electrical energy"],
        "COM(2021) 567 final": ["pollution control measures", "environmental protection", "international standard",
                                "emission allowance", "air transport", "international transport", "carbon",
                                "greenhouse gas", "tradeable emission permit", "reduction of gas emissions"],
        "COM(2021) 571 final": ["pollution control measures", "environmental protection", "reserves",
                                "EU Emissions Trading Scheme", "EU emission allowance", "auction sale",
                                "greenhouse gas", "EU environmental policy", "reduction of gas emissions"],
        "COM(2021) 568 final": ["fund (EU)", "investment", "household", "adaption to climate change",
                                "emission trading", "transport user", "greenhouse gas", "reduction of gas emissions",
                                "micro-enterprise", "social impact"]
    }

    # COM 560 main page auf niederländisch, mglw falsch verlinkt, COM 556 nicht verfügbar auf englisch, COM 551 nur als PDF verfügbar
    # https://betterprogramming.pub/the-beginners-guide-to-similarity-matching-using-spacy-782fc2922f7c
    def process_text(text):
        doc = nlp(text.lower())
        result = []
        for token in doc:
            if token.text in nlp.Defaults.stop_words:
                continue
            if token.is_punct:
                continue
            if token.lemma_ == '-PRON-':
                continue
            result.append(token.lemma_)
        return " ".join(" ".join(result).split())

    def calculate_similarity(text1, text2):
        base = nlp(process_text(text1))
        compare = nlp(process_text(text2))
        return base.similarity(compare)

    df["clean_body"] = df.apply(lambda row: process_text(row["body"]), axis=1)

    compare = df["clean_body"][0]
    base = EUDESK["COM(2021) 550 final"][1]
    calculate_similarity(base, compare)
    weighted_similarity = []
    cleaned_comnumber = []
    for row in range(len(df)):
        comnumber = df["comnumber"][row]
        comnumber = comnumber.replace("\n", "")
        comnumber = comnumber.strip()
        cleaned_comnumber.append(comnumber)
    df["comnumber"] = cleaned_comnumber
    for row in range(len(df)):
        comnum = df["comnumber"][row].strip()
        if comnum not in EUDESK:
            weighted_similarity.append([])
            continue
        sim_list = []
        desk_list = []
        for desk in EUDESK[comnum]:
            sim = calculate_similarity(desk, df["clean_body"][row])
            sim_list.append(sim)
            desk_list.append(desk)
            tup = sorted(zip(sim_list, desk_list), reverse=True)
        weighted_similarity.append(tup)
    df["weighted_similarities"] = weighted_similarity
    print(df["weighted_similarities"])
    deskriptor = []
    for ws in df["weighted_similarities"]:
        a = []
        for ws_pair in ws[:5]:
            a.append(ws_pair[1])
        deskriptor.append(a)
    df["deskriptor"] = deskriptor

    persist_to_db(df)


class Command(BaseCommand):
    def handle(self, *args, **options):
        analyse_documents()
        get_context_labels()


if __name__ == '__main__':
    analyse_documents()
    get_context_labels()
