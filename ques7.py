#!/usr/bin/env python
# coding: utf-8

# # Answer7

# ## Here, for each state, district and overall, we are going to find the following ratios: total number of Cov-ishield vaccinated persons (either 1 or 2 doses) to total number of Covaxin vaccinated persons
# 

# ### District wise

# In[1]:


import pandas as pd
pd.options.mode.chained_assignment = None   # this line will hide SettingWithCopyWarning


'''Here I will use vaccine dataframe vaccine_df which I have already prepared and processed. Originally, Many of its
numeric fields were of obect type but later I had modified them to numeric data type'''
#loading vaccine_df
vaccine_df=pd.read_csv('datasets/vaccine-df.csv')

#loading q1-district-list dataframe which will be used to remove districts not obtained in question1
q1_dist_list=pd.read_csv('datasets/q1-dist-list-df.csv')
dist_covi_cova_ratio_df=vaccine_df[['District_Key','14/08/2021.9','14/08/2021.8']]
dist_covi_cova_ratio_df['ratio(covishield/covaxin)']=dist_covi_cova_ratio_df['14/08/2021.9']/dist_covi_cova_ratio_df['14/08/2021.8']
dist_covi_cova_ratio_df=dist_covi_cova_ratio_df[['District_Key','ratio(covishield/covaxin)']]
dist_covi_cova_ratio_df.rename(columns={'District_Key':'District'}, inplace=True)
dist_covi_cova_ratio_df=pd.merge(dist_covi_cova_ratio_df,q1_dist_list)
dist_covi_cova_ratio_df.replace(to_replace=float('inf'),value=0,inplace=True)  # I am replacing inf (obtained due to division by zero) with zero
dist_covi_cova_ratio_df.to_csv('output files/district-vaccine-type-ratio.csv',index=False)


# ### State wise

# In[2]:


state_covi_cova_ratio_df=vaccine_df[['District_Key','14/08/2021.9','14/08/2021.8']]
state_covi_cova_ratio_df.replace(to_replace='_.*', value='',regex=True, inplace=True)
state_covi_cova_ratio_df=state_covi_cova_ratio_df.groupby('District_Key').sum() # groupby is applied so we need to save and load again
state_covi_cova_ratio_df.to_csv('datasets/state-covi-cova-ratio-df.csv')
state_covi_cova_ratio_df=pd.read_csv('datasets/state-covi-cova-ratio-df.csv')
state_covi_cova_ratio_df['ratio(covishield/covaxin)']=state_covi_cova_ratio_df['14/08/2021.9']/state_covi_cova_ratio_df['14/08/2021.8']
state_covi_cova_ratio_df=state_covi_cova_ratio_df[['District_Key','ratio(covishield/covaxin)']]
state_covi_cova_ratio_df.rename(columns={'District_Key':'State'})
state_covi_cova_ratio_df.replace(to_replace=float('inf'),value=0,inplace=True) # replacing inf with 0
state_covi_cova_ratio_df.to_csv('output files/state-vaccine-type-ratio.csv',index=False)


# ### Overall

# In[3]:


overall_covi_cova_ratio_df=vaccine_df[['District_Key','14/08/2021.9','14/08/2021.8']]
overall_covi_cova_ratio_df.replace(to_replace='^.*', value='India',regex=True, inplace=True)
overall_covi_cova_ratio_df=overall_covi_cova_ratio_df.groupby('District_Key').sum()
overall_covi_cova_ratio_df.to_csv('datasets/overall-covi-cova-ratio-df.csv')
overall_covi_cova_ratio_df=pd.read_csv('datasets/overall-covi-cova-ratio-df.csv')
overall_covi_cova_ratio_df['ratio(covishield/covaxin)']=overall_covi_cova_ratio_df['14/08/2021.9']/overall_covi_cova_ratio_df['14/08/2021.8']
overall_covi_cova_ratio_df=overall_covi_cova_ratio_df[['District_Key','ratio(covishield/covaxin)']]
overall_covi_cova_ratio_df.rename(columns={'District_Key':'overall'})
overall_covi_cova_ratio_df.replace(to_replace=float('inf'),value=0,inplace=True) # replacing inf with 0
overall_covi_cova_ratio_df.to_csv('output files/overall-vaccine-type-ratio.csv',index=False)


# # 
