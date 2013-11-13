#Plottool makes a graph of Principle Components created with a Principle Component analysis. 
#developer: Mirna Baak

#commands extracting of commandline
args <- commandArgs(TRUE)

#input files and options
input <- args[1]
main_title <- args[2]
x_title <- args[3]
y_title <- args[4]
x_column <- args[5]
y_column <- args[6]
names <- args [7] #name of every sample in one file
#output file
output <- args[8]

suppressMessages(library("geomorph")) #package geomorph

#reading of input files
read <- read.csv(file <- input,header = TRUE)
read2 <- scan(file <- names, what = "", quiet = TRUE)

pca1 <- read[,as.integer(x_column)] #principle component
pca2 <- read[,as.integer(y_column)] #principle component

png(output) #output in png format

#axis boundaries
minpca1 = min(pca1) - max(pca1)
maxpca1 = max(pca1) + max(pca1)
minpca2 = min(pca2) - max(pca2)
maxpca2 = max(pca2) + max(pca2)

#creating the plot with principle components and titels
suppressMessages(plot(pca1,pca2, main = main_title, xlab = x_title, ylab = y_title, pch=20,cex=0.6, xlim = c(minpca1,maxpca1), ylim=c(minpca2,maxpca2)))
#add labels to data points
text(pca1,pca2,labels = read2, pos = 2, cex = 0.6,col = heat.colors(5)) 

graphics.off()
