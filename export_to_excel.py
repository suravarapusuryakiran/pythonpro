

import pandas as pd
import numpy as np
import os
import pickle
from itertools import dropwhile
import xlwt
import sys
import re

#%%

"""

# need to initialize from main.py

pageid_lookup = {}
results = {}
"""

## initialization from main.py file cache

Cache_fp_Pageid_Lookup = "data/cache/p_id_lookup.cache"   #  Excel sheet
Cache_fp_Result = "data/cache/results.cache"              # data from xml    

if os.path.isfile(Cache_fp_Pageid_Lookup):
    with open(Cache_fp_Pageid_Lookup, 'rb') as f:
        pageid_lookup = pickle.load(f)                      #  pageid_lookup is the data from Excel sheet
        
        
if os.path.isfile(Cache_fp_Result):                          
    with open(Cache_fp_Result, 'rb') as f:
        results = pickle.load(f)                             # results is the data from xml
        

def try_split_pids(pids):
    #seperate pids into list of pid 
    if "," in pids:
        pids = pids.split(',')
        pids = list(map(str.strip, pids))
        return pids
    else:
        return [pids]
    

##################  purified result set, purified_resultset is the replacement for results ####################


purified_resultset = []

for index,r in enumerate(results):

    missing_content = r.get("content",404)
    missing_meta = r.get("meta",404)
    missing_pageid= r["meta"].get("NAVIGATIONPAGEID",404) # r.get
    missing_productname= r["meta"].get("SELECTORID", 404)
    
    
    if missing_content == 404 or missing_meta == 404 or missing_pageid == 404  or missing_productname == 404:
        
        if index == 250:
            continue
        else:
            
            print(f" Should remove these indexes __ {index} as there are no productname or page id's for these products")
        
    else:
        pid = r["meta"]["NAVIGATIONPAGEID"]
        product= r["meta"]["SELECTORID"]
        purified_resultset.append(r)
        print(f" pid list  -> {pid} and their corresponding product {product}")
        

###########################################################################################################################


def filter_elements(pageid_lookup, 
                    pg0_filter=None,
                    pg1_filter=None, 
                    pg2_filter=None, 
                    pg3_filter=None, 
                    pg4_filter=None):
    
    filtered = pageid_lookup
    if pg0_filter is not None:
        filtered = filtered[filtered.PG0 == pg0_filter]
    if pg1_filter is not None:
        filtered = filtered[filtered.PG1 == pg1_filter]
    if pg2_filter is not None:
        filtered = filtered[filtered.PG2 == pg2_filter]
    if pg3_filter is not None:
        filtered = filtered[filtered.PG3 == pg3_filter]
    if pg4_filter is not None:
        filtered = filtered[filtered.PG4 == pg4_filter]
    
    return filtered.copy()

elements_current_filter = filter_elements(pageid_lookup,                                        # data from excel sheet that contains infor for wege-seityventile
                                         # pg0_filter="IH_Produktkatalog",
                                         #pg1_filter= "Schaltventile"
                                         
                                          # pg3_filter="Wege-Sitzventile", 
                                          pg2_filter="Proportional-Wegeventile",
                                          #pg4_filter="Direktgesteuert"
                                          )

################################################################################################################

def new_filter_elements(page_id_lookup,  pg2_filter=None,pg3_filter=None):
    filtered = pageid_lookup
    if pg2_filter is not None and pg3_filter is not None:
        filtered= filtered.loc[ (filtered['PG2'] == pg2_filter) & (filtered['PG3']== pg3_filter)]
    
    return filtered.copy()
        

elements_current_filter = new_filter_elements(pageid_lookup,                                        # data from excel sheet that contains infor for wege-seityventile
                                         # pg0_filter="IH_Produktkatalog",
                                         #pg1_filter= "Schaltventile"
                                         
                                          # pg3_filter="Wege-Sitzventile", 
                                          pg2_filter="Proportional-Wegeventile",
                                          pg3_filter="Direktgesteuert"
                                          )

################################################################################################################


