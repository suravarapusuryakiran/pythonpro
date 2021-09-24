# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 15:54:19 2021

@author: USU1LO
"""

# Typschlüssel.xlsx
# Selector_Translations_Q_2021-08-05.xlsx



import pandas as pd
import math


def is_nan(x):
    return isinstance(x, float) and math.isnan(x)

pd.set_option('display.max_colwidth', None)

xmlname= 'Selector_Translations_Q_2021-08-05.xlsx'
newdf = pd.read_excel(xmlname,sheet_name='selector_translations')

titles = len(newdf.loc[newdf.Type == 'TITLE'])
newdf.loc[newdf.Type == 'TITLE', 'new_id'] = [n for n in range(1, titles+1)]
newdf['new_id'].fillna(method='ffill', inplace=True)

df = pd.read_excel("Typschlüssel.xlsx",sheet_name='Tabelle3')
family_list=df.SelectorID.tolist()


simple_list= []
column_names=["Classname", "family","Pos", "Type", "Lang", "Key", "Shorttext","Longtext","new_id"]
Thomas_df = pd.DataFrame(columns=column_names)


for index_i,family in enumerate(family_list):    #2-------------------------------- fixed
    
    
    print("index value is -", index_i)
    
    list_with_familyname=df.loc[df.SelectorID==family].values.tolist()
    list_of_classes=list_with_familyname[0][1:] # for each family we get list of classes 
    
    for index_j,klass in enumerate(list_of_classes):
        print("index value is -", index_j)
        
        # 1-------------------------------------------- fixed
        
        if klass in ["/","-","="] or is_nan(klass):
            pass
        
        else:
            
            
            df_rows=newdf.loc[ (newdf.SelectorID==family) & (newdf.Type=='TITLE') & (newdf.Key==klass) & (newdf.Lang=='DE') ]
            myid=df_rows.new_id.to_string(index=False)
            num=int(float(myid))  #9---------------------------------------- fixed
        
            innerdf=newdf.loc[ (newdf.SelectorID==family ) & (newdf.Type=='ATTR') & (newdf.new_id==num) & (newdf.Lang=='DE') ]
            #column_names=["Classname", "family","Pos", "Type", "Lang", "Key", "Shorttext","Longtext","new_id"]
            #Thomas_df = pd.DataFrame(columns=column_names)
            
            Pos=innerdf.Pos.tolist()   #3 ------------------------------ 
            Type=innerdf.Type.tolist()  # 4----------------------------
            Lang=innerdf.Lang.tolist()  #5--------------------------- 
            Key=innerdf.Key.tolist()   # 6--------------------------
            Shorttext=innerdf.Shorttext.tolist()   #7 ------------------
            Longtext=innerdf.Longtext.tolist()     #8 ------------------
            
            for i in range(len(Key)):
                final_list_line=[klass,family,Pos[i],Type[i],Lang[i],Key[i],Shorttext[i],Longtext[i],num] 
                Thomas_df.loc[len(Thomas_df)] = final_list_line
                
sorted_df=Thomas_df.sort_values('Classname')        
        
   
sorted_df.to_excel("new_output.xlsx")        
