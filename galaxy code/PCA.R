args <- commandArgs(TRUE)
input <- args[1]

output <- args[2]
#wil je er een plot bij?
suppressMessages(library("geomorph"))

read <- read.csv(file <- input,header = TRUE)

pca <- princomp(x=cov(read))

pov <- pca$sdev^2/sum(pca$sdev^2)
pca1 <- pca$scores[,1] *-1 *100
pca2 <- pca$scores[,2] *-1 *100

#png(output)

write.csv(pca$scores,output, row.names = FALSE)
#suppressMessages(plot(pca1,pca2, pch=20,cex=1))
#title(main = main_title) #gaat iets nog niet goed, als ik losse woorden typ
#suppressMessages(dev.copy(png, output))
#graphics.off()