pageids_current_filter = elements_current_filter.PageID.values.tolist()                         #  we have 28 products under wege-sityventile


# select subset of elements from result set
fitting_elements = []

for r in purified_resultset:
    if "NAVIGATIONPAGEID" in r["meta"]:
        # maybe multiple pids comma seperated in excel list
        pids = try_split_pids(r["meta"]["NAVIGATIONPAGEID"])
        print(pids)
        for pid in pids:
            if pid in pageids_current_filter:                                       # if pid in the list of  28 pids then pick the data from xml
                print(r)
                fitting_elements.append(r)                                          # We found 25 pid's data from xml
        



#%%
# filter by classes and create a lookup table for humans

def get_flat_list_of_classes(fitting_elements):    # fitting elements contains content and meta of all matched items
    
    elements_all_products = []
    for r in fitting_elements:
        content = r["content"]
        
        elements = []
        for c in content:
            if c[1] not in elements:
                elements.append(c[1])
    
        elements_all_products.append(elements)
    
    return [item for sublist in elements_all_products for item in sublist]


def create_product_table_pg3_simple(fitting_elements, pageid_lookup):
    typecode_classes = np.ones((500,500)).tolist()    # 25 arrays/list of each contains 100
    
    for index, r in enumerate(fitting_elements):
        
        current_pageid = r["meta"]["NAVIGATIONPAGEID"]    # fiting (25 or 200+) elements only 
        filepath = r["meta"]["filepath"]    
    
        current_line = pageid_lookup[pageid_lookup.PageID == current_pageid]
        print(f"---------------{current_line}----------------")
    
        typecode_classes[index][0] = current_pageid
        typecode_classes[index][1] = current_line.PG1.values[0]
        typecode_classes[index][2] = current_line.PG2.values[0]
        typecode_classes[index][3] = current_line.PG3.values[0]
        typecode_classes[index][4]= current_line.PG4.values[0]
        typecode_classes[index][5] = current_line.PRODUKT.values[0]
        typecode_classes[index][6] = filepath
        
        for c in r["content"]:
            # finsterer xml file is 1 based columns (switch back to zero based indices)
            
            sub_index = int(c[0]) - 1
            print(f"-----intoftuple--------{int(c[0])}--------------------------")
            print(f"----subindex-----------{sub_index}----------------")
            value = c[1]
            print(f"---------------{value}----------------")            
            typecode_classes[index][sub_index+7] = value
    
    df = pd.DataFrame(typecode_classes)
    df.to_csv("data/output/test.csv")


#%%



flat_list = get_flat_list_of_classes(fitting_elements)  

flat_list_unique = list(set(flat_list))                  # for 25 fitting elements we have 30 uniq classes flat list unique


data = create_product_table_pg3_simple(fitting_elements, pageid_lookup)

     

#%%

## filter by classes and also merge the attributes

def filter_by_class(fitting_elements, pageid_lookup):
    class_attribute_lookup = {}
    
    # iterate through all (prefiltered) elements
    for index, r in enumerate(fitting_elements):
        # index, r = 0, fitting_elements[0]
        # get the pageid (needed to extract the product name)
        current_pageid = r["meta"]["NAVIGATIONPAGEID"]                           # pageid from xml
        current_line = pageid_lookup[pageid_lookup.PageID == current_pageid]     # current line (product name, ) from excel sheet 
        product_name = current_line.PRODUKT.values[0]                            # product name from excel sheet                   
        print("working on {0} - {1}".format(index, product_name))                   # index from fitting_elements and product name from excel
        
        # loop through the content for that one product
        # list of classes: (column, classname, shortdescription, attributevalue, attribute_option)
        for c in r["content"]:
            # c = r["content"][0]
            classname = c[1]                           # taking the entire data from xml 
            attribute_value = c[3]                      # taken from xml
            attribute_option = c[4]                     # taken from xml
            # add new class to the dictionary if necessary
            if classname not in class_attribute_lookup:         # seems every class should have a vals, products and option
                class_attribute_lookup[classname] = {"vals": [], "products":[], "option": []}     # class name from xml
            
            # add the attributes to the class
            if attribute_option not in class_attribute_lookup[classname]["option"] or \
                attribute_value not in class_attribute_lookup[classname]["vals"]:              
                    
                class_attribute_lookup[classname]["vals"].append(attribute_value)
                class_attribute_lookup[classname]["option"].append(attribute_option)   # attribute option from xml
            
            # add the product to the class (product uses this class)
            if product_name not in class_attribute_lookup[classname]["products"]:
                class_attribute_lookup[classname]["products"].append(product_name)   # product name form excel sheet
            
    return class_attribute_lookup


