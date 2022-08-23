#!/usr/bin/env python
# coding: utf-8

# # Answer3
# ## Number of cases district-wise

# In[19]:


import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None   # this line will hide SettingWithCopyWarning

neighbor_df=pd.read_csv('datasets/neighbor-df.csv')   # neighbor-df.csv was created in ques1


# ### Pre-processing of district.csv

# In[20]:




district_df=pd.read_csv("datasets/districts.csv")


'''There are many bad rows( rows having 'unKnown' and district names are absent from some rows. They contain values such as
'other state'). These rows will be removed'''
district_df['District']=district_df['District'].str.lower()
district_df=district_df[['Date','State','District','Confirmed']]
district_df=district_df.replace(to_replace=['unknown','capital complex','other state','other region','others'],value=np.nan)   #remove districts not in ques1 districts
district_df=district_df.dropna(how='any',axis=0)
district_df['Confirmed'][district_df['Confirmed']<0]=0


# drop rows after 2021-08-14
drop_row_beg=district_df[district_df.Date=='2021-08-15'].first_valid_index()  
drop_row_end=len(district_df)
district_df.drop(district_df.loc[drop_row_beg+1:].index, inplace=True)




# In[21]:


#dictionary to replace district names with disrict keys in district.csv
dist_code_for_q3=pd.read_csv('datasets/dcodeq3.csv')
dist_code_for_q3=dist_code_for_q3['B'].to_list()
dist_name_for_q3=pd.read_csv('datasets/dnameq3.csv')
dist_name_for_q3=dist_name_for_q3['A'].to_list()
for i in range(len(dist_name_for_q3)):
    dist_name_for_q3[i]=dist_name_for_q3[i].lower()
dict_for_q3=dict(zip(dist_name_for_q3,dist_code_for_q3))


# In[22]:


#correcting those districts which have same name but belong to different states. For ex, pratapgarh is present in UP as well as RJ
state_list_q3=district_df['State'].to_list()
dist_list_q3=district_df['District'].to_list()
for i in range(len(state_list_q3)):
    if state_list_q3[i].lower()=='uttar pradesh' and dist_list_q3[i].lower()=='pratapgarh':
        dist_list_q3[i]='UP_Pratapgarh'
    elif state_list_q3[i].lower()=='rajasthan' and dist_list_q3[i].lower()=='pratapgarh':
        dist_list_q3[i]='RJ_Pratapgarh'
    
    if state_list_q3[i].lower()=='bihar' and dist_list_q3[i].lower()=='aurangabad':
        dist_list_q3[i]='BR_Aurangabad'
    elif state_list_q3[i].lower()=='maharashtra' and dist_list_q3[i].lower()=='aurangabad':
        dist_list_q3[i]='MH_Aurangabad'
    
    if state_list_q3[i].lower()=='uttar pradesh' and dist_list_q3[i].lower()=='balrampur':
        dist_list_q3[i]='UP_Balrampur'
    elif state_list_q3[i].lower()=='chhattisgarh' and dist_list_q3[i].lower()=='balrampur':
        dist_list_q3[i]='CT_Balrampur'
        
    if state_list_q3[i].lower()=='chhattisgarh' and dist_list_q3[i].lower()=='bilaspur':
        dist_list_q3[i]='CT_Bilaspur'
    elif state_list_q3[i].lower()=='himachal pradesh' and dist_list_q3[i].lower()=='bilaspur':
        dist_list_q3[i]='HP_Bilaspur'
        
    if state_list_q3[i].lower()=='uttar pradesh' and dist_list_q3[i].lower()=='hamirpur':
        dist_list_q3[i]='UP_Hamirpur'
    elif state_list_q3[i].lower()=='himachal pradesh' and dist_list_q3[i].lower()=='hamirpur':
        dist_list_q3[i]='HP_Hamirpur'
        
    
        
district_df['District']=dist_list_q3


# In[23]:


for col in district_df:
    district_df=district_df.replace({col:dict_for_q3})      #dict_for_q3 is dictionary which maps district names with corresponding district_keys


# In[24]:


district_df.to_csv('datasets/district-df.csv',index=False)   # will be used in ques4


# In[25]:


#creating a dataframe of districts obtained in ques1 so that only these districts will be included in furthur calculations

