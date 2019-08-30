""" Merges sets of object if they overlap by a minimum of all their objects
except one. By object is meant a tuple consisting of an object from both a and b
as the objects are paired on a one-to-one basis between sets a and b. A merge
will only happen if the Pairs objects from list a and list b on a
Inputs:
    a   Object set collection a
    b   Object set collection b
Outputs:
    a   Merged object set collection a
    b   Merged object set collection b
"""
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as ght
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

def dataTreeToList(aTree):
    theList = []
    for i in range(aTree.BranchCount ):
        thisListPart = []
        thisBranch = aTree.Branch(i)
        for j in range(len(thisBranch)):
            thisListPart.append( thisBranch[j] )
        theList.append(thisListPart)
    return theList

a = dataTreeToList(a)
b = dataTreeToList(b)


pair_sets = []
for i, ai in enumerate(a):
    pair_set = set()
    for j,wall in enumerate(ai):
        pair_set.add((wall,b[i][j]))
    
    # If this is the first room
    if len(pair_sets) <= 0:
        pair_sets.append(pair_set)
        continue
    
    # Go through existing sets
    for k in range(len(pair_sets)):
        #Add if it fits
        intersections = len(pair_sets[k].intersection(pair_set))
        if intersections >= 3:
            pair_sets[k] = pair_sets[k].union(pair_set)
            continue
        # Create new if it did not fit and end is reached
        if k == len(pair_sets)-1:
            pair_sets.append(pair_set)

# Go through existing sets combining them if they have enough intersection
for i in range(len(pair_sets)):
    for j in range(i):
        intersections = len(pair_sets[i].intersection(pair_sets[j]))
        if intersections >= 3:
            pair_sets[i] = pair_sets[i].union(pair_sets[j])
            pair_sets[j] = set()
pair_sets = [x for x in pair_sets if len(x)!=0]

# Ready output
room_lists = [list(x) for x in list(pair_sets)]
a, b = [], []
for s in pair_sets:
    sub_a = []
    sub_b = []
    for x in s:
        sub_a.append(x[0])
        sub_b.append(x[1])
    a.append(sub_a)
    b.append(sub_b)
a = ght.list_to_tree(a)
b = ght.list_to_tree(b)