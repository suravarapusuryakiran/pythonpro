

pageid_lookup = {}

results = {}

print("\n".join(map(str,pageid_lookup.PG1.unique())))

class_to_observe = "Schaltventile"
pageids = pageid_lookup[pageid_lookup.PG1 == "Schaltventile"].PageID.values.tolist()
sum_elements = sum(pageid_lookup.PG1 == "Schaltventile")



# get all results with matching pageid

fitting_elements = []

for r in results:
    if "NAVIGATIONPAGEID" in r["meta"] and r["meta"]["NAVIGATIONPAGEID"] in pageids:
        fitting_elements.append(r)
        

sum_typecodes = len(fitting_elements)


print("Schaltventile")
print("{0} - count of pageids".format(sum_elements))
print("{0} - number of pageids with typecode data".format(sum_typecodes))



elements_all_products = []
for r in fitting_elements:
    content = r["content"]
    
    elements = []
    for c in content:
        if c[1] not in elements:
            elements.append(c[1])

    elements_all_products.append(elements)

elements_all_products_flat = [item for sublist in elements_all_products for item in sublist]

abc = list(set(elements_all_products_flat))

with open('all-attributes.txt', 'w', encoding='utf-16') as f:
    f.write('\n'.join(sorted(abc)))


from collections import Counter
import operator
d = Counter(elements_all_products_flat)
e = [(k, v) for k,v in d.items()]
g = sorted(e, reverse=True, key=operator.itemgetter(1))









