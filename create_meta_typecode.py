



"""
    create a sorted list of the classes 
    try to be smart about it
    
    p1: 0 1 2 4 5
    p2: 0 1 3 4 5
    
    meta: 0 1 2 3 4 5
    p1:   x x x   x x
    p2:   x x   x x x
"""

def create_attribute_lookup(fitting_elements, pageid_lookup):
    
    classes_unsorted = []
        # iterate through all (prefiltered) elements
    for index, r in enumerate(fitting_elements):
        new_class = []
        # get the pageid (needed to extract the product name)
        current_pageid = r["meta"]["NAVIGATIONPAGEID"]
        current_line = pageid_lookup[pageid_lookup.PageID == current_pageid]
        product_name = current_line.PRODUKT.values[0]
        print("working on {0} - {1}".format(index, product_name))
        
        # loop through the content for that one product
        # list of classes: (column, classname, shortdescription, attributevalue, attribute_option)
        for c in r["content"]:
            if c[1] not in new_class:
                new_class.append(c[1])
            
        classes_unsorted.append(new_class)
        
    candidate_class = None
    Finished = False
    current_index = 0
    current_column = []
    product_current_index = [0]*len(classes_unsorted)
    
    left, right = classes_unsorted[0], classes_unsorted[1]
    
    current_element = left[0]
    for i in range(len(right)):
        if current_element == right[i]:
            break
    
    return classes_unsorted


def created_sorted_class_list(fitting_elements, pageid_lookup):
    cls_attrib_lookup = create_attribute_lookup(fitting_elements, pageid_lookup)
    
