args <- commandArgs(TRUE)
input <- args[1]
main_title <- args[2]
x_title <- args[3]
y_title <- args[4]
x_column <- args[5]
y_column <- args[6]
names <- args [7]
output <- args[8]

suppressMessages(library("geomorph"))

read <- read.csv(file <- input,header = TRUE)
read2 <- scan(file <- names, what = "", quiet = TRUE)
pca1 <- read[,as.integer(x_column)]*-100
pca2 <- read[,as.integer(y_column)] *-100

png(output)
minpca1 = min(pca1) - max(pca1)
maxpca1 = max(pca1) + max(pca1)
minpca2 = min(pca2) - max(pca2)
maxpca2 = max(pca2) + max(pca2)
suppressMessages(plot(pca1,pca2, main = main_title, xlab = x_title, ylab = y_title, pch=20,cex=0.6, xlim = c(minpca1,maxpca1), ylim=c(minpca2,maxpca2)))
text(pca1,pca2,labels = read2, pos = 3, cex = 0.6, col = 'red')
#title(main = main_title, xlab = x_title, ylab = y_title) #gaat iets nog niet goed, als ik losse woorden typ
#suppressMessages(dev.copy(png, output))
graphics.off()