def create_dataframe_from_class_lookup(class_attribute_lookup):
        
    # for the excel file, to make it more readable check the longest value column to start with the products after that
    longest_column = max([len(i["vals"]) for i in class_attribute_lookup.values()])
    print(f"longest column is = {longest_column} ")
    
    # create a 2d list of all classes
    
    # class_option, attribute1_opt, attribute2_opt, ... attributen_opt, space, space1 ... spacen, product1, product2, ..., productn
    # class_value, attribute1_val, attribute2_val, ... attributen_val, space, space1 ... spacen, product1, product2, ..., productn
    stacked = []
    for classname, elements in class_attribute_lookup.items():
        stacked.append([classname + " Auswahl", *elements["option"], *([""] * (longest_column+1-len(elements["vals"]))), *elements["products"]])
      
        
        stacked.append([classname + " Beschreibung", *elements["vals"], *([""] * (longest_column+1-len(elements["vals"]))), *elements["products"]])
        
      
        
    # create a dataframe and transpose for easier readbility
    df = pd.DataFrame(stacked)
    # save to output
    return df


#%%

#current_pg="Wege-Sitzventile"
current_pg = "Proportional-Wegeventile"


class_attribute_lookup = filter_by_class(fitting_elements, pageid_lookup)
                    
df = create_dataframe_from_class_lookup(class_attribute_lookup)

df.T.to_csv(f"data/output/{current_pg}.csv", index=False, header=False)
                                      
#df.T.to_excel(f"data/output/{current_pg}.xls", index=False, header=False)



 











#################################################################################################### search product with respective pageid

# finding product with respective to pid in fitting_elements

pid="p686851"

for index, r in enumerate(fitting_elements):
    
    
    if r["meta"]["NAVIGATIONPAGEID"] == pid:
        product= r["meta"]["SELECTORID"] 
        print(f" Product {product} found at index--> {index} ")
        
        
# finding product with respective to pid in results

pid = "p691425"

for index, r in enumerate(results):
    
    data= r["meta"].get("NAVIGATIONPAGEID",404) # r.get
    if data == 404:
        
        if index == 250:
            continue
        else:
            product= r["meta"]["SELECTORID"]
            #print(f"page id not found for the product {product} at index __ {index}")
        
    else:
        if r["meta"]["NAVIGATIONPAGEID"] == pid:
            product= r["meta"]["SELECTORID"]
            print(f" Product {product} found at index--> {index} ")
            


# dictionary contains list of pid's along with product names
fitting_products = {}

for r in fitting_elements:
    key = r["meta"]["NAVIGATIONPAGEID"]
    value = r["meta"]["SELECTORID"]
    fitting_products[key]=value



# pid's not in pageids_current_filter
pageids_current_filter_new = []
for index,pid in enumerate(pageids_current_filter):
    if pid not in pageids_current_filter_new:
        print(f" pid {pid} at index {index} doesn't have all properties")
        


            
force = True
Cache_fp_fitting_elements="data/cache/fittingele.cache"

if force:
    with open(Cache_fp_fitting_elements, 'wb') as f:
        pickle.dump(fitting_elements, f)   
        





############################################################################################

## To create classes with indexes after exclusing delimiters


filtered_product =[]  # contains 


