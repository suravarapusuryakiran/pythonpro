

from itertools import dropwhile


def compare_classes(a,b):
    """
    compare classes and orderings between two products

    """
    pass


def is_compatible(a, b):
    """
    checks whether two products have compatible classes incl. ordering
    """
    dictA = a["classes"]
    productA= a["product"]["SELECTORID"]
    
    preElements_in_a = []
    postElements_in_b = []
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
            
            
            
                
            else:
                #print("if the product A attribute doesn't exist in productB, then it couldn't clash for these value, Hence no need to add in pre elementlist")
                pass
        
        
        
        # External loop statements 
        
        print("you have already iterated through on element, So it should in your pre element list no matter whether it is found or not unless it clashes")
        preElements_in_a.append(class_a_value) if class_a_value not in preElements_in_a else preElements_in_a # if it already exists in preelement list , it doesn't add
        print(f"printing pre element list by the end of single iteration of product A {preElements_in_a}")
    

    return returnvalue        

