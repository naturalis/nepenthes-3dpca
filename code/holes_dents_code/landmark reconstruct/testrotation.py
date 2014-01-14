#rotation 

import math
from math import *
#file_name = raw_input("file: ")
file_name = 'dart_landmark.dta'
#file_connect = raw_input("file: ")
file_connect= 'mirror2.txt'

#maken dat die connect file onthoud. 
import sys
file_outputname = 'outputrotate.dta'
file_outputname2 = 'outputrotate2.dta'
file_outputname3 = 'outputrotate3.dta'
file_outputname4 = 'outputrotate4.dta'
output = open(file_outputname, 'w')
output2 = open(file_outputname2, 'w')
output3 = open(file_outputname3, 'w')
output4 = open(file_outputname4, 'w') 

datapoints = open(file_name)
datalines = datapoints.readlines()
#print datalines
listdata = []
listdta = []
sublistje = []

# open dta file
for a  in range(0,len(datalines)):
    aline = datalines[a].strip()

    listdta.append(datalines[a].strip().split(' ')) # let op spatie
    #print listdta
    #print len(listdta[a])
    if len(listdta[a]) == 3:
        sublistje.append(float(listdta[a][0]))
        sublistje.append(float(listdta[a][1]))
        sublistje.append(float(listdta[a][2]))
        listdata.append(sublistje)
        sublistje = []
    else:
        output.write("%s\n"%(aline))
print listdata

# open mirrorpoints file
mirrorpoints = open(file_connect)
lines= mirrorpoints.readlines()

listje = []
listjesym = []
for x in range(0, len(lines)):
    line = lines[x].strip()
    if line == 'sym':
        for a in range(1,4):
            listjesym.append(lines[a].strip().split())
    if line == 'mirror':
        for y in range(x + 1,len(lines)):
            listje.append(lines[y].strip().split())
#print listjesym





#shift to zeropoint ##########################################################

zeropoint = int(listjesym[2][0])

co_zeropoint = listdata[zeropoint -1]

listdata2 = []
listdata3 = []
# minus x,y,z of point shift to zeropoint of every point
for x in range(0,len(listdata)):
    listdata2.append(listdata[x][0] - co_zeropoint[0])
    listdata2.append(listdata[x][1] - co_zeropoint[1])
    listdata2.append(listdata[x][2] - co_zeropoint[2])
    listdata3.append(listdata2)
    listdata2 = []

print 'listdata3', listdata3

for x in range(0,len(listdata)):
    output.write("%s %s %s\n"%(listdata3[x][0], listdata3[x][1], listdata3[x][2]))
output.close()

# Rotate around z axis ########################################################################


def R2(angle): # Rz rotation matrix
    return [[cos(math.radians(angle)), -sin(math.radians(angle)), 0.0],[sin(math.radians(angle)),cos(math.radians(angle)),0.0],[0.0, 0.0, 1.0]]

def Rotate2(point2, angle2): # multiplication rotation matrix and coordinates 
    r_2 = R2(angle)
    #print 'm', r_2
    rotated2 = []
    '''for points in range(0,):#len(listdata3)
        print points
        for i in range(0,3):
            ax = r_2[i][0] * listdata3[points][0]
            by = r_2[i][1] * listdata3[points][1]
            cz = r_2[i][2] * listdata3[points][2]
            #print 'ax',ax
            #print 'by', by
            #print 'cz',cz
            totalx = ax + by + cz
            #print 'total', totalx
            #print '\n
            '''
               
    for i in range(3):
        rotated2.append((sum([r_2[i][j] * point2[j] for j in range(3)])))
    return rotated2

# calculate angle rotation
len_a = abs(listdata3[0][0] - listdata3[4][0])
len_b = abs(listdata3[0][1] - listdata3[4][1])

angle = -(math.degrees(math.atan(len_a/len_b)))
print angle

# calculate new coordinates
listdata5 = []

for d in range(0, len(listdata3)):
    #print 'r', Rotate2(listdata3[d], angle)
    listdata5.append(Rotate2(listdata3[d], angle))
print 'list5', listdata5

for x in range(0,len(listdata)):
    output2.write("%s %s %s\n"%(listdata5[x][0], listdata5[x][1], listdata5[x][2]))

output2.close()

# around x-axis #######################################################

def R3(angle3): #rotation matrix x-axis
    return [[1, 0, 0],[0,cos(math.radians(angle3)),-sin(math.radians(angle3))],[0,sin(math.radians(angle3)),cos(math.radians(angle3))]]

def Rotate3(point3, angle3): #multiplication rotation matrix and coordinates 
    r_3 = R3(angle3)
    rotated3 = []
    for i in range(3):
        rotated3.append((sum([r_3[i][j] * point3[j] for j in range(3)])))
        #round weggehaald
    return rotated3

#calculate angle
len_a3 = listdata5[0][2] - listdata5[4][0]
len_b3 = listdata5[0][1] - listdata5[4][0]
angle3 = -(math.degrees(math.atan(len_a3/len_b3)))
print angle
listdata7 = []

# new coordinates in list
for d in range(0, len(listdata3)):
    print 's', Rotate3(listdata5[d], angle3)
    listdata7.append(Rotate3(listdata5[d], angle3))

