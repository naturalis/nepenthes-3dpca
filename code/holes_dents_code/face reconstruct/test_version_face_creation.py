#for creating new faces when there is a dent in the pitcher

import numpy
output = open('new_coordinates_test.txt', 'w')
site = 0 #left site is okay. 
number_of_rows = 2
number_of_columns = 4
#test input
dictiolijst = {'0_2':[[9,8,3],[6,8,0],[8,2,1]],'0_1':[[0,4,5],[2,6,3],[1,1,1]], '1_1': [[0,4,5],[2,8,3],[1,1,1]], '1_0':[[9,8,3],[5,8,0],[6,2,1]],'0_3':[[10,8,3],[7,8,0],[8,2,1]],'0_0':[[0,4,5],[2,6,3],[1,1,1]]}
print dictiolijst
newdictio = {}
x = 0
total  = 0
gemiddeldetotaal = 0
for x in range(0,number_of_rows):
    for y in range(0,number_of_columns):
        varname = "%s_%s"%(x,y)
        #print varname
        d = dictiolijst.get(varname)
        try:
            for e in range(0,len(d)):
                total += d[e][0]
            gemiddelde  = total/(len(d))
            gemiddeldetotaal += gemiddelde
            newdictio[varname] = gemiddelde
            total = 0
        except:
            continue
        
print'newdictio',  newdictio
gemiddeldetotaal = gemiddeldetotaal  / 6
counter = 0
difference = 0
lijstje2 = []

#for calculating mean and stdev.
for x in range(0,number_of_rows):
    y = 0 
    while True:
        if y < (number_of_columns):
            varname1 = "%s_%s"%(x,y)
            varname2 = "%s_%s"%(x,y+1)
            d = newdictio.get(varname1)
            f = newdictio.get(varname2)
            try:
                lijstje2.append(abs(d-f))
                counter += 1
            except:
                y += 2
                continue
            y += 2
        else:
            break

print 'lijstje2', lijstje2
counter = 0
mean_percentage = numpy.mean(lijstje2) #gemiddelde van de verschillen tussen de vakjes
print mean_percentage, 'mean percentage'
std_percentage = numpy.std(lijstje2) # standard deviatie der van
print std_percentage, 'std'

left_range = mean_percentage - std_percentage #left range mean minus one standard deviation
right_range = mean_percentage + std_percentage
co = []

#for calculating if difference in range 
for x in range(0,number_of_rows):
    y = 0 
    while True:
        if y < number_of_columns:
            varname1 = "%s_%s"%(x,y)
            varname2 = "%s_%s"%(x,y+1)
            d = newdictio.get(varname1)
            f = newdictio.get(varname2)
            try:
                difference = abs(d-f)
                if (difference > right_range) or (difference < left_range):
                    if site == 0:
                        b = (dictiolijst.get(varname2))
                        for i in range (0, len(b)):
                            co.append(b[i])
                    elif site == 1:
                        co.append(dictiolijst.get(varname1))
                counter += 1
            except:
                y += 2
                continue
            y += 2
        else:
            break

#writing the newcoordinates with colorcode to ouputfile
for a in range(0,len(co)):
    co[a][0] = float(co[a][0] * -1)
    output.write('%s  %s  %s  0  0  0\n'%(co[a][0], co[a][1], co[a][2]))

C = []
sub = []
#calculating the nearest 2 points of point of interest
for b in range(0, len(co)):
    closestDist1 = 1000000000
    closestDist2 = 1000000000
    count= 0
    for c in range(0,len(co)):

        dist1 = sum(((co[b][0]- co[c][0])**2, (co[b][1]-co[c][1])**2, (co[b][2]-co[c][2])**2)) #klopt dit?
        dist2 = sum(((co[b][0]- co[c][0])**2, (co[b][1]-co[c][1])**2, (co[b][2]-co[c][2])**2)) #klopt dit?

        if count < 1: 
            first = (co[b])
            second = co[c]
            third = co[c]
            count = 1
        if closestDist1 > dist1 and dist1 != 0:
            if third == first:
                third = second
            second = co[c]

            closestDist1 = dist1
            
                
        elif closestDist2 > dist2 and dist2 != 0:
            third = co[c]
            closestDist2 = dist2

        else:
            continue

    sub.append(co[b])
    sub.append(second)
    sub.append(third)
    C.append(sub)
    sub = []
    
#writing points to outputfile
for z in range(0,len(C)):
    point1 = C[z][0]
    point2 = C[z][1]
    point3 = C[z][2]
    indexthing1 = co.index(C[z][0])
    indexthing2 = co.index(C[z][1])
    indexthing3 = co.index(C[z][2])
    output.write("3  %s  %s  %s\n"%(indexthing1, indexthing2, indexthing3))
output.close() 
#print 'coordinates 2', co        
#En nu per vakje de afwijking bekijken, is die binnen de perken, dan de coordinaten van de verkeerde opslaan in lijst

