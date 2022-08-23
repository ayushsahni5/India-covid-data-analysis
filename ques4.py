#!/usr/bin/env python
# coding: utf-8

# # Answer4

# ## District-peaks.csv file

# ### Calculation of peak weeks

# In[65]:


import pandas as pd

#dictionary to replace district names with disrict keys in district.csv
dist_code_for_q3=pd.read_csv('datasets/dcodeq3.csv')
dist_code_for_q3=dist_code_for_q3['B'].to_list()
dist_name_for_q3=pd.read_csv('datasets/dnameq3.csv')
dist_name_for_q3=dist_name_for_q3['A'].to_list()
for i in range(len(dist_name_for_q3)):
    dist_name_for_q3[i]=dist_name_for_q3[i].lower()
dict_for_q3=dict(zip(dist_name_for_q3,dist_code_for_q3))



district_df=pd.read_csv('datasets/district-df.csv')   #district-df.csv was created in ques3

# week of thursday to wednesday
dist_keyq4_list=[]
weekq4_list=[]
casesq4_list=[]
cumulativeq4_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
counter_q4=1
cases_q4=0
week_q4=2
n1_q4=len(district_df)
i=0
while '30' not in district_df['Date'].iloc[i]:
    i=i+1
i=i+1
while i<n1_q4:
    
    
    if district_df['Date'].iloc[i]==district_df['Date'].iloc[i-1]:
        i=i+1
        continue
      
    counter_q4=counter_q4+1      #for keeping count of days 
    
    if counter_q4==7:       #last day of week
        
        j=0
        while i+j<n1_q4-1:
            
            cases_q4=district_df['Confirmed'].iloc[i+j]
            temp=cases_q4
            cases_q4=cases_q4-cumulativeq4_dict[district_df['District'].iloc[i+j]]
            dist_keyq4_list.append(district_df['District'].iloc[i+j])
            weekq4_list.append(week_q4)
            casesq4_list.append(cases_q4)
            cumulativeq4_dict[district_df['District'].iloc[i+j]]=temp
            if district_df['Date'].iloc[i+j] != district_df['Date'].iloc[i+j+1]:
                break
            j=j+1
            
        
        counter_q4=0
        week_q4=week_q4+2
        
    i=i+1
        


# In[66]:


data={'District':dist_keyq4_list,'week':weekq4_list,'cases':casesq4_list}
type2_week_df=pd.DataFrame(data)
#type2_week_df


# In[67]:


#week of sunday to saturday
#calculation will be done by importing cases-week.csv and changing weeks from 1,2,3,4... to 1,3,5,7....
type1_week_df=pd.read_csv('output files/cases-week.csv')
week_q4_list=type1_week_df['week'].to_list()
n2_q4=len(type1_week_df)
i=0
while i<n2_q4:
    week_q4_list[i]=2*week_q4_list[i] - 1
    i=i+1
    
type1_week_df['week']=week_q4_list
#type1_week_df


# In[68]:


overlapped_week_df=pd.merge(type1_week_df,type2_week_df,how='outer')
overlapped_week_df=overlapped_week_df.sort_values('week')
#overlapped_week_df


# In[69]:


max_cases_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
max_wave1_weekid_dict=dict(zip(dist_code_for_q3,[1]*len(dist_code_for_q3)))
for i in range(40000):
    if overlapped_week_df['cases'].iloc[i] > max_cases_dict[overlapped_week_df['District'].iloc[i]]:
        max_cases_dict[overlapped_week_df['District'].iloc[i]]=overlapped_week_df['cases'].iloc[i]
        max_wave1_weekid_dict[overlapped_week_df['District'].iloc[i]]=overlapped_week_df['week'].iloc[i]
       
    
test_df=pd.DataFrame.from_dict(max_wave1_weekid_dict.items())
test1_df=pd.DataFrame()
test1_df['District']=test_df[0]
test1_df['wave1-weekid']=test_df[1]
#test1_df


# In[70]:


