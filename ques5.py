#!/usr/bin/env python
# coding: utf-8

# # Answer5

# ## District wise calculation

# ### weeks

# In[15]:


import pandas as pd

q1_dist_list=pd.read_csv('datasets/q1-dist-list-df.csv')
vaccine_df=pd.read_csv('datasets/cowin_vaccine_data_districtwise.csv',low_memory=False)
q1_dist_list.rename(columns={'District':'District_Key'},inplace=True)  
vaccine_df=pd.merge(vaccine_df,q1_dist_list)       # removing all districts not in ques1 district list
patternDel = "^DL_"
filter = vaccine_df['District_Key'].str.contains(patternDel)
vaccine_df=vaccine_df[~filter]
vaccine_df.loc[:, '16/01/2021':] = vaccine_df.loc[:, '16/01/2021':].apply(pd.to_numeric)
vaccine_df.to_csv('datasets/vaccine-df.csv')


# In[2]:


#dictionary to replace district names with disrict keys in district.csv
dist_code_for_q3=pd.read_csv('datasets/dcodeq3.csv')
dist_code_for_q3=dist_code_for_q3['B'].to_list()
dist_name_for_q3=pd.read_csv('datasets/dnameq3.csv')
dist_name_for_q3=dist_name_for_q3['A'].to_list()
for i in range(len(dist_name_for_q3)):
    dist_name_for_q3[i]=dist_name_for_q3[i].lower()
dict_for_q3=dict(zip(dist_name_for_q3,dist_code_for_q3))


'''creating a dictionary for storing number of doses of previous week. The value in this dictionary will be subtracted to get
current week data'''
dist_key_list=[]
week_list=[]
dose1_list=[]
dose2_list=[]
cumulative_dose1_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
cumulative_dose2_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
counter=1
dose1=0
dose2=0



n=len(vaccine_df)
for i in range(n):
    week=1
    col_len=len(vaccine_df.columns)
    k=69         #69th column is 23/01/2021.3 which contains first dose administered' data
    while k<col_len:
        dose1=vaccine_df.iloc[:, [k]].iloc[i].iloc[0]
        dose2=vaccine_df.iloc[:, [k+1]].iloc[i].iloc[0]
        temp1=dose1
        temp2=dose2
        dose1=dose1-cumulative_dose1_dict[vaccine_df['District_Key'].iloc[i]]
        dose2=dose2-cumulative_dose2_dict[vaccine_df['District_Key'].iloc[i]]
        dist_key_list.append(vaccine_df['District_Key'].iloc[i])
        week_list.append(week)
        dose1_list.append(dose1)
        dose2_list.append(dose2)
        cumulative_dose1_dict[vaccine_df['District_Key'].iloc[i]]=temp1
        cumulative_dose2_dict[vaccine_df['District_Key'].iloc[i]]=temp2
        week=week+1
        #now increment k so as to reach on 'first dose administered' column of 7 days later
        k=k+1
        k=k+69
        
    


# In[3]:


data={'District_Key':dist_key_list,'week':week_list,'dose1':dose1_list,'dose2':dose2_list}
vaccinated_count_week_df=pd.DataFrame(data)

# we have to count only upto 14/08/2021. So, removing weeks after this date
vaccinated_count_week_df.drop(vaccinated_count_week_df[vaccinated_count_week_df['week'] >32].index, inplace = True)


# In[4]:


#removing districts not obtained as result of question 1
vaccinated_count_week_df=pd.merge(vaccinated_count_week_df,q1_dist_list)
vaccinated_count_week_df.to_csv('output files/district-vaccinated-count-week.csv',index=False)


# ### months

# In[5]:


dist_key_list=[]
month_list=[]
dose1_list=[]
dose2_list=[]
cumulative_dose1_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
cumulative_dose2_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))

dose1=0
dose2=0

n=len(vaccine_df)
for i in range(n):
    month=1
    col_len=len(vaccine_df.columns)
    
    for col in vaccine_df:
        if '14' in col and '.3' in col:   #basically I am finding columns of form 14(.*).3$. For ex 14/02/2021.3  such columns contain dose1 data
            dose1=vaccine_df[col].iloc[i]
            dose2=vaccine_df.iloc[:,vaccine_df.columns.get_indexer([col])+1].iloc[i].iloc[0] # the column next to dose1 data is of dose2 data
            temp1=dose1
            temp2=dose2
            dose1=dose1-cumulative_dose1_dict[vaccine_df['District_Key'].iloc[i]]
            dose2=dose2-cumulative_dose2_dict[vaccine_df['District_Key'].iloc[i]]
            dist_key_list.append(vaccine_df['District_Key'].iloc[i])
            month_list.append(month)
            dose1_list.append(dose1)
            dose2_list.append(dose2)
            cumulative_dose1_dict[vaccine_df['District_Key'].iloc[i]]=temp1
            cumulative_dose2_dict[vaccine_df['District_Key'].iloc[i]]=temp2
            month=month+1
        
        
    
data={'District_Key':dist_key_list,'month':month_list,'dose1':dose1_list,'dose2':dose2_list}
vaccinated_count_month_df=pd.DataFrame(data)
vaccinated_count_month_df.drop(vaccinated_count_month_df[vaccinated_count_month_df['month'] >7].index, inplace = True)


#removing districts not obtained as result of question 1
vaccinated_count_month_df=pd.merge(vaccinated_count_month_df,q1_dist_list)  
vaccinated_count_month_df.to_csv('output files/district-vaccinated-count-month.csv',index=False)


# ### overall

# In[7]:


