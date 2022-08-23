#!/usr/bin/env python
# coding: utf-8

# # Answer6

# In[1]:


import pandas as pd
pd.options.mode.chained_assignment = None   # this line will hide SettingWithCopyWarning

population_df=pd.read_excel('datasets/india-census-2011.xlsx')
population_df=population_df[['State','Level','Name','TRU','TOT_P','TOT_M','TOT_F']]
#changing the name of districts having same name but in different states. 
population_df.loc[(population_df.Name=='Aurangabad') & (population_df.State==10),'Name']='BR_Aurangabad'
population_df.loc[(population_df.Name=='Aurangabad') & (population_df.State==27),'Name']='MH_Aurangabad'
population_df.loc[(population_df.Name=='Balrampur') & (population_df.State==27),'Name']='MH_Aurangabad'
population_df.loc[(population_df.Name=='Bilaspur'),'Name']='UP_Balrampur'
population_df.loc[(population_df.Name=='Bilaspur') & (population_df.State==22),'Name']='CT_Bilaspur'
population_df.loc[(population_df.Name=='Hamirpur') & (population_df.State==2),'Name']='HP_Hamirpur'
population_df.loc[(population_df.Name=='Hamirpur') & (population_df.State==9),'Name']='UP_Hamirpur'
population_df.loc[(population_df.Name=='Pratapgarh') & (population_df.State==8),'Name']='RJ_Pratapgarh'
population_df.loc[(population_df.Name=='Pratapgarh') & (population_df.State==9),'Name']='UP_Pratapgarh'


#census 2011 data has written leh as leh(ladakh). So i am changing leh(ladakh) to leh.
population_df.replace(to_replace='Leh\(Ladakh\)',value='leh',regex=True,inplace=True)

#dictionary to replace district names with disrict keys 
dist_codes=pd.read_csv('datasets/dcodeq3.csv')
dist_codes=dist_codes['B'].to_list()
dist_names=pd.read_csv('datasets/dnameq3.csv')
dist_names=dist_names['A'].to_list()
for i in range(len(dist_names)):
    dist_names[i]=dist_names[i].lower()
dist_key_dict=dict(zip(dist_names,dist_codes))


# ### district-wise

# In[2]:


q1_dist_list=pd.read_csv('datasets/q1-dist-list-df.csv')

#loading vaccine_df
'''Here I will use vaccine dataframe vaccine_df which I have already prepared and processed. Originally, Many of its
numeric fields were of obect type but later I had modified them to numeric data type'''
vaccine_df=pd.read_csv('datasets/vaccine-df.csv')



#calculation of vaccination ratio
vacc_pop_ratio_df=vaccine_df[['District_Key','14/08/2021.5','14/08/2021.6']]
vacc_pop_ratio_df['vaccinationratio']=vacc_pop_ratio_df['14/08/2021.6']/vacc_pop_ratio_df['14/08/2021.5']
vacc_pop_ratio_df=vacc_pop_ratio_df[['District_Key','vaccinationratio']]
#vacc_pop_ratio_df


# In[3]:


#calculation of population ratio
population_df['Name']=population_df['Name'].str.lower()
population_df.replace({'Name':dist_key_dict},inplace=True)


# In[4]:


import numpy as np

dist_pop_df=population_df[population_df['Level']=='DISTRICT']
dist_pop_df=dist_pop_df[dist_pop_df['TRU']=='Total']
dist_pop_df.rename(columns={'Name':'District'},inplace=True)
dist_pop_df=pd.merge(dist_pop_df,q1_dist_list)     #removing districts not in ques 1 district list
dist_pop_df['populationratio']=dist_pop_df['TOT_F']/dist_pop_df['TOT_M']
dist_pop_df.replace(to_replace=np.nan,value=0,inplace=True)   # replacing NaN obtained because of division by zero
dist_pop_df.to_csv('datasets/district-wise-total-population-df.csv',index=False)   # will be used in ques 8
dist_pop_df=dist_pop_df[['District','populationratio']]


