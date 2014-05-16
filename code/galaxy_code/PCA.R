# The tool PCA creates a Principal Component Analysis on Procrustes coordinates.
# MB

#commands of commandline
args <- commandArgs(TRUE)
#input file: procrustes coordinates
input <- args[1]
#output file
output <- args[2]
output2 <- args[3]

#package geomorph
suppressMessages(library("geomorph"))

#reading of coordinates
read <- read.csv(file <- input,header = TRUE)
#principal component analysis with princomp, using covariance matrix of coordinates
pca <- princomp(x=cov(read))

#output pca scores
write.csv(pca$scores,output, row.names = FALSE)
write.csv(pca$sdev, output2, row.names = FALSE)
