#Plottool makes a graph barplot of the variance
#MB

#commands extracting of commandline
args <- commandArgs(TRUE)

#input files and options
input <- args[1]
title <- args[2]
#output file
output <- args[3]

#reading of input files
read <- read.csv(file <- input,header = TRUE)

stdev<- read[,1] #standard deviation
pov = stdev^2/sum(stdev^2) #variance

png(output) #output in png format


#creating the barplot with the variance of pca 
suppressMessages(barplot(pov, main = title, names.arg = c(1:NROW(pov)), ylim = c(0,1), col = heat.colors(3)))


graphics.off()
