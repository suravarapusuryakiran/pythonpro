# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 14:18:04 2021

@author: USU1LO
"""




import glob
import numpy as np
import os
import pandas as pd
import json
import xmltodict
from pyparsing import ParseException
import pickle

from xml.parsers.expat import ExpatError
import xml.etree.ElementTree

from xml.parsers.expat import ExpatError

def parse_data_excel(filepath):
    
    print("function called...")
    df = pd.read_excel(filepath,sheet_name='Catalog_Page_20190717')
    print("excel has been picked")

    fill =  (df['MS']=='AV') | (df['MS']=='AS') 
    print("seems no error")

    data = fill.loc[["Material","Materialkurztext"]]  # Materialkurztext

    return data

catalog_filepath=r"Catalog_Page_20190717.xlsx"
Cache_filepath="data/Cache_lookup.cache"
force= True
data_lookup = parse_data_excel(catalog_filepath)

if force:
    with open(Cache_filepath, 'wb') as f:
        pickle.dump(data_lookup, f)

user_input = "R123456789"





people ={
    
    "first": ["Corey",'Jane','John'],
    "last":["Schafer",'John','Deo'],
    "email":["CoreyMSchafer@gmail.com",'JaneDoe@email.com','JohnDoe@email.com']
    
    }


dff= pd.DataFrame(people)
nill =  (dff['first']=='John') | (dff['last']=='John')
print(nill)


#============================================================================================

catalog_filepath=r"IH-Erzeugnisse_20210330.xlsx"
Cache_filepath="data/Cache_lookup.cache"
force= True
df = pd.read_excel(catalog_filepath,sheet_name='IH-Erzeugnisse_20210330')
condition =  (df['MS']=='AV') | (df['MS']=='AS')
data = df[condition]

data_filtered= data[["Material","Typkurzbezeichnung"]]
data_filtered['Typkurzbezeichnung'] = data_filtered['Typkurzbezeichnung'].str.strip()
data_filtered['Typkurzbezeichnung'] = data_filtered.Typkurzbezeichnung.str.replace(r'\&$', '', regex=True).str.strip()

data_filtered.to_excel("output.xlsx")  

with open('data_pickle.pkl','wb') as pickle_file:
    pickle.dump(data_filtered,pickle_file)

with open('data_pickle.pkl','rb') as pickle_file:
    new_data=pickle.load(pickle_file)


new_data_lookup= new_data.loc[new_data.Typkurzbezeichnung.str.startswith(("CYTROPAC","PGH4","4WRPEH 6"), na=False)] 



with open('new_data_pickle.pkl','wb') as pickle_file:
    pickle.dump(new_data_lookup,pickle_file)


with open('new_data_pickle.pkl','rb') as pickle_file:
    new_data=pickle.load(pickle_file)


User_Entered_code=811404529
print(type(User_Entered_code))
df= new_data[new_data.apply(lambda row: row.astype(str).str.contains(User_Entered_code).any(), axis=1)]
print(User_Entered_code)
con=(df['Material'] == User_Entered_code )
print(con)
    
filter_condition = (df['Material'] == User_Entered_code ) | (df['Typkurzbezeichnung'] == User_Entered_code) 
print(df.loc[filter_condition,"Material"])
material_number= df.loc[filter_condition,"Material"].to_string(index=False)
material_number=material_number.upper()
print(material_number)
type_code= df.loc[filter_condition,"Typkurzbezeichnung"].to_string(index=False)
type_code=type_code.upper()
print(f" material number is {material_number}")
print(f" material number is {type_code}")


fil = (new_data['Material'] == varib) | (new_data['Typkurzbezeichnung'] == varib)
print(new_data.loc[fil,'Material'].to_string(index=False))
print(new_data.loc[fil,'Typkurzbezeichnung'].to_string(index=False))

#df2=new_data[new_data["Material"] == varib]

#=============================================================================================================


xmlname= 'datasheets.xlsx'
mydf = pd.read_excel(xmlname,sheet_name='Sheet1')
product='PGH4'
language='english'
pd.set_option('display.max_colwidth', None)
mydf.loc[mydf['product']==product][language]

print(mydf.loc[mydf['product']==product][language])

link=mydf.loc[mydf['product']==product][language].to_string(index=False)




code='4WRPEH 6 C4 B12L-2X/G24K0/B5M'
xmlname= 'datasheets.xlsx'
mydf = pd.read_excel(xmlname,sheet_name='Sheet1')

if code.startswith("4WRPEH 6"):
    product="4WRPEH 6"
    link=mydf.loc[mydf['product']==product][language].to_string(index=False)
    print(link)




mask = np.column_stack([new_data[col].str.contains(r"\^", na=False) for col in new_data])
print(mask)



if df1.empty == True and df2.empty == True:
    flag= False
    print("Entered typecode is invalid")
else:
    flag=True 
    print("Entered typecode is valid")
    
    Material_num= df2["Material"].to_string(index=False)
    type_code= df2["Typkurzbezeichnung"].to_string(index=False)
    
    if type_code.startswith("CYTROPAC"):
        product="CYTROPAC"
        product_group = "power Unit"
        
    elif type_code.startswith("4WRPEH 6"):
        product="4WRPEH 6"
        product_group = "valves"
        
    elif type_code.startswith("PGH4"):
        product = "PGH4"
        product_group = "pumps"
    
    elif type_code.startswith("CG"):
        product = "CG"
        product_group = "Double rod cylinder"
        
    else:
        print("invalid product")


code='CGH3MF3/40/28/1500Asdfhasuhfaoismfomasoduf9a8efzuahsdufh'
link= "https://www.boschrexroth.com/ics/Modules/Configuration/?Modelcode=Rundzylinder&Configurator=Zylinder&Action=TypecodeEntry&Typecode=dankeschöne&InitConfiguration=1&o=Desktop"
url= link.replace('dankeschöne',code)
print(url)



    
    
    
    
