

import glob
import os
import pandas as pd
import json
import pickle

from parse_xml import parse_xml_file


def get_xml_files(basepath):
    basepath = os.path.join(basepath, "*\\*.xml")
    filepaths = glob.glob(basepath)

    result = []
    for filepath in filepaths:
        if "test" in filepath:
            continue
        if "error" in filepath:
            continue

        result.append(filepath)

    return result


def parse_page_id_excel(filepath):

    df = pd.read_excel(filepath)

    df_non_empty = df.drop(df[df.PageID.isna()].index, axis=0)

    df_non_empty.ffill(inplace=True)

    sub = df_non_empty[["PageID", "PG0",
        "PG1", "PG2", "PG3", "PG4", "PRODUKT"]]

    return sub


def print_states(states):
    factors = [s[1] for s in states]
    failures = sum(factors)
    success = len(factors) - failures
    print("success: {0}".format(success))
    print("failed: {0}".format(failures))


catalog_filepath = r"data/raw/IH_Katalogstruktur_DCcatalog.xlsx"
xml_basedir = r"C:\work\usu1lo\spyderPro\Q"
# xml_basedir = "data/raw/Q/"

# pageid_lookup contains the excel data
pageid_lookup = parse_page_id_excel(catalog_filepath)
print(
    f" ---------------type of pageid_lookup is: ${type(pageid_lookup)} -------------------------------")
xml_files_cachepath = "data/raw/xml_filenames.cache"

force = True

if os.path.isfile(xml_files_cachepath) and not force:

    with open(xml_files_cachepath, 'r') as f:
        xml_filepaths = json.load(f)
        print(xml_filepaths)
else:
    # get_xml_files returns list of all xml files
    xml_filepaths = get_xml_files(xml_basedir)
    with open(xml_files_cachepath, 'w') as f:
        # json formated data into xml_filepaths
        json.dump(xml_filepaths, f)

results = []
states = []

ignored = list(map(lambda x: os.path.join(xml_basedir, x), [
    r"XYZ\XYZ.xml",
    r"HAD\validate_csv.xml",
    r"WE6_73_A12\WE6_73_A12.xml"
]))

for filepath in xml_filepaths:
    if filepath in ignored:
        continue
    # what does parse_xml_file returns ?
    result, state = parse_xml_file(filepath)
    print(f"Result value is ${result} and the state value is ${state}")

    if "NAVIGATIONCATALOGID" not in result["meta"] or result["meta"]["NAVIGATIONCATALOGID"] == "IH":
        states.append(state)
        results.append(result)
    else:
        print(f"ommiting non IH catalog: {result}")
        
        

Cache_fp_Pageid_Lookup="data/cache/p_id_lookup.cache"
Cache_fp_Result="data/cache/results.cache"

if force:
    with open(Cache_fp_Pageid_Lookup, 'wb') as f:
        pickle.dump(pageid_lookup, f)

if force:
    with open(Cache_fp_Result, 'wb') as f:
        pickle.dump(results, f)



log_messages=[s[-1] for s in states]

with open("log.txt", 'w') as f:
    f.write("\n".join(log_messages))

print_states(states)
        
        
        
        
####################################################################################################################
       


        
        
        
        

maxlength = 122
pageid = "dummy"

for index, r in enumerate(results):
    data = r.get("content", 1)          # r.get is useful in dict when some key value doesn't exist it can return desired value instead of error
    if data == 1:
        print(f"content key value not found at index -- {index}")
   
    else:
        length = len(data)
        print(f"-At index {index}length is {length } ")
        if length > maxlength:
            maxlength = length
            pageid = r["meta"]["NAVIGATIONPAGEID"]
            print(f" Maxlength is ------> {length} at index ---> {index} pageid --> {pageid}")


"""
    if "content" in r:
        # do logic
        pass
    else: 
        print(f"content key value not found at index -- {index}")
"""    



print(maxlength)
print(pageid)









# group by P groups
Pg1var=len(pageid_lookup.PG1.unique())
print(f"PG1 uniq --- {Pg1var} ")

print(pageid_lookup.PG1.unique())

Pg2var=len(pageid_lookup.PG2.unique())
print(f"PG2 uniq --- {Pg2var} ")

Pg3var=len(pageid_lookup.PG3.unique())
print(f"PG3 uniq --- {Pg3var} ")

Pg4var=len(pageid_lookup.PG4.unique())
print(f"PG4 uniq --- {Pg4var} ")


# len((pageid_lookup.PG3 + pageid_lookup.PG4).unique())
pg3undpg4var=int(len((pageid_lookup.PG3.unique())) + \
                 int(len(pageid_lookup.PG4.unique())))
print(f"PG3 plus PG4 --- { pg3undpg4var}")

len(pageid_lookup.PRODUKT.unique())
print(f"Unique products --- {len(pageid_lookup.PRODUKT.unique())} ")

# group by main type data

# get a list of all elements


gp2=pageid_lookup.PG2 == "Proportional-Wegeventile"
gp3=pageid_lookup.PG3 == "Direktgesteuert"

klaus_ventile=pageid_lookup[gp2 & gp3]


gp2=pageid_lookup.PG2 == "Regel-Wegeventile"
gp3=pageid_lookup.PG3 == "Direktgesteuert"

klaus_ventile2=pageid_lookup[gp2 & gp3]

klaus_ventile3=pd.concat([klaus_ventile, klaus_ventile2])

pageids=klaus_ventile3.PageID.values


result["meta"]["NAVIGATIONPAGEID"]

xml_infos=[]