max_cases_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
max_wave2_weekid_dict=dict(zip(dist_code_for_q3,[1]*len(dist_code_for_q3)))
for i in range(40001,83000):
    if overlapped_week_df['cases'].iloc[i] > max_cases_dict[overlapped_week_df['District'].iloc[i]]:
        max_cases_dict[overlapped_week_df['District'].iloc[i]]=overlapped_week_df['cases'].iloc[i]
        max_wave2_weekid_dict[overlapped_week_df['District'].iloc[i]]=overlapped_week_df['week'].iloc[i]
        
test_df=pd.DataFrame.from_dict(max_wave2_weekid_dict.items())
test2_df=pd.DataFrame()
test2_df['District']=test_df[0]
test2_df['wave2-weekid']=test_df[1]
#test2_df


# ### Calculation of peak months

# In[71]:


#WAVE-1
monthq4_df=pd.read_csv('output files/cases-month.csv')
monthq4_df=monthq4_df.sort_values('month')

max_cases_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
max_wave1_monthid_dict=dict(zip(dist_code_for_q3,[1]*len(dist_code_for_q3)))
for i in range(4300):
    if monthq4_df['cases'].iloc[i] > max_cases_dict[monthq4_df['District'].iloc[i]]:
        max_cases_dict[monthq4_df['District'].iloc[i]]=monthq4_df['cases'].iloc[i]
        max_wave1_monthid_dict[monthq4_df['District'].iloc[i]]=monthq4_df['month'].iloc[i]
        
test_df=pd.DataFrame.from_dict(max_wave1_monthid_dict.items())
test3_df=pd.DataFrame()
test3_df['District']=test_df[0]
test3_df['wave1-monthid']=test_df[1]
#test3_df


# In[72]:




#WAVE-2
max_cases_dict=dict(zip(dist_code_for_q3,[0]*len(dist_code_for_q3)))
max_wave2_monthid_dict=dict(zip(dist_code_for_q3,[1]*len(dist_code_for_q3)))
for i in range(4301,9200):
    if monthq4_df['cases'].iloc[i] > max_cases_dict[monthq4_df['District'].iloc[i]]:
        max_cases_dict[monthq4_df['District'].iloc[i]]=monthq4_df['cases'].iloc[i]
        max_wave2_monthid_dict[monthq4_df['District'].iloc[i]]=monthq4_df['month'].iloc[i]
        
test_df=pd.DataFrame.from_dict(max_wave2_monthid_dict.items())
test4_df=pd.DataFrame()
test4_df['District']=test_df[0]
test4_df['wave2-monthid']=test_df[1]
#test4_df


# ### creation of file districts-peak.csv

# In[73]:


q1_dist_list=pd.read_csv('datasets/q1-dist-list-df.csv')
district_peak_df=pd.merge(test1_df,test2_df)
district_peak_df=pd.merge(district_peak_df,test3_df)
district_peak_df=pd.merge(district_peak_df,test4_df)
district_peak_df=pd.merge(district_peak_df,q1_dist_list)   # removing all districts not in ques1 district list

'''Some districts have all the entries as 1 of column wave1-weekid,  wave2-weekid, wave1-monthid and wave2-monthid
This is supposedly due to reasons such as NEGATIVE ENTRIES in cowin-vaccine data and incorrect cummulative entries.
These can be left as it is but I am going to remove them because they behave somewhat like outliers/noise'''
#removing rows having all entries as 1
district_peak_df=district_peak_df.drop(district_peak_df[(district_peak_df['wave1-weekid']==1)&(district_peak_df['wave2-weekid']==1)&(district_peak_df['wave1-monthid']==1)&(district_peak_df['wave2-monthid']==1) ].index,axis=0)



district_peak_df.to_csv('output files/district-peaks.csv',index=False)


# ## State-peaks.csv

# ### week-wise peak calculation

# In[74]:


# converting district data into state-wise data
overlapped_week_df.to_csv('datasets/overlapped_week-df.csv',index=False)
state_wise_df=pd.read_csv('datasets/overlapped_week-df.csv')
state_wise_df=state_wise_df.sort_values('week')
state_wise_df=state_wise_df.replace(to_replace='_.*',value='',regex=True)
state_wise_df=state_wise_df.rename(columns={'District':'state'})

