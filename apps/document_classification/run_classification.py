# -*- coding: utf-8 -*-
import os
import csv
from pandarallel import pandarallel
pandarallel.initialize()
import re


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



f = open('./results.csv', 'w')
writer = csv.writer(f, delimiter=";")
#names of rows
writer.writerow(['header', 'header2', 'body', 'doctype', 'titreobjet', 'comnumber', 'structure'])

#dokument count/ necessity to name it like dokument1, dokument2, document3 etc. when crawling
dir_path = r'../../html_processing/crawler/html'
for filename in os.listdir(dir_path):
    dok = open(os.path.join(dir_path, filename))
    dokstring = str(dok.read())
# because the hmtl headings are unstructured, there are different Versions:
# for Dok1 applies: <p class="li Heading1" id="_GoBack"> and <p class="li Heading1">
# for (Dok2, Dok3, Dok6, Dok7, Dok8, Dok9, Dok12, Dok13, Dok15, Dok16, Dok17) applies: <p class="li ManualHeading1"> <p class="li ManualHeading2"> <p class="li ManualHeading3"> (Dok3 has not: <p class="li ManualHeading2"> but: <span>• </span>) (mix from: <p class="li ManualHeading2"> and <span>• </span> also by Dok4)
# for Dok5 applies: <p id="_GoBack" class="Exposdesmotifstitre"> and next it goes on with: <span>1.</span> <span>2.</span> and insite it can have: <span>•</span>

#regex will find all of these different headings

    matches1 = re.findall(
                          '(<p.*?ManualHeading1[^°]+?.??<.*?ManualHeading1)|(<p.*?Heading1[^°]+?.??</p.*?)|'
                          '(<p\sid="_GoBack"\sclass="li\sHeading1">)([^°]+?.??<p\sclass="li\sHeading1">)|'
                          '(<p\sid="_GoBack"\sclass="Exposdesmotifstitre>)([^°]+?.??<p\sclass="li\sHeading1">)|'
                          #'(<p\sclass="li\sHeading1">)([^°]+?.??<p\sclass="li\sHeading1">)|'
                          #'(<p\sclass="li\sManualHeading1">[^°]+?.??)<p\sclass="li\sManualHeading1">|'
                          '(<p\sclass="li\sManualHeading1">)([^°]+?.??<dl\sid="footnotes">)|'
                          '(<p\sclass="li\sHeading1">)([^°]+?.??<dl\sid="footnotes">)',
                          dokstring)
    fullMatches1 = []
    if matches1:
        for submatches in matches1:
            for submatch in submatches:
                if submatch != '':
                    fullMatches1.append(str(submatch))
#there is also information on structure in the tag typedudocument
        typedudocument = re.findall('<p\sclass="Typedudocument_cp">.*?([^°]+?.??)</p>', dokstring)
#also information in the titreobjet-tag
        titreobjet = re.findall('<p\sclass="Titreobjet_cp">.*?([^°]+?.??)</p>', dokstring)
#also information in the rfrenceinstitutionelle-tag
        rfrenceinstitutionelle = re.findall('<p\sclass="Rfrenceinstitutionnelle">.*?([^°]+?.??)</p>', dokstring)
#there are not only heading1 but heading2 in the dokument, so we need to find these headings2 and exclude non-essential characters
        for match in fullMatches1:
            liHeaders2 = []
             #h1 = re.findall('(<p\sid="_GoBack"\sclass="li\sHeading1">\\\\n.*?\\\\n)|'
             #('(ManualHeading1[^°]+?.??</p>)|(Heading1[^°]+?.??</p>)', match))

            h1 = str(re.findall('(<p.*?ManualHeading1[^°]+?.??</p>)|(<p.*?Heading1[^°]+?.??</p>)', match))
            headers2 = re.findall('(<p.*?ManualHeading2[^°]+?.??</p)|(<p.*?Heading2[^°]+?.??<.*?Heading2)|'
                                  '(<p\sid="_GoBack"\sclass="li\sHeading2">[^°]+?.??)<p\sclass="li\sHeading2">|'
                                  '(<p\sid="_GoBack"\sclass="Exposdesmotifstitre>[^°]+?.??)<p\sclass="li\sHeading2">|'
                                  '(?<=<p\sclass="li\sHeading2">)([^°]+?.??)(?<=<p\sclass="li\sHeading2">)|'
                                  '<p\sclass="li\sManualHeading2">([^°]+?.??)<p\sclass="li\sManualHeading2">|'
                                  '(<p\sclass="li\sManualHeading2">)([^°]+?.??<dl\sid="footnotes">)|'
                                  '(<p\sclass="li\sHeading2">)([^°]+?.??<dl\sid="footnotes">)', match)
#define all structure Labels and find in the row header and append the results in structure row


#not in these ducuments but maybe in future ones (which are legally binding)

                    #if word in ['resolution'] not in tokens:
                    #    tokens.append('Resolution (legally binding)')
                    #if word in ['law'] not in tokens:
                    #    tokens.append('Law (legally binding)')
                    #if word in ['act'] not in tokens:
                    #    tokens.append('Act (legally binding)')
                    #if word in ['general'] and ['guidlines'] not in tokens:
                    #    tokens.append('General guidlines (legally binding)')
                    #if word in ['policy'] not in tokens:
                    #    tokens.append('Policy (legally binding)')
                    #if word in ['treaty'] not in tokens:
                    #    tokens.append('Treaty (legally binding)')
                    #if word in ['implementing'] and ['decision'] not in tokens:
                    #    tokens.append('Implementing decision (legally binding)')

