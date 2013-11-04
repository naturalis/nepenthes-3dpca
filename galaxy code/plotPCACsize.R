#The plotPCACsize tool creates a plot with a principle component and the centroid size created with procrustes analysis
#developer: Mirna Baak
#commandline arguments
args <- commandArgs(TRUE)

#inputs
input_PCA <- args[1]
input_Csize <- args[2]
main_title <- args[3]
x_title <- args[4]
y_title <- args[5]
x_column <- args[6]
names <- args [7] #sample names in one file
output <- args[8]

#library geomorph
suppressMessages(library("geomorph"))
#reading of the input files
read <- read.csv(file <- input_PCA, header = TRUE) #principle components
read2 <- read.csv(file <- input_Csize, header = TRUE) #centroid size
read3 <- scan(file <- names, what = "", quiet = TRUE)
pca1 <- read[,as.integer(x_column)] #principle component
read2 <- read2[,1] #centroid size

#output
png(output)

#creating plot with pca and centroid size
suppressMessages(plot(pca1,read2, main = main_title, xlab = x_title, ylab = y_title, pch=20,cex=0.6))
#adding labels to datapoints
text(pca1,read2,labels = read3, pos = 3, cex = 0.6, col = 'red') 

graphics.off()
