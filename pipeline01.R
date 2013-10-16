#Pipeline Mirna
#making PCA plot
#reading files 
reading_file6 = read.csv(file = 'output_curved_lower.csv', header = FALSE)
reading_file7 = read.csv(file = 'output_elongation_lower.csv', header = FALSE)
reading_file8 = read.csv(file = 'output_h15_upper_pitcher.csv', header = FALSE)
reading_file9 = read.csv(file = 'output_inflation_phase_lower.csv', header = FALSE)
reading_file10 = read.csv(file = 'output_just_curved_lower.csv', header = FALSE)
reading_file11 = read.csv(file = 'output_late_elongation_lower.csv', header = FALSE)
reading_file12 = read.csv(file = 'output_mature_lower_2.csv', header = FALSE)

#names for labels
names = c('curved_lower','elongation_lower','h15_upper_pitcher', 'inflation_phase_lower', 'just_curved_lower',
          'late_elongation_lower','mature_lower_2') 
#make 1 array
co = rbind(reading_file6,reading_file7,reading_file8,reading_file9,reading_file10,reading_file11,reading_file12)

#transform array to use in statistical analyses
new_array = arrayspecs(co,18,3)

#procrustes fit
output_procrustes = gpagen(A=new_array, ShowPlot= FALSE)

#output procrustes fit 
coords2d = two.d.array((output_procrustes$coords))
# turn around the array
coords2d = t(coords2d)
#perform a pca with covariance matrix
pca = princomp(x=cov(coords2d))
# variance  
pov = pca$sdev^2/sum(pca$sdev^2)
barplot(pov)

#scores for pca1 and pca2 for each species
pca1 = pca$scores[,1]
pca2 = pca$scores[,2]

#plot the pca scores 
plot(pca1,pca2, xlim = c(-0.002, 0.005), ylim = c(-0.0005,0.0007), pch=20,cex=0.5)
#add labels
textxy(pca1, pca2,names, cx = 0.5)
