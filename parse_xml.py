

from pyparsing import ParseException
import xmltodict

from xml.parsers.expat import ExpatError

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
        state = filepath, 0, "success in file: {0}".format(filepath)
        
    except (ParseException, ExpatError, KeyError, UnicodeDecodeError, TypeError) as e:
        state = filepath, 1, "error in file: {0}. exception text: {1}".format(filepath, e)

    return result, state
