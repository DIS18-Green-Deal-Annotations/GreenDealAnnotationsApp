def main():
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
    
    doc = doc_1

    return doc