for index,r in enumerate(fitting_elements):        # r gives product level
    classlist = []    # for list of classes won't be used in later stage
    classes = {}        # classes dictionary
    product= {}         # corresponding product dictionary
    rootdict = {}       # contains classes and products

    for productlist in r["content"]:   # r[content"] gives list of tuple,  so product contains tuple
        
        attribute=productlist[1]
        if attribute == "-" or attribute == "/":
            continue
        else:
            if attribute in classlist:
                continue
            else:
                classlist.append(attribute)
                
    print(classlist)
    print("------------------------------------------")
    for key,value in enumerate(classlist):
        classes[key]=value
    
    #
    rootdict["classes"]=classes
    
    productvalue=r["meta"]["SELECTORID"]
    product["SELECTORID"]=productvalue
    
    rootdict["product"]=product
    
    filtered_product.append(rootdict)
    
    

    

force = True
Cache_fp_filtered_products="data/cache/filteredproducts.cache"

if force:
    with open(Cache_fp_filtered_products, 'wb') as f:
        pickle.dump(filtered_product, f) 
        

################################ is_compatible function  ###############################################


product_clash = {}
no_clash={}


def is_compatible(a, b):
    """
    checks whether two products have compatible classes incl. ordering
    """
    dictA = a["classes"]
    productA= a["product"]["SELECTORID"]
    
    preElements_in_a = []
    returnvalue = False
   
    
    
    productB= b["product"]["SELECTORID"]
    
    dictB= b["classes"]
    
    print("------------------------------------------------------------------------------------------------")
    
    for index_A, class_a_key in enumerate(dictA):
        class_a_value= dictA[class_a_key]                # 1 typ 
        #print(f" class a value {class_a_value}")           # 2 haupt
        
        
        for index_B, class_b_key in enumerate(dictB):
            class_b_value = dictB[class_b_key]          # 1,2,3,4,6,7 typ
            #print(f" class B value {class_b_value}")
            
            lastindex_of_B= int( list(dictB)[-1] )
            
            print(f" for product {productA} to product {productB} last index of {productB} is {lastindex_of_B}")
            print(f" Value of product a is {class_a_value} and value of product B is {class_b_value} ")
            
            if class_a_value == class_b_value and  index_B != lastindex_of_B: # found and not last index of B
                
                # A's pre element list shouldn't fall under post element list of B
                print(f" when matches for class value {class_a_value} and product {productA} to product {productB}")
                
                # found the match at index 0
                
                if len( preElements_in_a) == 0 and index_B == 0 :
                    preElements_in_a.append(class_a_value)    # add the value to the list and break the innerloop B, taking next attribute from class A  
                    print(f"added class {class_a_value} to pre element list")
                    break  
                
                elif len(preElements_in_a) ==0 and index_B !=0:  # list is still empty to compare with other elements,so add to pre value and break 
                    preElements_in_a.append(class_a_value)
                    print(f"added class {class_a_value} to pre element list")
                    break
                                                                                         
                else:   # found and pre list is not empty, iterate through post list from index b and check pre list falls into it or not
                    flag=0
                    
                    print(f"list is not empty, hence iterating from the existing list {preElements_in_a} ")
                    for pre_list_value in preElements_in_a:     # iterate through pre list one by one
                        
                        post_index = index_B + 1
                        
                        # shoud nöt fall under post list of B
                        for post_list_key in dropwhile(lambda k: k != post_index, sorted(dictB)): # iterate through post list one by one
                            print(f"running loop from index {post_index} till end {lastindex_of_B} ")
                            post_list_value = dictB[post_list_key]
                            
                            print(f"... checking if pre list value {pre_list_value} equals with the post list value {post_list_value}")
                        
                            if pre_list_value == post_list_value:
                                
                                print(f" products {productA} is clashing with product {productB} for value {pre_list_value}")
                                product_clash[productA] =productB
                                flag=1
                                returnvalue=True
                                break
                            
                    if flag==1:
                        print(f" There is a clash between {productA} and {productB}, Hence exiting the program")
                        
                        
                    else:
                        # enters 1) when it value equals, 2) when pre element list is not empty 3) when it doesn't clash with pre elements
                        print(f" {class_a_value} exists in product B but doesn't no clash between pre and post elements as of now")
                        preElements_in_a.append(class_a_value)
                        print(f"Adding {class_a_value} to the preelement list ... {preElements_in_a}")
            
            
            elif class_a_value == class_b_value and  index_B == lastindex_of_B:
                # There are no post elements in product B to class with pre elements of product A as this is the lastindex in product B
                print(f" {class_a_value} exists in product B but doesn't no clash between pre and post elements as of now")
                preElements_in_a.append(class_a_value)
                print(f"Adding {class_a_value} to the preelement list ... {preElements_in_a}")
                
            
                
            else:
                #print("if the product A attribute doesn't exist in productB, then it couldn't clash for these value, Hence no need to add in pre elementlist")
                pass
        
        
        
        # External loop statements 
        
        print("you have already iterated through on element, So it should in your pre element list no matter whether it is found or not unless it clashes")
        preElements_in_a.append(class_a_value) if class_a_value not in preElements_in_a else preElements_in_a # if it already exists in preelement list , it doesn't add
        print(f"printing pre element list by the end of single iteration of product A {preElements_in_a}")
    
    return returnvalue 
                


