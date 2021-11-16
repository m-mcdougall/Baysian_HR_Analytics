# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

path = os.path.abspath(r'C:\Users\Mariko\Documents\GitHub\Baysian_HR_Analytics')
#%%

#Load the training and testing data
training_raw = pd.read_csv(path+'/Data/Train.csv')
testing_raw = pd.read_csv(path+'/Data/Test.csv')

#%%

training = training_raw.copy()
testing = testing_raw.copy()

#Set up training/testing
training.name='Training'
testing.name='Testing'

processing = [training, testing]


for dataset in processing:
    #Categorical columns
    unknown_cols = ['gender','relevent_experience', 'enrolled_university', 'education_level',
                    'major_discipline','company_type']    
    for col in unknown_cols:
        dataset[col] = dataset[col].fillna('Unknown')
        
    
    #Numeric columns
    numeric_cols = ['experience', 'company_size','last_new_job', 'training_hours', 
                    'city_development_index']
    for col in numeric_cols:
        dataset[col] = dataset[col].fillna(9999)
        
    
#%%

#Print all categories present in each column
for col in testing.columns:
    print('\n\n------',col,'-------')
    for dataset in processing:
        print(dataset.name, "\n--------------\n",dataset[col].unique(),'\n')    
    
    
    
#%%
"""
Priority Columns:
city_development_index, experience, company_size, company_type, last_new_job 

city_development_index : Done!
experience : clean nan, strings, bins
company_size : clean nan, strings, bins
company_type : merge startups, clean nan , can you do continous with MCMC
last_new_job : clean nan, strings, bins


Non-Priority Columns:
relevent_experience, education_level

relevent_experience : make binary
education_level : merge lower education, clean nan , can you do continous with MCMC
"""

#%%




#Drop Unneeded columns
#--------------------------------------
for dataset in processing:
    dataset.drop(['enrollee_id', 'city','gender', 'enrolled_university',
                  'major_discipline','training_hours'],
                 axis=1, inplace=True)




#city_development_index : Done!
#--------------------------------------


#experience : clean nan, strings, bins
#--------------------------------------

col = 'experience'
print('\n\n------',col,'-------')

for dataset in processing:
    dataset[col].replace('>20', '21', inplace=True)
    dataset[col].replace('<1', '0', inplace=True)
    dataset[col] = pd.to_numeric(dataset[col])

    print('NaN', dataset.name,':', (dataset[col] == 9999).sum())




#company_size : clean nan, strings, bins
#--------------------------------------
# Small:  0-100
# Medium: 101-1000
# Large:  1000+

col = 'company_size'
print('\n\n------',col,'-------')

binning = {9999:'Unknown', '50-99':'Small', '<10':'Small', '10000+':'Large', '5000-9999':'Large', 
           '1000-4999':'Large', '10/49':'Small', '100-500':"Medium", '500-999':"Medium"}

for dataset in processing: 
    dataset[col].replace(binning, inplace=True)
    print('NaN', dataset.name,':', (dataset[col] == 'Unknown').sum())






#company_type : merge startups, clean nan , can you do continous with 
#--------------------------------------

col = 'company_type'
print('\n\n------',col,'-------')


binning = {'Funded Startup':'Startup',  'Early Stage Startup':'Startup'}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)  
    print('NaN', dataset.name,':', (dataset[col] == 'Unknown').sum())






#last_new_job : clean nan, strings, bins
#--------------------------------------

col = 'last_new_job'
print('\n\n------',col,'-------')


binning = {'never':'0', '>4':'5'}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)
    dataset[col] = pd.to_numeric(dataset[col])
    print('NaN', dataset.name,':', (dataset[col] == 9999).sum())





#relevent_experience : make binary
#--------------------------------------
col = 'relevent_experience'
print('\n\n------',col,'-------')


binning = {'Has relevent experience':1, 'No relevent experience':0}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)
    print('NaN', dataset.name,':', (dataset[col] == 'Unknown').sum())
    
    
    

#education_level : merge lower education, clean nan , can you do continous with MCMC
#--------------------------------------

col = 'education_level'
print('\n\n------',col,'-------')


binning = {'Graduate':'Bachelors','High School':'PublicEducation','Primary School':'PublicEducation'}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)
    print('NaN', dataset.name,':', (dataset[col] == 'Unknown').sum())






#%%

#Print a demo plot of all processed columns
for col in dataset.columns:
    print('\n\n------',col,'-------')
    dataset[col][dataset[col]!=9999].hist()
    plt.title(col)
    plt.ylabel('Count')
    plt.show()
    


#%%

# Export the Cleaned Data (no Nan replce)
for dataset in processing:
    file=dataset.name+'_cleaned.csv'
    dataset.to_csv(file)









