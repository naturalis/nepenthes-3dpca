reading_file1 = read.csv(file='Upper_pitcher_big_output.csv',header=FALSE) #read csv file
reading_file2 = read.csv(file = 'Upper_pitcher_medium_output.csv', header = FALSE)
reading_file3 = read.csv(file = 'Output Raf lower.csv', header = FALSE)
#co2 = rbind(reading_file,reading_file2,reading_file3)

k = 2
co3 = reading_file1
while(k < 4){
  name =  paste('reading_file',k,sep="")
  co3 = rbind(co3, name[1])
  k = k+1
}
co3

