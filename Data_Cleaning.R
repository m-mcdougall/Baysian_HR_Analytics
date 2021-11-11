#------------
fileIn = 'Train.csv'

#Read training data
data = read.csv(paste(getwd(),'/Data/',fileIn, sep=''), header = TRUE, sep=',', na.strings=c("","NA"), stringsAsFactors = FALSE)

#-----------

#Check all columns for nan values
sapply(data, function(x) sum(is.na(x)))

#Drop all nan - Removes too many rows (more than half)
data2 = na.omit(data)

#-------


data3 = data.frame(data)

data3 = replace(data3,is.na(data3),'Unknown')
data3$gender = replace(data3$gender,is.na(data3$gender),'Who')


#data3$gender = replace(data3$gender,is.na(data3$gender),'Unknown')
