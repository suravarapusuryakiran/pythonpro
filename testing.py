# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 16:30:07 2021

@author: USU1LO
"""


import glob
import os
import json
import pickle
from pyparsing import ParseException
import xmltodict
from xml.parsers.expat import ExpatError


def get_xml_files(basepath):
    basepath = os.path.join(basepath, "*.xml")
    filepaths = glob.glob(basepath)

    result = []
    for filepath in filepaths:
        if "test" in filepath:
            continue
        if "error" in filepath:
            continue

        result.append(filepath)

    return result



def print_states(states):
    factors = [s[1] for s in states]
    failures = sum(factors)
    success = len(factors) - failures
    print("success: {0}".format(success))
    print("failed: {0}".format(failures))

xml_basedir = r"C:\work\usu1lo\spyderPro\Q"
xml_files_cachepath = "xml_filenames.cache"
force = True

if os.path.isfile(xml_files_cachepath) and not force:

    with open(xml_files_cachepath, 'r') as f:
        xml_filepaths = json.load(f)
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
    r"WE6_73_A12\WE6_73_A12.xml",
    "Archiv/*.xml"
]))


def parse_metadata(inp):
    
    if not isinstance(inp, list):
        raise ParseException("metadata element should be a list" + str(inp))
    
    result = {}
    
    for l in inp:
        result[l["@Key"]] = l["@Value"]
    
    return result
        

def parse_col(t_list):
    #header
    value_option = []
    for element in (t_list):
        attribute_value_type = isinstance(element["AttributeValue"], list)
        values = element["AttributeValue"]
        if not attribute_value_type:
            values = [values]
            
        index = element["@Col"]
        classification = element["@Title"]
        
        for j in values:
            col = j["@Col"]
            shortdesc = j["@ShortDesc"]
            value = j["@Value"]
            value_option.append((index, classification, col, shortdesc, value))
            
    return value_option


def parse_content(content):
    t_list = [i for i in content if len(i.items()) == 7]
    return parse_col(t_list)

def parse_typecode(typecode,product):
    dict ={}
    value_option = []
    #t_list = [i for i in typecode if len(i.items()) == 4]
    for i in typecode["Item"]:
        MatNr = i["@MatNr"]
        Typecode = i["@Typecode"]
        Filepath=i["@Filepath"]
        Inactive=i["@Inactive"]
        value_option.append((MatNr, Typecode, Filepath, Inactive))
        dict[product]=value_option
    return dict
    

def parse_xml_file(filepath):
    result = {}
    state = ""
    try:
        try:
            with open(filepath, 'r', encoding='utf-16') as xml_file:
                data = xml_file.read()
        except UnicodeError:
            with open(filepath, 'r', encoding='utf-8') as xml_file:
                data = xml_file.read()
                
        data_dict = xmltodict.parse(data)             # xml to json
        # try to print this and check the output, so that you understand clearly how xml to datadic looks like

        result["meta"] = parse_metadata(data_dict["GenericSelector"]["MetaData"]["Item"])
        result["meta"]["filepath"] = filepath
        
        content = data_dict["GenericSelector"]["Translation"]["Language"]
        if isinstance(content, list):
            content = content[0]["Attribute"]
        else: 
            content = content["Attribute"]                   #  
            
        result["content"] = parse_content(content)          # contains list of tuple
        
        result["product"]= result["meta"]["PRESELECTTYPECODE"]
        product =result["product"]
        typecode = data_dict["GenericSelector"]["CAD"]
        result["codes"]=parse_typecode(typecode,product)
        
        
        state = filepath, 0, "success in file: {0}".format(filepath)
        
    except (ParseException, ExpatError, KeyError, UnicodeDecodeError, TypeError) as e:
        state = filepath, 1, "error in file: {0}. exception text: {1}".format(filepath, e)

    return result, state


for filepath in xml_filepaths:
    if filepath in ignored:
        continue
    # what does parse_xml_file returns ?
    result, state = parse_xml_file(filepath)
    #print(f"Result value is ${result} and the state value is ${state}")

    if "NAVIGATIONCATALOGID" not in result["meta"] or result["meta"]["NAVIGATIONCATALOGID"] == "IH":
        states.append(state)
        results.append(result)
    else:
        print(f"ommiting non IH catalog: {result}")
        
  
user_type_code= "CYTROPAC-1X/20/AF1AS04/2/A/WA/1/7035"
print("validating typecode ....")

for index, r in enumerate(results):
    data= r["meta"].get("NAVIGATIONPAGEID",404)
    if data == 404:
        if index == 250:
            continue
        else:
            product= r["meta"]["SELECTORID"]
    else:
        product= r["meta"]["SELECTORID"]
        for code in r["codes"][product]:
            db_Material_number= code[0]
            db_typecode=code[1]
            print(db_typecode)
            filename=code[2]

            if db_typecode == user_type_code:
                print("found________________")
                flag="found"
                break
                
            else:
                flag="Not found"
                


        

#
Cache_fp_Pageid_Lookup="data/cache/p_id_lookup.cache"
Cache_fp_Result="data/cache/results.cache"
log_messages=[s[-1] for s in states]

with open("log.txt", 'w') as f:
    f.write("\n".join(log_messages))

print_states(states)