#these words needed to be added in future in searchWords and in:
                    # if word in [''] not in tokens:
                    #    tokens.append('')

                    #evaluation
                    #report
                    #correction
                    #summary
                    #announcement
                    #impact assessment
                    #draft decision
                    #assasement
                    #reference
                    #provision
                    #proportionality
                    #subsidiarity
                    #corrigendum
                    #protocol
                    #opinion
                    #budget
                    #announcements
                    #information
                    #note
                    #judgment
                    #guideline
                    #recommendation
                    #ex-post-evaluation

            tokens = check_string_contains_token(str(typedudocument))
            tokens += check_string_contains_token(str(titreobjet))
            tokens += check_string_contains_token(str(rfrenceinstitutionelle))
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
                        header2 = re.findall('(<p.*?ManualHeading3[^°]+?.??</p)|(<p.*?Heading3[^°]+?.??<.*?Heading3)|'
                                              '(<p\sid="_GoBack"\sclass="li\sHeading3">[^°]+?.??)<p\sclass="li\sHeading3">|'
                                              '(<p\sid="_GoBack"\sclass="Exposdesmotifstitre>[^°]+?.??)<p\sclass="li\sHeading3">|'
                                              '(?<=<p\sclass="li\sHeading3">)([^°]+?.??)(?<=<p\sclass="li\sHeading3">)|'
                                              '<p\sclass="li\sManualHeading3">([^°]+?.??)<p\sclass="li\sManualHeading3">|'
                                              '(<p\sclass="li\sManualHeading3">)([^°]+?.??<dl\sid="footnotes">)|'
                                              '(<p\sclass="li\sHeading3">)([^°]+?.??<dl\sid="footnotes">)|'
                                              '(<span\sclass="num">[^°]+?.??</p)', match)

                    header2 = re.sub('(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\xa2)', '', str(header2))
                    tokens += check_string_contains_token(h1)
                    tokens += check_string_contains_token(header2)
                    #tokens = filter(None, tokens)
                    writer.writerow(
                        [h1, header2, headers2, typedudocument, titreobjet, rfrenceinstitutionelle, tokens])
            else:
                match = re.sub('(<.*?>)|(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\x..)', '', str(match))
                tokens += check_string_contains_token(str(matches1))
                filter(None, tokens)
                writer.writerow(
                    [matches1, '', match, typedudocument, titreobjet, rfrenceinstitutionelle, tokens])

#if html-tags wanted to be delated in header, header2 and in body:
    heading1 = []
    for header in heading1:
     heading1.append(re.sub('(<.*?>)|(\\\\n)|(\\\\r)|(\\n)|(\\\\xe2\\\\x80\\\\x99S)', '', str(header)))

    heading2 = []
    for header in heading2:
        heading2.append(re.sub('(<.*?>)|(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\x..)', '', str(header2)))
        match = re.sub('(<.*?>)|(\\\\n)|(\\\\r)|(\\\\xe2\\\\x80\\\\x..)', '', str(match))
#tokenisierung
    # tokenizer = RegexpTokenizer(r'\w+')
    #
    # writer.writerow["tokens"] = (lambda row: tokenizer.tokenize(row["header"].lower()), axis=1)
    #
    # for i in data['tokens']:
    #     if ('legal' in i or 'basis' in i):
    #         print("Legal Basis")
    #     if ('proposal' in i):
    #         print("Proposal")
    #     else:
    #         print("")
f.close()

########################
# Für <p class="li Heading1" id="_GoBack"> und <p class="li Heading1"> (Dok1)

# Für <p class="li ManualHeading1"> <p class="li ManualHeading2"> <p class="li ManualHeading3"> (Dok2, Dok6, Dok7, Dok8, Dok9, Dok12, Dok13, Dok15, Dok16, Dok17) (Dok3 hat kein <p class="li ManualHeading2"> sondern <span>• </span>) (mix aus <p class="li ManualHeading2"> und <span>• </span> bei Dok4)

# muss evtl. noch bearbeitet werden
# Für Dok5  <p id="_GoBack" class="Exposdesmotifstitre"> und dann kommt <span>1.</span> <span>2.</span> und innerhalb <span>•</span>

# Für Dok10 und Dok18 nur mit Beatifulsoup: <p class="Typedudocument_cp">...</p> und <p class="Titreobjet_cp">...</p>
##########################

# pattern = re.compile(r'(<p\sclass="li\sHeading1">[^°]+?.?<p\sclass="li\sHeading1">)')
# string = dokstring.rstrip().lstrip().strip().replace('\n','')

# headers1 = re.findall('(<p\sclass="li\sHeading1\sid="_GoBack">)([^°]+?.??<p\sclass="li\sHeading1">?<=)|(<p\sclass="li\sHeading1">)([^°]+?.??<p\sclass="li\sHeading1">?<=)|(?=<p\sclass="li\sHeading1">)([^°]+?.??<dl\sid="footnotes">)|(<p\sclass="li\sManualHeading1">)([^°]+?.??<p\sclass="li\sManualHeading1">?<=)|(<p\sclass="li\sManualHeading1">)([^°]+?.??<dl\sid="footnotes">)|(?<=<p\sid="_GoBack"\sclass="Exposdesmotifstitre>)([^°]+?.??<p\sclass="li\sHeading1">?<=)',
#                       dokstring)


# for word2 in searchWords:
#   if (typedudocument.find[word2] != -1):
#      if word2 in ['COMMUNICATION'] and 'Communication' not in tokens:
#         tokens.append('Communication')
#    if word2 in ['REGULATION'] and 'Regulation' not in tokens:
#       tokens.append('Regulation')