print 'listdata7', listdata7
# write new coordinates
for x in range(0,len(listdata)):
    output4.write("%s %s %s\n"%(listdata7[x][0], listdata7[x][1], listdata7[x][2]))


###############################################################
    
'''
marge = 300 ####### hoe zouden we hier een getal voor kunnen nemen?
# change the wrong points
for x in range(0,len(listje)):
    left = listje[x][0]
    right = listje[x][1]
    co_left = listdata[int(left)-1]
    co_right = listdata[int(right)-1]
    distance_x = float(co_left[0]) + float(co_right[0])
    #print 'distance', distance_x

    if distance_x > marge:
        if site == 0:
            listdata[int(right)-1][0] = float(co_left[0]) * -1
            listdata[int(right)-1][1] = float(co_left[1])
            listdata[int(right)-1][2] = float(co_left[2])
        if site == 1:
            listdata[int(left)-1][0] = float(co_right[0]) * -1
            listdata[int(left)-1][1] = float(co_right[1])
            listdata[int(left)-1][2] = float(co_right[2])
            
for x in range(0,len(listdata)):
    output.write("%s %s %s\n"%(listdata7[x][0], listdata7[x][1], listdata7[x][2]))

#print listdata
#print len(listdata)
output.close()
output2.close()
output3.close()
output4.close()
datapoints.close()
mirrorpoints.close()


def R(theta, u):
    return [[cos(theta) + u[0]**2 * (1-cos(theta)), 
             u[0] * u[1] * (1-cos(theta)) - u[2] * sin(theta), 
             u[0] * u[2] * (1 - cos(theta)) + u[1] * sin(theta)],
            [u[0] * u[1] * (1-cos(theta)) - u[2] * sin(theta),
             cos(theta) + u[1]**2 * (1-cos(theta)),
             u[1] * u[2] * (1 - cos(theta)) + u[0] * sin(theta)],
            [u[0] * u[2] * (1-cos(theta)) - u[1] * sin(theta),
             u[1] * u[2] * (1-cos(theta)) - u[0] * sin(theta),
             cos(theta) + u[2]**2 * (1-cos(theta))]]

def Rotate(pointToRotate, point1, point2, theta):


    u= []
    squaredSum = 0
    for i,f in zip(point1, point2):
        u.append(f-i)
        print u
        squaredSum += (f-i) **2
        print squaredSum
    u = [i/squaredSum for i in u]#????
    print u
    r = R(theta, u)
    rotated = []

    for i in range(3):
        print 'j', (sum([r[j][i] for j in range(3)]))
        rotated.append(round(sum([r[j][i] * pointToRotate[j] for j in range(3)])))
        print rotated

    return rotated


point = [1,0,0]
p1 = [0,0,0]
p2 = [0,1,0]


print Rotate(point, p1, p2, pi) # [-1.0, 0.0, 0.0]

##########################################
def R(theta, u):
    return [[cos(theta) + u[0]**2 * (1-cos(theta)), 
             u[0] * u[1] * (1-cos(theta)) - u[2] * sin(theta), 
             u[0] * u[2] * (1 - cos(theta)) + u[1] * sin(theta)],
            [u[0] * u[1] * (1-cos(theta)) - u[2] * sin(theta),
             cos(theta) + u[1]**2 * (1-cos(theta)),
             u[1] * u[2] * (1 - cos(theta)) + u[0] * sin(theta)],
            [u[0] * u[2] * (1-cos(theta)) - u[1] * sin(theta),
             u[1] * u[2] * (1-cos(theta)) - u[0] * sin(theta),
             cos(theta) + u[2]**2 * (1-cos(theta))]]

def Rotate(pointToRotate, point1, point2, theta):
    u= []
    squaredSum = 0
    for i,f in zip(point1, point2):
        u.append(f-i)
        #print u
        squaredSum += (f-i) **2
        #print squaredSum
    u = [i/squaredSum for i in u]#????
    #print u
    r = R(theta, u)
    #print r
    rotated = []

    for i in range(3):
        #print 'j', (sum([r[j][i] for j in range(3)]))
        rotated.append((sum([r[j][i] * pointToRotate[j] for j in range(3)])))
        #round weggehaald

    return rotated

p1 = [0,0,0]
p2 = [0,10,0]
print p1, p2
listdata6 = []
len_a = abs(listdata3[0][0] - listdata3[4][0])
print len_a


len_b = abs(listdata3[0][1] - listdata3[4][1])
print len_b
angle = math.degrees(math.atan(len_a/len_b))
print 'angle', angle
angle = math.radians(angle)
print 'angle', angle

#angle = 0.045
#print angle
for c in range(0, len(listdata3)):
    print 'iets'
    #if (c + 1) == 15 or (c+1) == 13:
        #listdata4.append((listdata3[c]))
        #continue
    print 'oke'
    print Rotate(listdata3[c], p1, p2, angle) # [-1.0, 0.0, 0.0]
    listdata6.append(Rotate(listdata3[c], p1, p2, angle))
print 'listdata6', listdata6
print len(listdata6)

for x in range(0,len(listdata)):
    output3.write("%s %s %s\n"%(listdata6[x][0], listdata6[x][1], listdata6[x][2]))
##########################################################################
'''