state_list=state_wise_df['state'].unique().tolist()
state_wise_df=state_wise_df.groupby(['state','week']).sum()  # here groupby is applied on state and week together. So we cannot
                                                             # apply operation on state column alone. That is why i am saving csv file in next step


state_wise_df=state_wise_df.sort_values('week')
state_wise_df.to_csv('datasets/state-wise-df.csv')
state_wise_df=pd.read_csv('datasets/state-wise-df.csv')

#wave1
max_cases_state_dict=dict(zip(state_list,[0]*len(state_list)))
max_wave1_weekid_state_dict=dict(zip(state_list,[1]*len(state_list)))
for i in range(2000):       # len(state_wise_df)=4156  , so i have traversed from row 1 to 1000 for wave-1
    if state_wise_df['cases'].iloc[i] > max_cases_state_dict[state_wise_df['state'].iloc[i]]:
        max_cases_state_dict[state_wise_df['state'].iloc[i]]=state_wise_df['cases'].iloc[i]
        max_wave1_weekid_state_dict[state_wise_df['state'].iloc[i]]=state_wise_df['week'].iloc[i]
        
#wave2
max_cases_state_dict=dict(zip(state_list,[0]*len(state_list)))
max_wave2_weekid_state_dict=dict(zip(state_list,[1]*len(state_list)))
for i in range(2001,4100):
    if state_wise_df['cases'].iloc[i] > max_cases_state_dict[state_wise_df['state'].iloc[i]]:
        max_cases_state_dict[state_wise_df['state'].iloc[i]]=state_wise_df['cases'].iloc[i]
        max_wave2_weekid_state_dict[state_wise_df['state'].iloc[i]]=state_wise_df['week'].iloc[i]
        
#converting dictionaries to dataframe so that we can merge them at end easily
test_df=pd.DataFrame.from_dict(max_wave1_weekid_state_dict.items())
test5_df=pd.DataFrame()
test5_df['state']=test_df[0]
test5_df['wave1-weekid']=test_df[1]

test_df=pd.DataFrame.from_dict(max_wave2_weekid_state_dict.items())
test6_df=pd.DataFrame()
test6_df['state']=test_df[0]
test6_df['wave2-weekid']=test_df[1]


# ### month-wise peak calculation

# In[75]:


# converting district data into state-wise data
state_wise_month_df=pd.read_csv('output files/cases-month.csv')
state_wise_month_df=state_wise_month_df.sort_values('month')
state_wise_month_df=state_wise_month_df.replace(to_replace='_.*',value='',regex=True)
state_wise_month_df=state_wise_month_df.rename(columns={'District':'state'})

state_wise_month_df=state_wise_month_df.groupby(['state','month']).sum()  

state_wise_month_df=state_wise_month_df.sort_values('month')
state_wise_month_df.to_csv('datasets/state-wise-month-df.csv')
state_wise_month_df=pd.read_csv('datasets/state-wise-month-df.csv')

#wave1
max_cases_state_dict=dict(zip(state_list,[0]*len(state_list)))
max_wave1_monthid_state_dict=dict(zip(state_list,[1]*len(state_list)))
for i in range(230):
    if state_wise_month_df['cases'].iloc[i] > max_cases_state_dict[state_wise_month_df['state'].iloc[i]]:
        max_cases_state_dict[state_wise_month_df['state'].iloc[i]]=state_wise_month_df['cases'].iloc[i]
        max_wave1_monthid_state_dict[state_wise_month_df['state'].iloc[i]]=state_wise_month_df['month'].iloc[i]
        
#wave2
max_cases_state_dict=dict(zip(state_list,[0]*len(state_list)))
max_wave2_monthid_state_dict=dict(zip(state_list,[1]*len(state_list)))
for i in range(231,470):
    if state_wise_month_df['cases'].iloc[i] > max_cases_state_dict[state_wise_month_df['state'].iloc[i]]:
        max_cases_state_dict[state_wise_month_df['state'].iloc[i]]=state_wise_month_df['cases'].iloc[i]
        max_wave2_monthid_state_dict[state_wise_month_df['state'].iloc[i]]=state_wise_month_df['month'].iloc[i]
        

