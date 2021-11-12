# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np

path = os.path.abspath(r'C:\Users\Mariko\Documents\GitHub\Baysian_HR_Analytics')
#%%

#Load the training and testing data
training_raw = pd.read_csv(path+'/Data/Train.csv')
testing_raw = pd.read_csv(path+'/Data/Test.csv')

#%%

training = training_raw.copy()
testing = testing_raw.copy()

#Categorical columns
unknown_cols = ['gender','relevent_experience', 'enrolled_university', 'education_level',
                'major_discipline','company_type']

for col in unknown_cols:
    training[col] = training[col].fillna('Unknown')
    testing[col] = testing[col].fillna('Unknown')
    

#Numeric columns
numeric_cols = ['experience', 'company_size','last_new_job', 'training_hours']

for col in numeric_cols:
    training[col] = training[col].fillna(9999)
    testing[col] = testing[col].fillna(9999)
    
#%%


for col in training.columns:
    print('\n\n------',col,'-------')
    print(training[col].unique())    
    
    
    