pd.options.mode.chained_assignment = None   # this line will hide SettingWithCopyWarning
vaccinated_count_overall_df=vaccine_df[['District_Key','14/08/2021.3','14/08/2021.4']]
vaccinated_count_overall_df.rename(columns={'14/08/2021.3':'dose1','14/08/2021.4':'dose2'},inplace=True) #in cowin dataset, the column '14/08/2021.3' stores dose1 data
vaccinated_count_overall_df['overall']=pd.DataFrame([1]*len(vaccinated_count_overall_df))
vaccinated_count_overall_df=vaccinated_count_overall_df[['District_Key','overall','dose1','dose2']]
vaccinated_count_overall_df=pd.merge(vaccinated_count_overall_df,q1_dist_list)
vaccinated_count_overall_df.to_csv('output files/district-vaccinated-count-overall.csv',index=False)


# ## State wise calculation

# ### weeks

# In[8]:


state_vacc_count_week_df=pd.read_csv('output files/district-vaccinated-count-week.csv')
state_vacc_count_week_df['District_Key'].replace(to_replace='_.*$',value='',regex=True,inplace=True) #removing district name and keeping only stateid
state_vacc_count_week_df=state_vacc_count_week_df.groupby(['District_Key','week']).sum()
state_vacc_count_week_df.to_csv('datasets/state-vacc-count-week-temp-df.csv')   # saving and reloading csv because groupby operation is applied
state_vacc_count_week_df=pd.read_csv('datasets/state-vacc-count-week-temp-df.csv')
state_vacc_count_week_df.rename(columns={'District_Key':'State'},inplace=True)
state_vacc_count_week_df.to_csv('output files/state-vaccinated-count-week.csv',index=False)


# ### months

# In[9]:


state_vacc_count_month_df=pd.read_csv('output files/district-vaccinated-count-month.csv')
state_vacc_count_month_df['District_Key'].replace(to_replace='_.*$',value='',regex=True,inplace=True) #removing district name and keeping only stateid
state_vacc_count_month_df=state_vacc_count_month_df.groupby(['District_Key','month']).sum()
state_vacc_count_month_df.to_csv('datasets/state-vacc-count-month-temp-df.csv')   # saving and reloading csv because groupby operation is applied
state_vacc_count_month_df=pd.read_csv('datasets/state-vacc-count-month-temp-df.csv')
state_vacc_count_month_df.rename(columns={'District_Key':'State'},inplace=True)
state_vacc_count_month_df.to_csv('output files/state-vaccinated-count-month.csv',index=False)


# ### overall

# In[10]:


state_vacc_count_overall_df=pd.read_csv('output files/district-vaccinated-count-overall.csv')
state_vacc_count_overall_df['District_Key'].replace(to_replace='_.*$',value='',regex=True,inplace=True) #removing district name and keeping only stateid
state_vacc_count_overall_df=state_vacc_count_overall_df.groupby(['District_Key','overall']).sum()
state_vacc_count_overall_df.to_csv('datasets/state-vacc-count-overall-temp-df.csv')   # saving and reloading csv because groupby operation is applied
state_vacc_count_overall_df=pd.read_csv('datasets/state-vacc-count-overall-temp-df.csv')
state_vacc_count_overall_df.rename(columns={'District_Key':'State'},inplace=True)
state_vacc_count_overall_df.to_csv('output files/state-vaccinated-count-overall.csv',index=False)


# #  

# ## Overall (country) wise calculation

# ### weeks

# In[11]:


overall_vacc_count_week_df=pd.read_csv('output files/state-vaccinated-count-week.csv')
overall_vacc_count_week_df['State'].replace(to_replace='^.*',value='India',regex=True,inplace=True)
overall_vacc_count_week_df=overall_vacc_count_week_df.groupby(['State','week']).sum()
overall_vacc_count_week_df.to_csv('datasets/overall-vacc-count-week-temp-df.csv')   # saving and reloading csv because groupby operation is applied
overall_vacc_count_week_df=pd.read_csv('datasets/overall-vacc-count-week-temp-df.csv')
overall_vacc_count_week_df.rename(columns={'State':'overall'},inplace=True)
overall_vacc_count_week_df.to_csv('output files/overall-vaccinated-count-week.csv',index=False)


# ### months

# In[12]:


overall_vacc_count_month_df=pd.read_csv('output files/state-vaccinated-count-month.csv')
overall_vacc_count_month_df['State'].replace(to_replace='^.*',value='India',regex=True,inplace=True)
overall_vacc_count_month_df=overall_vacc_count_month_df.groupby(['State','month']).sum()
overall_vacc_count_month_df.to_csv('datasets/overall-vacc-count-month-temp-df.csv')   # saving and reloading csv because groupby operation is applied
overall_vacc_count_month_df=pd.read_csv('datasets/overall-vacc-count-month-temp-df.csv')
overall_vacc_count_month_df.rename(columns={'State':'overall'},inplace=True)
overall_vacc_count_month_df.to_csv('output files/overall-vaccinated-count-month.csv',index=False)


# ### overall

# In[13]:


overall_vacc_count_overall_df=pd.read_csv('output files/state-vaccinated-count-overall.csv')
overall_vacc_count_overall_df['State'].replace(to_replace='^.*',value='India',regex=True,inplace=True)
overall_vacc_count_overall_df=overall_vacc_count_overall_df.groupby(['State','overall']).sum()
overall_vacc_count_overall_df.to_csv('datasets/overall-vacc-count-overall-temp-df.csv')   # saving and reloading csv because groupby operation is applied
overall_vacc_count_overall_df=pd.read_csv('datasets/overall-vacc-count-overall-temp-df.csv')
overall_vacc_count_overall_df.rename(columns={'State':'overall'},inplace=True)
overall_vacc_count_overall_df.to_csv('output files/overall-vaccinated-count-overall.csv',index=False)


# #  
