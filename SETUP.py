"""
This script sets up the data for our database.
Run this script to
- fetch latest green deal documents
- populate html code database table for document viewer
- populate date extraction database table for timeline
- populate classification database tables
"""
# from html_processing.get_and_process import crawl_and_process_com
from html_processing.write_to_db import main as generate_htmlcode_data
from html_processing.date_extraction import main as generate_timeline_data
from html_processing.addcom import add_com_ids
from html_processing.classification import analyse_documents, get_context_labels


def main():
    # crawl latest green deal documents
    # crawl_and_process_com()
    # TODO: crawler wirft Fehler
    # put them into database with document links applied
    generate_htmlcode_data()
    # put data for timeline into database
    # NOTE: python -m spacy download en_core_web_sm MUST BE INSTALLED
    generate_timeline_data()
    add_com_ids()
    analyse_documents()
    get_context_labels()


if __name__ == '__main__':
    main()
