# create new coordinates, middle of faces
name_file = raw_input("file ")
file1 = open(name_file)
listje = []
listtotal_vertex = []
listtotal_face_sq = []
listtotal_face_tr = []
var_col = 0
outfile = open('outfile.ply', 'w')

# reading header, extract number of faces, en number of vertex
for x in range(0, 20):
    readheader = file1.readline().strip().split()
    if readheader[0] == 'end_header':
        var_header = x
    if 'red' in readheader:
        var_col += 1
    if 'blue' in readheader:
        var_col += 1
    if 'green' in readheader:
        var_col += 1
    if readheader[0] == "element" and readheader[1] == "vertex":
        var_vertex_ln = readheader[1]
        var_vertex_nm = readheader[2]

    if readheader[0] == "element" and readheader[1] == "face":
        var_face_ln = readheader[1]
        var_face_nm = readheader[2]
                
print 'end header task'
file1.close()

file1 = open(name_file)
# find coordinates for each face
for a in range(0, (int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):

    line = file1.readline().strip().split()
    if int(var_header) < a < (int(var_vertex_nm)+ int(var_header)+1):
        rayx = listje.append(line[0])
        rayy = listje.append(line[1])
        rayz = listje.append(line[2])
        listtotal_vertex.append(listje)
        listje = []
    if (int(var_vertex_nm)+ int(var_header)) < a < (int(var_vertex_nm) + int(var_header) + int(var_face_nm)+1):
        if int(line[0]) ==  4:
            listje.append(line[1])
            listje.append(line[2])
            listje.append(line[3])
            listje.append(line[4])
            listtotal_face_sq.append(listje)
            
            listje = []
        if int(line[0]) == 3:
            listje.append(line[1])
            listje.append(line[2])
            listje.append(line[3])
            listtotal_face_tr.append(listje)
            listje = []

#squares calculating
for b in range(0, len(listtotal_face_sq)):
    number1 = int(listtotal_face_sq[b][0])
    number2 = int(listtotal_face_sq[b][1])
    number3 = int(listtotal_face_sq[b][2])
    number4 = int(listtotal_face_sq[b][3])

    square1 = listtotal_vertex[number1]
    square2 = listtotal_vertex[number2]
    square3 = listtotal_vertex[number3]
    square4 = listtotal_vertex[number4]

    p1 = (float(square1[0]) + float(square2[0]) + float(square3[0]) + float(square4[0]))/4
    p2 = (float(square1[1]) + float(square2[1]) + float(square3[1]) + float(square4[1]))/4
    p3 = (float(square1[2]) + float(square2[2]) + float(square3[2]) + float(square4[2]))/4
    
    outfile.write("%s %s %s\n"%(p1,p2,p3))

newpoint = []
newpointtotal = []


# triangles calculating
for c in range(0, len(listtotal_face_tr)):
    number1 = int(listtotal_face_tr[c][0])
    number2 = int(listtotal_face_tr[c][1])
    number3 = int(listtotal_face_tr[c][2])
    triangle1 = listtotal_vertex[number1]
    triangle2 = listtotal_vertex[number2]
    triangle3 = listtotal_vertex[number3]
    
    p1 = (float(triangle1[0]) + float(triangle2[0]) + float(triangle3[0]))/3
    p2 = (float(triangle1[1]) + float(triangle2[1]) + float(triangle3[1]))/3
    p3 = (float(triangle1[2]) + float(triangle2[2]) + float(triangle3[2]))/3
    outfile.write("%s %s %s\n"%(p1,p2,p3))

outfile.close()

#writing new ply file with new points
file1.close()
outfile2 = open("outfile2.ply", 'w')
pointsfile = open('outfile.ply', 'r')
file2= open(name_file)
for d in range(0,(int(var_header) + int(var_vertex_nm) + int(var_face_nm) + 1)):
    line2 = file2.readline()
    readline2 = line2.strip().split()
    if readline2[0] == "element" and readline2[1] == "vertex":
        outfile2.write("element vertex %s\n"%(int(var_vertex_nm) + int(var_face_nm)))
    elif (int(var_header) + int(var_vertex_nm)) == d:
        outfile2.write(line2)
        for x in range(0, int(var_face_nm)+1):
            line3 = pointsfile.readline()
            outfile2.write(line3)
    else:
        outfile2.write(line2)

        
outfile2.close()
