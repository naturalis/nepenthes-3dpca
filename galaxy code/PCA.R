# The tool PCA creates a principle component analysis on procrustes data.
# developer: Mirna Baak

#commands of commandline
args <- commandArgs(TRUE)
#input file: procrustes coordinates
input <- args[1]
#output file
output <- args[2]

#package geomorph
suppressMessages(library("geomorph"))

#reading of coordinates
read <- read.csv(file <- input,header = TRUE)
#principle componten analysis with princomp, using covariance matrix of coordinates
pca <- princomp(x=cov(read))

#output pca scores
write.csv(pca$scores,output, row.names = FALSE)

