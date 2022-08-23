#!/usr/bin/env python
# coding: utf-8

# # Answer9

# ## The date on which the entire population will get at least one dose of vaccination

# In[10]:


import pandas as pd
pd.options.mode.chained_assignment = None   # this line will hide SettingWithCopyWarning


vaccine_df=pd.read_csv('datasets/vaccine-df.csv')   #from vaccine-df.csv I have already removed districts not obtained as result in question1
rate_df=vaccine_df[['District_Key','07/08/2021.3','07/08/2021.4','14/08/2021.3','14/08/2021.4']]
#'07/08/2021.3' is the column name of dose1 on 7th aug 2021
#'07/08/2021.4' is the column name of dose2 on 7th aug 2021
#'14/08/2021.3' is the column name of dose1 on 14th aug2021
#'14/08/2021.4' is the column name of dose2 on 14th aug 2021

#before calculating the rates, I should group-by the districts into their states
rate_df['District_Key'].replace(to_replace='_.*',value='',regex=True,inplace=True)  #removing the district names and keeping only state codes
rate_df=rate_df.groupby('District_Key').sum()
rate_df.to_csv('datasets/rate-df.csv')   
'''since groupby is applied the indexing has been changed. Also, because of groupby, rows of those columns which were
not included in groupby cannot be retrieved. After saving csv file and then loading back will allow those operations
to be done as usually on the dataframe'''
rate_df=pd.read_csv('datasets/rate-df.csv')

rate_df.rename(columns={'District_Key':'State'},inplace=True)


# ###  NOTE: To find the  date on which the entire population will get "atleast one dose" of vaccination, we should find the rate of vaccination and total population left to be vaccinated by considering only dose1 and not dose2. This is because: 
# ### Let A denote number of people vaccinated with dose1 and B denote number of people vaccinated with dose2. Let N(A) denote number of people in set A. Then N(atleast one dose)=N(A union B)=N(A)+N(B)-N(AandB)=N(A)+N(B)-N(B)=N(A) {because N(AnadB) means people vaccinated with both doses is same as people vaccinated with dose2...because dose2 cannot be completed before dose1}

# In[11]:


'''So I am going to count only dose1 for rate calculation for the time when every person will get vacicnated with
"atleast one dose" '''
rate_df['rateofvaccination']=(rate_df['14/08/2021.3'] - rate_df['07/08/2021.3'] )/7
state_wise_pop_df=pd.read_csv('datasets/state-wise-tot-pop-df.csv')
state_wise_pop_df.rename(columns={'District':'State'},inplace=True)
complete_df=pd.merge(rate_df,state_wise_pop_df)
complete_df['populationleft']=complete_df['TOT_P']-complete_df['14/08/2021.3']
complete_df=complete_df[['State','populationleft','rateofvaccination']]
#note that in rate_df I have removed those states for which any of the files given to be used had an entry named 'Unknown'


'''The populationleft and rateofvaccination entries are according to the date 14/08/2021'''
complete_df['more_days_required']=(complete_df['populationleft']/complete_df['rateofvaccination'] +1)  # i have added 1 because of round-off error while dividing.Also, adding 1 more day is better for prediction

#converting days required to integer
complete_df['more_days_required']=complete_df['more_days_required'].astype(int)



#converting more_days_required to exact date on which everyone will get atleast one dose
import datetime

date_1 = datetime.datetime.strptime("14-08-2021", "%d-%m-%Y")
for i in range(len(complete_df)):
    temp=complete_df['more_days_required'].iloc[i]
    put_date=date_1 + datetime.timedelta(days=int(temp))
    complete_df['more_days_required'].iloc[i]=put_date
    
complete_df.rename(columns={'more_days_required':'date'},inplace=True)
complete_df['date'].replace(to_replace=' 00:00:00',value='',regex=True,inplace=True)


# ### Note that in  complete-vaccination.csv file, some values are negative because I have used population data of 2011 and population has increased since then

# In[12]:


#writing complete-vaccination.csv file
complete_df.to_csv('output files/complete-vaccination.csv',index=False)

