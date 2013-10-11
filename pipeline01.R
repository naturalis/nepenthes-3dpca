reading_file = read.csv(file='Upper_pitcher_big_output.csv',header=FALSE) #read csv file
header = tail(reading_file, n = 1L) #Header
name_sample = (header[1]) #name sample
number_landmarks = header[,2] # number of landmarks
coordinates = head(reading_file, n = number_landmarks) #coordinates
coordinates = as.matrix(coordinates)
