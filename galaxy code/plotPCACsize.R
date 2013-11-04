args <- commandArgs(TRUE)
input_PCA <- args[1]
input_Csize <- args[2]
main_title <- args[3]
x_title <- args[4]
y_title <- args[5]
x_column <- args[6]
names <- args [7]
output <- args[8]

suppressMessages(library("geomorph"))

read <- read.csv(file <- input_PCA, header = TRUE)
read2 <- read.csv(file <- input_Csize, header = TRUE)
read3 <- scan(file <- names, what = "", quiet = TRUE)
pca1 <- read[,as.integer(x_column)]
pca2 <- read[,2]
read2 <- read2[,1]
minpca1 = min(pca1) - max(pca1)
maxpca1 = max(pca1) + max(pca1)

png(output)

suppressMessages(plot(pca1,read2, main = main_title, xlab = x_title, ylab = y_title, pch=20,cex=0.6))
text(pca1,read2,labels = read3, pos = 3, cex = 0.6, col = 'red')

graphics.off()