# In[5]:


dist_pop_df.rename(columns={'District':'District_Key'},inplace=True)   # making column name same as of vacc_pop_ratio_df to perform merge
vacc_pop_ratio_df=pd.merge(vacc_pop_ratio_df,dist_pop_df)
vacc_pop_ratio_df['ratioofratios']=vacc_pop_ratio_df['vaccinationratio']/vacc_pop_ratio_df['populationratio'] 
vacc_pop_ratio_df.replace(to_replace=float('inf'),value=0,inplace=True)  #replacing inf obtained due to division by zero
vacc_pop_ratio_df=vacc_pop_ratio_df.sort_values('ratioofratios')
vacc_pop_ratio_df.to_csv('output files/district-vaccination-population-ratio.csv',index=False)


# ### state-wise

# In[6]:


#calculation of population ratio
state_pop_df=population_df[population_df['Level']=='STATE']
state_pop_df=state_pop_df[state_pop_df['TRU']=='Total']
state_pop_df.drop('State',axis=1,inplace=True)
state_pop_df.rename(columns={'Name':'State'},inplace=True)
state_pop_df['populationratio']=state_pop_df['TOT_F']/state_pop_df['TOT_M']
state_pop_df.replace(to_replace=np.nan,value=0,inplace=True)   # replacing NaN obtained because of opeartion between bad numbers
state_pop_df=state_pop_df[['State','populationratio']]
#state_pop_df


# In[7]:


#calculation of vaccination ratio
state_vacc_pop_df=vaccine_df[['State','14/08/2021.5','14/08/2021.6']]
state_vacc_pop_df=state_vacc_pop_df.groupby(['State']).sum()
state_vacc_pop_df.to_csv('datasets/state-vacc-pop-df.csv')
state_vacc_pop_df=pd.read_csv('datasets/state-vacc-pop-df.csv')
state_vacc_pop_df['vaccinationratio']=state_vacc_pop_df['14/08/2021.6']/state_vacc_pop_df['14/08/2021.5']
state_vacc_pop_df['State']=state_vacc_pop_df['State'].str.lower()
state_vacc_pop_df=pd.merge(state_vacc_pop_df,state_pop_df)
state_vacc_pop_df=state_vacc_pop_df[['State','vaccinationratio','populationratio']]
state_vacc_pop_df['ratioofratios']=state_vacc_pop_df['vaccinationratio']/state_vacc_pop_df['populationratio']
state_vacc_pop_df=state_vacc_pop_df.sort_values('ratioofratios')
state_vacc_pop_df.to_csv('output files/state-vaccination-population-ratio.csv',index=False)


# ### overall

# In[8]:


overall_pop_df=population_df.iloc[[0],[2,5,6]]
overall_pop_df['populationratio']=overall_pop_df['TOT_F']/overall_pop_df['TOT_M']
overall_pop_df.rename(columns={'Name':'overall'},inplace=True)
#overall_pop_df


# In[9]:

pd.options.mode.chained_assignment = None   # this line will hide SettingWithCopyWarning

overall_vacc_df=vaccine_df[['District_Key','14/08/2021.5','14/08/2021.6']]
overall_vacc_df['District_Key'].replace(to_replace='^.*',value='India',regex=True,inplace=True)
overall_vacc_df.rename(columns={'District_Key':'overall'},inplace=True)
overall_vacc_df=overall_vacc_df.groupby(['overall']).sum()
overall_vacc_df.to_csv('datasets/overall-vacc-pop-df.csv')
overall_vacc_df=pd.read_csv('datasets/overall-vacc-pop-df.csv')
overall_vacc_df['vaccinationratio']=overall_vacc_df['14/08/2021.6']/overall_vacc_df['14/08/2021.5']
overall_vacc_df['populationratio']=overall_pop_df['populationratio']
overall_vacc_df=overall_vacc_df[['overall','vaccinationratio','populationratio']]
overall_vacc_df.to_csv('output files/overall-vaccination-population-ratio.csv',index=False)


# In[ ]:




