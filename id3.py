## Author: Grimmag
#
#   Jsem si vedom, ze to urcite slo udelat lip/efektivnej apod
#   Ale co, vypocitat to vypocita
#   Prosim, nesmejte se mi ^.^

#   Vystup jde na stdout, ale klidne si ho muzete vypsat do filu.
#   Staci prepsat print uplne na konci souboru

#   Spousteno ve VSCode na WIN10 v cmd pomoci 'python'
#             a v Ubuntu terminalu pomoci 'python3'

import math

# dot = 0   pro generaci .md souboru
# dot = 1   pro generaci .dot souboru (pro generaci grafu) 
dot = 0

# Staci nakopirovat svoje atributy, objekty a popr. prejmenovat classes
# do nasledujicich 3 promennych.
# VAROVANI: Testovane pouze na nasledujicich atributech (resp. 4 atributy s poctem hodnot [3,3,3,2])

attributes = """velikost : maly stredni velky
    srst : kratka dlouha bez
    barva : cerny bily hnedy
    spolecensky : ano ne"""

classes = ['V','N','Q']

objects = """1 N velky bez cerny ne
    2 V maly bez cerny ano
    3 Q stredni dlouha bily ano
    4 V stredni kratka cerny ano
    5 Q velky kratka bily ano
    6 N maly bez hnedy ano
    7 V maly bez bily ano
    8 Q stredni kratka hnedy ne
    9 N velky bez hnedy ano
    10 V velky bez cerny ano
    11 N velky dlouha hnedy ano
    12 N stredni dlouha cerny ano
    13 N stredni bez hnedy ano
    14 Q stredni bez bily ne
    15 Q maly dlouha hnedy ano
"""

buffer = ""
def recursion(string,obj, att, nameIndex):
    global buffer
    obj_index = string.split(',')
    new_obj = []
    for i in obj_index:
        for j in range(len(obj)):
            if str(i) in obj[j]:
                new_obj.append(obj[j])

    claCount = [0,0,0]
    for item in new_obj:
        if item.count(classes[0]):
            claCount[0] += 1
        if item.count(classes[1]):
            claCount[1] += 1
        if item.count(classes[2]):
            claCount[2] += 1

    claSum = claCount[0]+claCount[1]+claCount[2]
     
    i = 0
    for item in claCount:
        if item == claSum:
            buffer += "Item" + str(nameIndex) + " [" + box_round + "label=\"" + classes[i] + "\"]\n"
            return
        i += 1
    
    
    subEnt = []
    for x in claCount:
        if x == 0:
            subEnt.append(0)
        else:
            subEnt.append((x/claSum)*math.log2(x/claSum))

    EntS = -subEnt[0]-subEnt[1]-subEnt[2]

    num_of_att = int(len(att)/2)
    Gain = []
    for j in range(1,num_of_att+1):
        clbA = clbB = clbC = 0
        clbCount = [[0,0,0],[0,0,0],[0,0,0]]
        i=0
        for attrib in att[2*j-1]:
            for item in new_obj:
                if item.count(classes[0]) and item.count(attrib):
                    clbCount[i][0] += 1
                if item.count(classes[1]) and item.count(attrib):
                    clbCount[i][1] += 1
                if item.count(classes[2]) and item.count(attrib):
                    clbCount[i][2] += 1
            i += 1

        clbSum = []
        for item in clbCount:
            clbSum.append(item[0]+item[1]+item[2])

        subEntAtt = []
        tempEntAtt = []
        i = 0
        for item in clbCount:
            tempEntAtt.clear()
            for x in item:
                if x == 0:
                    tempEntAtt.append(0)
                else:
                    tempEntAtt.append((x/clbSum[i])*math.log2(x/clbSum[i]))
            subEntAtt.append(-tempEntAtt[0]-tempEntAtt[1]-tempEntAtt[2])
            i += 1

        Gain.append(EntS - (clbSum[0]/claSum)*subEntAtt[0] - (clbSum[1]/claSum)*subEntAtt[1] - (clbSum[2]/claSum)*subEntAtt[2])

    max_index = Gain.index(max(Gain))
    
    i=0
    string="{"
    for item in Gain:
        string += att[2*i] + "=" + str(format(round(Gain[i],4),'.4f')) + "|"
        i += 1
    string = string[:-1] + "}"
    buffer += "Item" + str(nameIndex) + " [" + record + "label=\"" + att[max_index*2] + "|" + string + "\"]\n"
    
    tempAtt = []
    j = 1
    for i in att[max_index*2+1]:
        string = "{"
        for item in new_obj:
            if i in item:
                string += item[0] + ","
        string = string[:-1] + "}"
        if len(string)>2:
            buffer += "Item" + str(nameIndex) + " -> Item" + str((nameIndex+j)*10) + " [label=\"" + i + " " + string + "\"]\n"
            tempAtt.clear()
            for item in att:
                tempAtt.append(item)
            del tempAtt[2*max_index:2*max_index+2]
            recursion(string[1:-1], new_obj, tempAtt, (nameIndex+j)*10)
            j += 1
    

box_round = ""
record = ""
if (dot == 1):
    box_round = "shape=box, style=rounded, "
    record = "shape=record, "
    buffer += "digraph {\n"


att = attributes.replace(':','\n').split('\n')
i = 0
for item in att:
    if (i%2):
        att[i] = item.split(' ')
        att[i].remove('')
    else:
        att[i] = item.replace(' ','')
    i += 1

obj = objects.split('\n')
i = 0
for item in obj:
    obj[i] = item.split(' ')
    x = obj[i].count('')
    for j in range(x):
        obj[i].remove('')
    i += 1
    if len(obj[i])==0:
        obj.remove(obj[i])



num_of_att = int(len(att)/2)

string = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15"
recursion(string, obj, att, 1)
if dot == 1:
    buffer += "}"

# buffer = text k vypsani...
print(buffer)