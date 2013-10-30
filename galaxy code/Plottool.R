args <- commandArgs(TRUE)
input <- args[1]
main_title <- args[2]
x_title <- args[3]
y_title <- args[4]
names <- args [5]
output <- args[6]

suppressMessages(library("geomorph"))

read <- read.csv(file <- input,header = TRUE)
read2 <- scan(file <- names, what = "", quiet = TRUE)
pca1 <- read[,1]
pca2 <- read[,2] 

png(output)

suppressMessages(plot(pca1,pca2, main = main_title, xlab = x_title, ylab = y_title, pch=20,cex=0.6))
text(pca1,pca2,labels = read2, pos = 3, cex = 0.6, col = 'red')
#title(main = main_title, xlab = x_title, ylab = y_title) #gaat iets nog niet goed, als ik losse woorden typ
#suppressMessages(dev.copy(png, output))
graphics.off()
