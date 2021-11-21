# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

#Imputer
from sklearn.impute import SimpleImputer


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

    print('NaN', dataset.name,':', (dataset[col].isna()).sum())



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
    print('NaN', dataset.name,':', (dataset[col].isna()).sum())






#company_type : merge startups, clean nan , can you do continous with 
#--------------------------------------

col = 'company_type'
print('\n\n------',col,'-------')


binning = {'Funded Startup':'Startup',  'Early Stage Startup':'Startup'}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)  
    print('NaN', dataset.name,':', (dataset[col].isna()).sum())






#last_new_job : clean nan, strings, bins
#--------------------------------------

col = 'last_new_job'
print('\n\n------',col,'-------')


binning = {'never':'0', '>4':'5'}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)
    dataset[col] = pd.to_numeric(dataset[col])
    print('NaN', dataset.name,':', (dataset[col].isna()).sum())





#relevent_experience : make binary
#--------------------------------------
col = 'relevent_experience'
print('\n\n------',col,'-------')


binning = {'Has relevent experience':1, 'No relevent experience':0}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)
    print('NaN', dataset.name,':', (dataset[col].isna()).sum())
    
    
    

#education_level : merge lower education, clean nan , can you do continous with MCMC
#--------------------------------------

col = 'education_level'
print('\n\n------',col,'-------')


binning = {'Graduate':'Bachelors','High School':'PublicEducation','Primary School':'PublicEducation'}


for dataset in processing:
    dataset[col].replace(binning, inplace=True)
    print('NaN', dataset.name,':', (dataset[col].isna()).sum())






#%%

#Print a demo plot of all processed columns
for col in dataset.columns:
    print('\n\n------',col,'-------')
    dataset[col].hist()
    plt.title(col)
    plt.ylabel('Count')
    plt.show()
    


#%%

# Export the Cleaned Data (no Nan replce)
for dataset in processing:
    file=path+'\\Data\\'+dataset.name+'_cleaned.csv'
    dataset.to_csv(file)



#%%

#Impute Variables


#Impute Training Set
train_imput = processing[0].iloc[:,0:-1]

imp_mean = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

train_imput_out = imp_mean.fit_transform(train_imput)
train_imput_out = pd.DataFrame(train_imput_out, columns = train_imput.columns)
train_imput_out['target'] = processing[0].iloc[:,-1]


#Impute Testing Set

test_imput = processing[1]

imp_mean = SimpleImputer(missing_values=np.nan, strategy='most_frequent')

test_imput_out = imp_mean.fit_transform(test_imput)
test_imput_out = pd.DataFrame(test_imput_out, columns = test_imput.columns)



# Export the Cleaned Data (with simple impute)
train_imput_out.to_csv(path+'\\Data\\'+'Training_cleaned_impute.csv')
test_imput_out.to_csv(path+'\\Data\\'+'Testing_cleaned_impute.csv')

#%%

# OHE Categorical Variables

def ohe_vars(df_in):
        
    #Create base OHE
    company_types_ohe = pd.get_dummies(df_in.company_type, prefix = 'Company_Type')
    education_ohe = pd.get_dummies(df_in.education_level, prefix = 'Education_Higest')
    education_total_ohe = pd.get_dummies(df_in.education_level, prefix = 'Education_Total')
    
  
    
    #For the Total Education, Add binary for all education levels 
    #below the highest level achieved
    
    all_rows =[]
    
    for i in range(education_ohe.shape[0]):
        row = education_total_ohe.iloc[i,:]
        
        highest = row[row==1].index[0]
        if highest == 'Education_Total_PublicEducation':
            pass
        
        elif highest == 'Education_Total_Bachelors':
            row.Education_Total_PublicEducation = 1
            
        elif highest == 'Education_Total_Masters':
            row.Education_Total_PublicEducation = 1
            row.Education_Total_Bachelors = 1
            
        elif highest == 'Education_Total_Phd':
            row.Education_Total_PublicEducation = 1
            row.Education_Total_Bachelors = 1
            row.Education_Total_Masters = 1
    
        all_rows.append(row)
    
    #Combine all processed rows
    education_total_ohe = pd.DataFrame(all_rows)
    
    #Combine OHE frames
    combo = company_types_ohe.join([education_ohe, education_total_ohe])
    return combo

#%%

#Create OHE

train_ohe = ohe_vars(train_imput_out)
train_ohe_out = train_imput_out.join(train_ohe)

test_ohe = ohe_vars(test_imput_out)
test_ohe_out = test_imput_out.join(test_ohe)

# Export the Cleaned Data (with OHE)
train_ohe_out.to_csv(path+'\\Data\\'+'Training_cleaned_impute_OHE.csv')
test_ohe_out.to_csv(path+'\\Data\\'+'Testing_cleaned_impute_OHE.csv')


#%%


# Change colmns to represent people who work at company and do/don't want to leave


    


def binary_column_parser(df_in, col):
    
    #Seperate target and fileter column
    targ = df_in['target']    
    filt = df_in[col]
    
    #Only data where target is true
    filt = filt[filt == 1]
    
    #Get targ data for those rows
    targ_filt = targ.iloc[filt.index]
    
    #Replace
    filt = targ_filt.rename(col).reset_index(drop=True)
    
    return filt

filtered_columns = []



for col in ['Company_Type_NGO', 'Company_Type_Other', 'Company_Type_Public Sector',
            'Company_Type_Pvt Ltd', 'Company_Type_Startup',
            'Education_Higest_Bachelors', 'Education_Higest_Masters',
            'Education_Higest_Phd', 'Education_Higest_PublicEducation',
            'Education_Total_Bachelors', 'Education_Total_Masters',
            'Education_Total_Phd', 'Education_Total_PublicEducation']:

    filtered_columns.append(binary_column_parser(train_ohe_out, col))


#%%

for i in range(len(filtered_columns)):
    name_df = filtered_columns[i].name
    filtered_columns[i].to_csv(path+'\Data\Binary_target_'+name_df+'.csv')
    