print("<-------------------------------------------------------->")

#####################################  calling is_compatible function #################################

product_clash = {}
no_clash={}


for mainIndex,productA in enumerate(filtered_product):  # every single product   1
            proa= productA["product"]["SELECTORID"]
            
            for index,productB in enumerate(filtered_product):
                prob=productB["product"]["SELECTORID"]
                
                result = is_compatible(productA, productB)  # to all products  1-25
                
                if result == True:
                    product_clash[proa]=prob
                
                else:
                    no_clash[proa]=prob


######################### Exclude clashing products from the list of products ################################

# After taking a look at product_clash and no clash , we exclude those products that clashes , here for wege sitzventile we exclude products that starts with k

#complete_filter = []

#for x in filtered_product:
#   if x["product"]["SELECTORID"].startswith(('K','k')):
#        pass
#    else:
#        complete_filter.append(x)
################################################ Remodifying complete_filter / you have to execute this #######################################
complete_filter = []

for x in filtered_product:
    if x["product"]["SELECTORID"] in ["WREE-3X", "STW0196"]:
        pass
    else:
        complete_filter.append(x)


####################################### Again executing product clash from complete_filter ##########################

product_clash = {}    # After excluding product clash .! this will be null and ready to create super code
no_clash={}

for mainIndex,productA in enumerate(complete_filter):  # every single product   1
            proa= productA["product"]["SELECTORID"]
            
            for index,productB in enumerate(complete_filter):
                prob=productB["product"]["SELECTORID"]
                
                result = is_compatible(productA, productB)  # to all products  1-25
                
                if result == True:
                    product_clash[proa]=prob
                
                else:
                    no_clash[proa]=prob
                    
############################## Total number of classes from complete filter as list#######################################################################################



totalnumclasses= []
for plist in complete_filter:
    for key,value in plist["classes"].items():    
        totalnumclasses.append(value) if value not in totalnumclasses else totalnumclasses
    
######################################################################################
# No need to execute this  

print("totalnumclasses contains list of classes from complete_filter")

superdict = {} 

for i in range(len(totalnumclasses)):
    className = totalnumclasses[i]  # taking single class from list of classes
    
    leastindex=100                  # taking it's least index is 100.!
    
    for product_dict in complete_filter:
        
        for key,value in  product_dict["classes"].items():
            
            if className == value:
                if key <= leastindex:
                    leastindex = key
                    superdict[key] = value
                
            
            
        







########################## Finding baseline product ######################################################################################
# by default max, change it to min if you want

baseline=[]
maxlength = 5
# minlength = 10
max_len_product_index = "1"
min_len_product_index = "1"

for index, r in enumerate(complete_filter):
    data = r.get("classes", 1)          # r.get is useful in dict when some key value doesn't exist it can return desired value instead of error
    if data == 1:
        print(f"content key value not found at index -- {index}")
   
    else:
        length = len(data)
        print(f"-At index {index}length is {length } ")
        if length > maxlength:
            maxlength = length
            baseLine_product = r["product"]
            baseline = r
            max_len_product_index=index

