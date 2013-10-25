
args <- commandArgs(TRUE)
input <- args[1]
nb_landmarks <- args[2]
nb_species <- args[3]
main_title <- args[4]
output <- args[5]

suppressMessages(library("geomorph"))#new

read <- read.csv(file <- input,header = FALSE)
outp <- t(read)
#print(csvTables)
new_array  <- arrayspecs(read,as.integer(nb_landmarks),as.integer(nb_species)) #new
output_procrustes <- gpagen(A=new_array, ShowPlot= FALSE)
coords2d <- two.d.array((output_procrustes$coords))
coords2d <- t(coords2d)

pca <- princomp(x=cov(coords2d))


pov <- pca$sdev^2/sum(pca$sdev^2)
pca1 <- pca$scores[,1]
pca2 <- pca$scores[,2]

#plot the pca scores 
png(output)
#write.table(pca1,output)
suppressMessages(plot(pca1,pca2, pch=20,cex=1))
title(main = main_title) #gaat iets nog niet goed, als ik losse woorden typ
#suppressMessages(dev.copy(png, output))
graphics.off()