#converting dictionaries to dataframe so that we can merge them at end easily
test_df=pd.DataFrame.from_dict(max_wave1_monthid_state_dict.items())
test7_df=pd.DataFrame()
test7_df['state']=test_df[0]
test7_df['wave1-monthid']=test_df[1]

test_df=pd.DataFrame.from_dict(max_wave2_monthid_state_dict.items())
test8_df=pd.DataFrame()
test8_df['state']=test_df[0]
test8_df['wave2-monthid']=test_df[1]


# In[76]:


month_peak_df=pd.merge(test5_df,test6_df)
month_peak_df=pd.merge(month_peak_df,test7_df)
month_peak_df=pd.merge(month_peak_df,test8_df)

'''Some states have all the entries as 1 of column wave1-weekid,  wave2-weekid, wave1-monthid and wave2-monthid
This is supposedly due to reasons such as NEGATIVE ENTRIES in cowin-vaccine data and incorrect cummulative entries.
These can be left as it is but I am going to remove them because they behave somewhat like outliers/noise'''
#removing rows having all entries as 1
month_peak_df=month_peak_df.drop(month_peak_df[(month_peak_df['wave1-weekid']==1)&(month_peak_df['wave2-weekid']==1)&(month_peak_df['wave1-monthid']==1)&(month_peak_df['wave2-monthid']==1) ].index,axis=0)
#removing another outlier
month_peak_df=month_peak_df.drop(month_peak_df[(month_peak_df['state']=='TG')].index,axis=0)


month_peak_df.to_csv('output files/state-peaks.csv',index=False)


# ## Overall-peaks.csv

# In[77]:


overall_week_df=state_wise_df
overall_week_df['state']=overall_week_df['state'].replace(to_replace='^.*',value='India',regex=True)
overall_week_df=overall_week_df.rename(columns={'state':'overall'})


# ### week wise peak calculation

# In[78]:


overall_week_df=overall_week_df.groupby(['overall','week']).sum()
overall_week_df.to_csv('datasets/overall-week-df.csv')
overall_week_df=pd.read_csv('datasets/overall-week-df.csv')

wave1_weekid=1
max_cases=0
for i in range(60):
    if overall_week_df['cases'].iloc[i] > max_cases:
        max_cases=overall_week_df['cases'].iloc[i]
        wave1_weekid=overall_week_df['week'].iloc[i]

        
wave2_weekid=61
max_cases=0
for i in range(61,135):
    if overall_week_df['cases'].iloc[i] > max_cases:
        max_cases=overall_week_df['cases'].iloc[i]
        wave2_weekid=overall_week_df['week'].iloc[i]
        


# ### Month wise peak calculation

# In[79]:


overall_month_df=state_wise_month_df
overall_month_df=overall_month_df.replace(to_replace='^.*',value='India',regex=True)
overall_month_df.rename(columns={'state':'overall'},inplace=True)
overall_month_df=overall_month_df.groupby(['overall','month']).sum()
overall_month_df.to_csv('datasets/overall-month-df.csv',index=False) #groupby has been applied so the relation between columns has been changed.We need to save and load csv again
overall_month_df=pd.read_csv('datasets/overall-month-df.csv')



# There are only 15 rows. It is clear that wave1-month is 5th month(cases=2105105) and wave2-month is 13th month(cases=9109152)

wave1_monthid=5
wave2_monthid=13


# ### creation of overall-peaks.csv

# In[80]:


overall_peaks=pd.DataFrame(data={'overall':'India','wave1-weekid':wave1_weekid,'wave2-weekid':wave2_weekid,'wave1-monthid':5,'wave2_monthid':13},index=[0])
overall_peaks.to_csv('output files/overall-peaks.csv',index=False)


# #   
