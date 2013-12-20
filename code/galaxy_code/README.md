nepenthes-3dpca
===============

Pipeline for performing principal component analysis of 3D scans of Nepenthes pitchers


Tools
-----
/code/galaxy_code


Converter_dta_to_csv:
* Convert one .dta file to a .csv file 

Converter_multiple_dta_to_csv2:
* convert multiple .dta files to one merged .csv file

Procustes:
* Procustes fitting to scale rotate and translate the objects. Use procrustes first for PCA.

PCA:
* Execute a principle component analyses on procrustes coordinates.

Plottool:
* Makes a plot with principle components on the axis. 

plotPCACsize:
* Makes a plot with a principle component and the centroid size of the object

barplot:
* Makes a barplot with variance 


Galaxy
------

Install galaxy  (http://galaxyproject.org/)
Put the tools (the .xml and .R or .py)  in the directory galaxy-dist/tools 
Make Galaxy aware of the new tool in the tool_conf.xml file


Python 2.7
----------
Install python 2.7 to use the tools (http://www.python.org/)

R
-
Install R to use the tools (http://www.r-project.org/)
Install also the package 'geomorph' (http://cran.r-project.org/web/packages/geomorph/)