print(f"max length for the product {baseLine_product} at index {max_len_product_index}")
baseline_dict=baseline["classes"]

################################################################################################################
 
#=================================================================================================================    

                
###################################################################################################################     


baseline_dict=baseline["classes"]
supercode = []

original_stdout = sys.stdout # save a reference to the original standard output

with open('output.txt','w') as f:
    sys.stdout = f
    print('This message will be written to the file')
        
    # iterating through each and every class from baseline class
    
    
    for class_index,class_name in baseline_dict.items():  # changed from baseline_dict to createdbaseline
        
        # for loop to iterate each and every product from complete_filter list of products
        
        for product_index,product_dict in enumerate(complete_filter): # product_dict contains single product dictionary
            subset_counter=0
            #

            
            for product_key,product_value in product_dict["classes"].items():
                #print(f" product key is {product_key}  and product value is {product_value}")
                
                #lastindex_in_product = int( list(product_dict["classes"])[-1] )  # also taking last index in product dict
                
                
                
                if class_name ==  product_value and int(product_key) == 0:
                    # if product value of product and class name equalls at first index then only it gets added 
                    supercode.append(class_name) if class_name not in supercode else supercode # supercode is never empty 
                    
                elif (class_name == product_value) and ( class_index < product_key ):
                    print(f" class {class_name} exists in product {product_key} where class index = {class_index} and product index = {product_key}")    
                    # this condition exists only when product class order is greater than baseline,
                    #in such case we need all classes of porduct in order 
                    
                    print(f"Super code was {supercode}")
                        
                    preset = {x: y for x, y in product_dict["classes"].items() if int(x) <= int(product_key)}
                      
                    print(f" for the product {product_index} presubset is -- {preset}")
                    print(f" preset length is = {preset} and subset_counter length = {subset_counter}")
                    
                    if  len(preset) >= subset_counter:
                        
                        
                        for i in preset: # Here i is the index in preset which is key
                            value= preset[i]
                            #supercode.insert(i,value) if value not in supercode else print(" value is there so letting it be")
                            
                            if value not in supercode and i==0:
                                # which means preset is greater than supercode and first value in preset isn't there in supercode.!
                                supercode.insert(0,value) if value not in supercode else supercode
                            
                            
                            if value not in supercode and i !=0:
                                # supercode won't be empty by the time it reaches this condition,
                                #So, if found a new value in preset then take index -1 value of it and check it in supercode take that index and add next to it 
                                preindex = i -1;
                                prevalue = preset[preindex]
                                
                                for supercode_index in range(len(supercode)):
                                    supercode_value = supercode[supercode_index]
                                    if supercode_value == prevalue:
                                        # insert, prevalue next to supercode_index
                                        print(f" Inserting {value} next to {prevalue} in supercode at index {i+1}")
                                        supercode.insert(supercode_index +1, value) if value not in supercode else supercode
                                
                                
                        
                        print(f" <-- supercode after operation for product {product_index} is =  {supercode} -->")
                        print()
                    
                    subset_counter = len(preset)
            
                
            
            else:
                        # falls when class exists in product but class_index (5) > product index (2)
                        # (which means missing few classes in product and exists in baseclass no problem) take baseclass as supercode.
                                      
                    
                    # occurs when class itself not there in product list, then also we have to add class in supercode
                    supercode.append(class_name) if class_name not in supercode else supercode   # if it already exist and list gets added by else condition in previous iteration then we don't add
                    
            
            #print(f" super code for class index {class_index} class name {class_name} --> for product {product_index} at index {product_key} supercode is {supercode}  ")
            
    
    sys.stdout = original_stdout
                

################################################################################################################
        
############ finding  ############################################## 
pattern = '^Steuerölversorgung'

for index,x in enumerate(complete_filter):
    
    for key,value in x["classes"].items():
        result = re.match(pattern, value)
        if result :
            print(f"found value at index - {index}")
 
