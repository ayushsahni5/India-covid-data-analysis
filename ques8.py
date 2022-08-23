#!/usr/bin/env python
# coding: utf-8

# # Answer8

# ## Here, for each state, district and overall, we will find the following ratio: total number of persons vaccinated (both 1 and 2 doses) to total population

# ## District wise

# In[3]:


import pandas as pd

#loading district-wise-total-population data frame which was created in ques6
dist_wise_tot_pop_df=pd.read_csv('datasets/district-wise-total-population-df.csv')

#loading district-wise-dose1-dose2 dataframe created in ques 5
dist_wise_tot_vaccinated=pd.read_csv('output files/district-vaccinated-count-overall.csv')


#taking only district column and total vaccinated column
dist_wise_tot_vaccinated=dist_wise_tot_vaccinated[['District_Key','dose1','dose2']]

#merging district wise total vaccinated dataframe and district wise total population to get district wise total population along with total vaccinated people
dist_wise_tot_vaccinated.rename(columns={'District_Key':'District'},inplace=True) # one dataframe has column District and other has District_Key. Before merging they need to be same.
dist_vaccinated_dose_ratio=pd.merge(dist_wise_tot_vaccinated,dist_wise_tot_pop_df)
dist_vaccinated_dose_ratio['vaccinateddose1ratio']=dist_vaccinated_dose_ratio['dose1']/dist_vaccinated_dose_ratio['TOT_P']
dist_vaccinated_dose_ratio['vaccinateddose2ratio']=dist_vaccinated_dose_ratio['dose2']/dist_vaccinated_dose_ratio['TOT_P']
dist_vaccinated_dose_ratio=dist_vaccinated_dose_ratio[['District','vaccinateddose1ratio','vaccinateddose2ratio']]
dist_vaccinated_dose_ratio.sort_values('vaccinateddose1ratio',inplace=True)
dist_vaccinated_dose_ratio.to_csv('output files/district-vaccinated-dose-ratio.csv',index=False)


# ## State wise

# In[4]:


#loading district-wise-total-population data frame which was created in ques6
state_wise_tot_pop_df=pd.read_csv('datasets/district-wise-total-population-df.csv')
state_wise_tot_pop_df['District'].replace(to_replace='_.*',value='',regex=True,inplace=True)
state_wise_tot_pop_df=state_wise_tot_pop_df[['District','TOT_P']]
state_wise_tot_pop_df=state_wise_tot_pop_df.groupby(['District']).sum()

state_wise_tot_pop_df.to_csv('datasets/state-wise-tot-pop-df.csv')  #groupby has been applied so saving and loading csv file
state_wise_tot_pop_df.to_csv('datasets/state-wise-tot-pop-df.csv')
state_wise_tot_pop_df=pd.read_csv('datasets/state-wise-tot-pop-df.csv')

#loading district-wise-dose1-dose2 dataframe created in ques 5
state_wise_tot_vaccinated=pd.read_csv('output files/state-vaccinated-count-overall.csv')


#taking only district column and total vaccinated column
state_wise_tot_vaccinated=state_wise_tot_vaccinated[['State','dose1','dose2']]

#merging district wise total vaccinated dataframe and district wise total population to get district wise total population along with total vaccinated people
state_wise_tot_pop_df.rename(columns={'District':'State'},inplace=True) # one dataframe has column District and other has District_Key. Before merging they need to be same.
state_vaccinated_dose_ratio=pd.merge(state_wise_tot_vaccinated,state_wise_tot_pop_df)
state_vaccinated_dose_ratio['vaccinateddose1ratio']=state_vaccinated_dose_ratio['dose1']/state_vaccinated_dose_ratio['TOT_P']
state_vaccinated_dose_ratio['vaccinateddose2ratio']=state_vaccinated_dose_ratio['dose2']/state_vaccinated_dose_ratio['TOT_P']
state_vaccinated_dose_ratio=state_vaccinated_dose_ratio[['State','vaccinateddose1ratio','vaccinateddose2ratio']]
state_vaccinated_dose_ratio.sort_values('vaccinateddose1ratio',inplace=True)
state_vaccinated_dose_ratio.to_csv('output files/state-vaccinated-dose-ratio.csv',index=False)


# ## overall

# In[5]:


#loading overall dose1 dose2 vaccinated dataframe created in ques5
overall_tot_vaccinated_df=pd.read_csv('output files/overall-vaccinated-count-overall.csv')
overall_tot_vaccinated_df
#loading overall population of india
'''The overall population can be directly seen from cencus 2011 data. It is 1210854977. So to find the required ratio
I will simply divide by this number'''

#calculation
overall_tot_vaccinated_df['vaccinateddose1ratio']=overall_tot_vaccinated_df['dose1']/1210854977
overall_tot_vaccinated_df['vaccinateddose2ratio']=overall_tot_vaccinated_df['dose2']/1210854977

overall_tot_vaccinated_df=overall_tot_vaccinated_df[['overall','vaccinateddose1ratio','vaccinateddose2ratio']]
overall_tot_vaccinated_df.to_csv('output files/overall-vaccinated-dose-ratio.csv',index=False)

