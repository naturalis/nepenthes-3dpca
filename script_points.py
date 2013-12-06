import os

# getest op simpel 1 bij 1 bij 1 vierkant blok
os.system("rm col2.txt col3.txt col1.txt col4.txt A.txt")

os.system("nl < blok.ply > testline.ply")
# de faces getallen met 4 er voor
os.system("cat testline.ply |awk '{if((NF + 1) == 7 && $2 == 4)print$3, $4, $5, $6}' > squaretest.txt")
# de coordinaten in de orginele file met lijnnummers
os.system("cat testline.ply | awk '{if((NF + 1) == 8)print$1, $2, $3, $4}'> coordinates.txt")

os.system("wc -l < squaretest.txt > numberlines.txt") 
file1 = open('squaretest.txt')
file2 = open('numberlines.txt')

readnumberline = file2.readline()
print readnumberline

listje = []
listje2 = []
listje3 = []
listje4 = []
# alle punten voor face
for x in range(0,int(readnumberline)):
    readregel = file1.readline().strip().split()
    listje.append(readregel[0])
    listje2.append(readregel[1])
    listje3.append(readregel[2])
    listje4.append(readregel[3])

# coordinaten van elke punt in face
for a in range(0,len(listje)):
    os.system("cat coordinates.txt | awk '{if (($1) == (%s+12))print $2,$3,$4}' >> col1.txt"%(listje[a]))
    os.system("cat coordinates.txt | awk '{if (($1) == (%s+12))print $2,$3,$4}' >> col2.txt"%(listje2[a]))
    os.system("cat coordinates.txt | awk '{if (($1) == (%s+12))print $2,$3,$4}' >> col3.txt"%(listje3[a]))
    os.system("cat coordinates.txt | awk '{if (($1) == (%s+12))print $2,$3,$4}' >> col4.txt"%(listje4[a]))
    os.system("pr -m -t col1.txt col2.txt col3.txt col4.txt > copoint.txt")

# x2-x1 y2-y1 z2-z1
os.system("cat copoint.txt | awk '{print($4-$1, $7-$4, $10-$7, $1-$10, $7-$1, $10-$4)}'> A.txt")
os.system("cat copoint.txt | awk '{print($5-$2, $8-$5, $11-$8, $2-$11, $8-$2, $11-$5)}'> B.txt")
os.system("cat copoint.txt | awk '{print($6-$3, $9-$6, $12-$9, $3-$12, $9-$3, $12-$6)}'> C.txt")
# A, B, C en COL1, COL2, COl3, COL4
os.system("pr -m -t -J A.txt B.txt C.txt col1.txt col2.txt col3.txt col4.txt>total.txt")

# new point coordinates
os.system("cat total.txt | awk '{print($19 + (0.5*$1), $20 + (0.5*$7), $21 + (0.5*$13))}' > newpoints1_2.txt")
os.system("cat total.txt | awk '{print($22 + (0.5*$2), $23 + (0.5*$8), $24 + (0.5*$14))}' > newpoints2_3.txt")
os.system("cat total.txt | awk '{print($25 + (0.5*$3), $26 + (0.5*$9), $27 + (0.5*$15))}' > newpoints3_4.txt")
os.system("cat total.txt | awk '{print($28 + (0.5*$4), $29 + (0.5*$10), $30 + (0.5*$16))}' > newpoints4_1.txt")
os.system("cat total.txt | awk '{print($19 + (0.5*$5), $20 + (0.5*$11), $21 + (0.5*$17))}' > newpoints1_3.txt")
os.system("cat total.txt | awk '{print($22 + (0.5*$6), $23 + (0.5*$12), $24 + (0.5*$18))}' > newpoints2_4.txt")

# alle nieuwe punten
os.system("cat newpoints1_2.txt newpoints2_3.txt newpoints3_4.txt newpoints4_1.txt newpoints1_3.txt newpoints2_4.txt > newpoint_temp.txt") 
# de nieuwe unieke punten
os.system("sort newpoint_temp.txt | uniq > newpoints.txt")  



