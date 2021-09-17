# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 13:30:24 2021

@author: richlink
"""

import pandas as pd

import requests

from bs4 import BeautifulSoup


def extract_pdf(document, default_document=None):
    
    lookup_search_url = r"https://www.boschrexroth.com/en/xc/myrexroth/media-directory-download?object_nr="

    response = requests.get(lookup_search_url + document)
    search_attribute = "media-directory-downloader-message"
    
    parsed_html = BeautifulSoup(response.text, features="html.parser")
    
    result_element = parsed_html.body.find('div', attrs={'class':search_attribute})
    if result_element is not None:
        
        possible_link = result_element.find("a")
        
        if possible_link is not None:
            
            return possible_link.get("href").split(".pdf/")[0] + ".pdf"
    
    return default_document
    

def read_excel_file(path):
        
    df_original = pd.read_excel(fpath)
    df = df_original.copy()
    # Get indexes where name column has value john
    indexNames = df[df["Data sheet"].isna()].index
     
    # Delete these row indexes from dataFrame
    df.drop(indexNames , inplace=True)
    
    return df, df_original

def is_document_from_requested_language(link, language):
    """
        checks whether the document has a sane language
        or some edge case (r-rs -> false positive for RS (spanish))
    """
    if link is None:
        return False
    
    filename = link.split('/')[-1]
    if filename.lower().startswith(language):
        return True
    
    return False
    

def find_documents(df):       
        
    languages = ["rd", "rf", "rs", "ri"]
    
    default_language = "re"
    
    results = {}
    
    for index, document in enumerate(df["Data sheet"].values.astype(str)):
        print(f"{index}/{len(df)} - {document}")
        
        if document in results:
            continue
        
        results[document] = {
            "re": None,
            "rd": None,
            "rf": None,
            "rs": None,
            "ri": None
        }
    
        # extract default language document
        full_document_name = default_language + document
                
        default_document_link = extract_pdf(full_document_name)
        if is_document_from_requested_language(default_document_link, default_language):
            results[document][default_language] = default_document_link
        else:
            print(f"ignored: {full_document_name} - expected language: {default_language} got {default_document_link}")
        
        for language in languages:
            full_document_name = language + document
            document_link = extract_pdf(full_document_name, default_document_link)
            
            if document_link != default_document_link and \
                not is_document_from_requested_language(document_link, language):
                    print(f"ignored: {full_document_name} - expected language: {default_language} got {default_document_link}")
                    
            else:
                results[document][language] = document_link
            
    return results
     

    
if __name__ == '__main__':
    
    fpath = r"C:\Users\usu1lo\Downloads\Hello.xlsx"
    print(f"reading file: {fpath}")
    df, df_original = read_excel_file(fpath)
    
    print(f"looking up {len(df)} document numbers")
    results = find_documents(df)
        
    data_sheet_indices = df_original[~df_original["Data sheet"].isna()].index
    df_original["Data sheet"] = pd.Series(df_original["Data sheet"], dtype="string")
    df_original["Data sheet"] = df_original.iloc[data_sheet_indices]["Data sheet"].apply(lambda x: x.split('.')[0])
    
    for document_id, documents in results.items():
        df_original.loc[df_original["Data sheet"] == document_id, "Link Deutsch"] = documents["rd"]
        df_original.loc[df_original["Data sheet"] == document_id, "Link Englisch"] = documents["re"]
        df_original.loc[df_original["Data sheet"] == document_id, "Link Französisch"] = documents["rf"]
        df_original.loc[df_original["Data sheet"] == document_id, "Link Spanisch"] = documents["rs"]
        df_original.loc[df_original["Data sheet"] == document_id, "Link Italienisch"] = documents["ri"]
        

    newfile = r"C:\Users\usu1lo\Downloads\hello_output.xlsx"
    
    print(f"saving to {newfile}")
    df_original.to_excel(newfile)

    



