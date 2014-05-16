nepenthes-3dpca
===============

Pipeline for performing Principal Component analysis of 3D scans of Nepenthes pitchers, 
correct Landmarks with ReMarker and reconstruct a 3D file with ReConstructor


Tools
-----
/code/galaxy_code


Converter:
* Convert .dta files to a .csv file 


Procustes:
* Procustes fitting to scale rotate and translate the objects. Use Procrustes first for PCA.

PCA:
* Execute a Principle Component analyses on Procrustes coordinates.

PCA plot:
* Makes a plot with principle components on the axis. 

Csize plot:
* Makes a plot with a principle component and the centroid size of the object

Variance plot:
* Makes a barplot with variance 

ReMarker: 
* Correct landmarks (.dta) based on the symmetry 

Convert ply:
* Convert ply to ply

Rotate:
* Rotate an object based on calibration points

ReConstructor:
* Reconstruct holes and dents in a 3D object (.ply) based on symmetry


Galaxy
------

Install galaxy  (http://galaxyproject.org/).
Put the tools (the .xml and .R or .py)  in the directory galaxy-dist/tools. 
Make Galaxy aware of the new tool in the tool_conf.xml file


Python 2.7
----------
Install python 2.7 to use the tools (http://www.python.org/)

Numpy
-----
Install numpy 1.6.1 to use the tools (http://www.scipy.org/scipylib/download.html)

R
-
Install R to use the tools (http://www.r-project.org/).
Install also the package 'geomorph' (http://cran.r-project.org/web/packages/geomorph/).






