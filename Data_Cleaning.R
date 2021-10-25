#------------
fileIn = 'Train.csv'

#Read training data
data = read.table(paste(getwd(),'/Data/',fileIn, sep=''), header = TRUE, sep=',')

#-----------