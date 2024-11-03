transections = {}
unique_items = set()

with open("input.txt", "r") as file:
    for line in file:
        tid, items = line.strip().split(":")

        item_list = tuple([item.strip() for item in items.split(",")])
        transections[tid.strip()] = item_list
        unique_items.update(item_list)


unique_items = sorted(unique_items)
# print("Transactions Dictionary:", transections)
# print("Unique Items List:", unique_items)

support_count =  int(input("Enter support count: "))
itemsets = []
itemsetCandid = list(unique_items)

def convertToTuple(itemset):
    tupledItemset = [(i,) for i in itemset]
    return tupledItemset

def nextItemSetCandid(itemset):
    if(type(itemset[0]) != tuple):
        itemset = convertToTuple(itemset)
    
    candidSet = set()
    for i in range(len(itemset)-1):
        for j in range(i+1, len(itemset)):
            temp = set(itemset[i] + itemset[j])
            temp = sorted(tuple((temp)))
            if(len(temp))==len(itemset[0])+1:
                candidSet.add(tuple(temp))

    return candidSet

def is_subtuple(candid, items):
    if len(candid) > len(items):
        return False
    
    for i in candid:
        if i not in items:
            return False
    return True


itemsetCandid = convertToTuple(itemsetCandid)

for i in range(100):
    itemset=[]
    for candid in itemsetCandid:
        count = 0
        for items in transections.values():
            if is_subtuple(candid, items):
                count += 1
        if count >= support_count:
            # print("selected:", candid, "count", count)
            itemset.append(candid)
    
    if(len(itemset)==0):
        break
    itemsets.append(itemset)
    itemsetCandid = nextItemSetCandid(itemset)

for i in range(len(itemsets)):
    print(f"{i+1}-items sets: ", itemsets[i])