q1_dist_list=neighbor_df.columns.to_list()
q1_dist_list=pd.DataFrame(q1_dist_list,columns=['District'])


# ### Calculation of week-wise cases

# In[26]:


dist_key_list=[]
week_list=[]
cases_list=[]
cumulative_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
counter=1
cases=0
week=1
n=len(district_df)
for i in range(n):
    
    if i==0:
        continue
    
    if district_df['Date'].iloc[i]==district_df['Date'].iloc[i-1]:
        continue
      
    counter=counter+1      #for keeping count of days 
    
    if counter==7:       #last day of week
        
        j=0
        while i+j<n-1:
            
            cases=district_df['Confirmed'].iloc[i+j]
            temp=cases
            cases=cases-cumulative_dict[district_df['District'].iloc[i+j]]
            dist_key_list.append(district_df['District'].iloc[i+j])
            week_list.append(week)
            cases_list.append(cases)
            cumulative_dict[district_df['District'].iloc[i+j]]=temp
            if district_df['Date'].iloc[i+j] != district_df['Date'].iloc[i+j+1]:
                break
            j=j+1
            
        
        counter=0
        week=week+1
        
    
        
    


# In[27]:


data={'District':dist_key_list,'week':week_list,'cases':cases_list}
weekly_data=pd.DataFrame(data)


# ## creation of list of district codes which will be used to match districts obtained in furthur questions with districts of question1

# In[28]:


q1_dist_list=pd.read_csv('datasets/q1-dist-list-df.csv')


# In[29]:


weekly_data['cases'][weekly_data['cases']<0]=np.nan
weekly_data=pd.merge(weekly_data,q1_dist_list)   # removing districts not obtained in ques1
weekly_data.dropna(how='any',axis=0,inplace=True)
weekly_data.to_csv('output files/cases-week.csv',index=False)


# ### Calculation of month wise cases

# In[30]:



dist_list_q3m=[]
month_list_q3m=[]
cases_list_q3m=[]
month=1
curr_cases_m=0
last_value_q3m_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))

i=0
n_m=len(district_df)   #n for month
while i<n_m:
    if '14' not in district_df['Date'].iloc[i]:
        i=i+1
        continue
        
    else:
        j=0
        
        while i+j<n_m:
            curr_cases_m=district_df['Confirmed'].iloc[i+j]
            temp=curr_cases_m
            curr_cases_m=curr_cases_m - last_value_q3m_dict[district_df['District'].iloc[i+j]]
            
            dist_list_q3m.append(district_df['District'].iloc[i+j])
            cases_list_q3m.append(curr_cases_m)
            month_list_q3m.append(month)
            
            last_value_q3m_dict[district_df['District'].iloc[i+j]]=temp
            
            if '14' not in district_df['Date'].iloc[i+j+1]:
                
                i=i+j
                break
                
            j=j+1
            
        month=month+1
            
    i=i+1 


# In[31]:


data_month={'District':dist_list_q3m,'month':month_list_q3m,'cases':cases_list_q3m}
monthly_data=pd.DataFrame(data_month)


# In[32]:


monthly_data['cases'][monthly_data['cases']<0]=np.nan
monthly_data=pd.merge(monthly_data,q1_dist_list)
monthly_data.dropna(how='any',axis=0,inplace=True)

monthly_data.to_csv('output files/cases-month.csv',index=False)


# ### Calculation of overall cases

# In[33]:


overall_cases_df=district_df[district_df['Date']=='2021-08-14']
overall_cases_df=overall_cases_df.rename(columns={'Confirmed':'cases'})
temp_list=[1]*len(overall_cases_df)
overall_cases_df=overall_cases_df.assign(overall=temp_list)
overall_cases_df.drop(columns={'Date','State'},axis=1)
overall_cases_df=overall_cases_df[['District','overall','cases']]
#overall_cases_df


# In[34]:


#writing overall file
pd.options.mode.chained_assignment = None   # this line will hide SettingWithCopyWarning
overall_cases_df['cases'][overall_cases_df['cases']<0]=np.nan
overall_cases_df.dropna(how='any',axis=0,inplace=True)
overall_cases_df=pd.merge(overall_cases_df,q1_dist_list)
overall_cases_df.to_csv('output files/cases-overall.csv',index=False)


# In[ ]:




