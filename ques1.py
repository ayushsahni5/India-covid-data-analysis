#!/usr/bin/env python
# coding: utf-8

# # Answer1

# ### Pre-processing neighbor-district.json

# In[30]:


import pandas as pd
import json
import re

#loading neighbour-districts data
with open('datasets/neighbor-districts.json') as json_file:
    data = json.load(json_file)
    
neighbor_df=pd.DataFrame.from_dict(data,orient='index')
neighbor_df=neighbor_df.transpose()



#removing bad symbols and correcting spelling ambiguities
neighbor_df=neighbor_df.replace(to_replace='_',value=' ',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('_',' ',x))

neighbor_df=neighbor_df.replace(to_replace=' district',value='',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub(' district','',x))

neighbor_df=neighbor_df.replace(to_replace='–',value=' ',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('–',' ',x))

neighbor_df=neighbor_df.replace(to_replace='-',value=' ',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('-',' ',x))

neighbor_df=neighbor_df.replace(to_replace='ri bhoi',value='ribhoi',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('ri bhoi','ribhoi',x))


# These districts have same name but belong to two different districts:-
#    Hamirpur, pratapgarh, bilaspur, bijapur(vijayapura), balrampur and aurangabad    ....I found these districts to be duplicate at later stage in this code
redundancy_dict={'hamirpur/Q2086180' : 'HP_hamirpur', 'hamirpur/Q2019757' : 'UP_hamirpur' , 'bijapur_district/Q1727570': 'KA_vijayapura' , 'bijapur/Q100164' : 'CT_bijapur' , 'pratapgarh/Q1585433' : 'RJ_pratapgarh' , 'pratapgarh/Q1473962' : 'UP_pratapgarh' , 'balrampur/Q1948380' : 'UP_balrampur' , 'balrampur/Q16056268' : 'CT_balrampur' , 'bilaspur/Q100157' : 'CT_bilaspur' , 'bilaspur/Q1478939': 'HP_bilaspur' ,  'aurangabad/Q592942' : 'MH_aurangabad' , 'aurangabad/Q43086' : 'BR_aurangabad'}
neighbor_df=neighbor_df.replace(redundancy_dict)
neighbor_df=neighbor_df.rename(columns=redundancy_dict)


#removing unneccesary suffixes and other symbols in district names
neighbor_df=neighbor_df.replace(to_replace='\/Q.*',value='',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('\/Q.*','',x))

neighbor_df=neighbor_df.replace(to_replace='\/None',value='',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('\/None','',x))

#Correcting name of lahaul and spiti(I have already manually found this incorrect name)
neighbor_df=neighbor_df.replace(to_replace='lahul',value='lahaul',regex=True)

neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('lahul','lahaul',x))

neighbor_df=neighbor_df.replace(to_replace='bangalore',value='bengaluru',regex=True)  #bangalore is officially bengaluru
neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('bangalore','bengaluru',x))
neighbor_df=neighbor_df.replace(to_replace='belgaum',value='belagavi',regex=True)  #belgaum is officially belagavi
neighbor_df=neighbor_df.rename(columns=lambda x: re.sub('belgaum','belagavi',x))


# ### Pre-processing of District-wise covid data

# In[31]:



dwise_df=pd.read_csv("datasets/district_wise.csv",index_col=False)
dwise_df=dwise_df[['State_Code','State','District_Key','District']]
dwise_df=dwise_df.iloc[1:]
dwise_df=dwise_df.reset_index(drop=True)
dwise_df=dwise_df.drop(dwise_df[dwise_df['District']=='Unknown'].index)
dwise_df.drop_duplicates(subset =['State_Code','State','District_Key','District'],keep = 'first', inplace = True)
#dwise_df


# ### Pre-processing of cowin vaccine data

# In[32]:


vaccine_df=pd.read_csv('datasets/cowin_vaccine_data_districtwise.csv',low_memory=False)
vaccine_df=vaccine_df[['State_Code','State','District_Key','District']]
vaccine_df=vaccine_df.iloc[1:]
vaccine_df=vaccine_df.replace(to_replace='Bangalore',value='Bengaluru',regex=True)  #Bangalore is officially Bengaluru
vaccine_df=vaccine_df.replace(to_replace='Belgaum',value='Belagavi',regex=True)
vaccine_df=vaccine_df.replace(to_replace='Ri-Bhoi',value='Ribhoi',regex=True)
vaccine_df.drop_duplicates(subset=['State_Code','State','District_Key','District'],keep ='first', inplace = True)


# In[33]:


# I am applying intersection according to both states-name and district-name because some districts have same name in two different states
# For example, Pratapgarh is present in UP and Rajasthan both
common_df=pd.merge(vaccine_df,dwise_df)        #To get common states and districts in cowin vaccination data and covid data
#common_df[common_df['State_Code']=='TG']


# In[34]:


unique_districts_common=common_df['District'].to_list()
unique_districts_neighbor=neighbor_df.keys()
diff=set(unique_districts_neighbor)-set(unique_districts_common)


# In[35]:


for i in range(len(unique_districts_common)):
    unique_districts_common[i]=unique_districts_common[i].lower()
#unique_districts_common


# ### Districts present in neighbor.json but not in cowin_vaccine and covid_data

# In[36]:


diff=set(unique_districts_neighbor)-set(unique_districts_common)
           #These districts need to be checked for spelling mistakes or other reasons of their absence in cowin_vaccine and covid_data.

           #shorthands--> list1 = neighbor.json data        list2=merged data(intersection) of cowin_vaccine and covid_data
           #[wrong spellings:correct spelling] :- 
           #list2=['aizawl':'aizwal', 'Ashoknagar':'ashok nagar', ]  ....these are spelling mistakes in covid_data but I will not change them because question has asked to change only neighbor_data according to covid_data
           #list1=['anugul':'angul', 'badgam':'budgam', 'baleshwar':'balasore', 'banas kantha':'banaskantha', 'baramula':'baramulla', 'baudh':'boudh', 'bellary':'ballari', .....so on]
           # I will put the whole list2 in a csv file in next step and load it into dictionary to replace wrong spellings with correct spellings
    
    #NOTE: some of the districts are present in both but still are shown in output because I had to replace them 
    #with their district_key because those districts were present in two states. Anyway, it doesnt create any problem.


# ## handling the case of same named districts in two different states and incorrect spellings

# In[37]:


# I have used the names obtained here of such districts and modified them directly in the first block at the beginning of code
keys_df=pd.read_csv('datasets/district_keys.csv')
keys_df=keys_df.replace(to_replace='^ ',value='',regex=True)
values_df=pd.read_csv('datasets/district_values.csv')
values_df=values_df.replace(to_replace='^ ',value='',regex=True)
keys_list=keys_df['A'].to_list()
values_list=values_df['B'].to_list()
dictionary = dict(zip(keys_list, values_list))
for col in neighbor_df:
    neighbor_df=neighbor_df.replace({col: dictionary})
    
neighbor_df=neighbor_df.rename(columns=dictionary)
    
#values_list
#dictionary
#neighbor_df['hamirpur']
duplicate_columns_df = neighbor_df.loc[:,neighbor_df.columns.duplicated()]   # Using these I found that Hamirpur, bilaspur,balrampur,aurangabad,bijapur and pratapgarh belong to two different states
#neighbor_df


# ## After above corrections let us again check how many districts are now present in neighbor data but not in covid data

# In[38]:


neighbor_district_list=neighbor_df.keys()
covid_district_list=common_df['District'].to_list()

for i in range(len(covid_district_list)):
    covid_district_list[i]=covid_district_list[i].lower()
difference_list=set(neighbor_district_list)-set(covid_district_list)
#difference_list

#NOTE: These districts will not match becasue they had been replaced with their district_key:-
# 'BR_aurangabad',
# 'CT_balrampur',
# 'CT_bijapur',
# 'CT_bilaspur',
# 'HP_bilaspur',
# 'HP_hamirpur',
# 'MH_aurangabad',
# 'RJ_pratapgarh',
# 'UP_balrampur',
# 'UP_hamirpur',
# 'UP_pratapagarh

#Hence this reveal that only konkan division, mumbai suburban, niwari and noklak are absent in covid_data. We will simply drop these


# In[39]:


neighbor_df=neighbor_df.replace(to_replace='konkan division',value=None,regex=True)
neighbor_df=neighbor_df.replace(to_replace='noklak',value=None,regex=True)
neighbor_df=neighbor_df.replace(to_replace='niwari',value=None,regex=True)
neighbor_df=neighbor_df.replace(to_replace='mumbai suburban',value=None,regex=True)
neighbor_df = neighbor_df.drop('konkan division', axis=1)   #running drop function twice gives error. If you want to run twice then run first cell again
neighbor_df = neighbor_df.drop('noklak', axis=1)
neighbor_df = neighbor_df.drop('niwari', axis=1)
neighbor_df = neighbor_df.drop('mumbai suburban', axis=1)
#neighbor_df


# ## Replacing district name with district key

# In[40]:



district_name_key=pd.read_csv("datasets/district_name_key.csv")
district_code_value=pd.read_csv("datasets/district_code_value.csv")
d_n_list=district_name_key['A'].to_list()
for i in range(len(d_n_list)):
    d_n_list[i]=d_n_list[i].lower()
d_c_list=district_code_value['B'].to_list()
dict_final=dict(zip(d_n_list,d_c_list))
for col in neighbor_df:
    neighbor_df=neighbor_df.replace({col: dict_final})
    
neighbor_df=neighbor_df.rename(columns=dict_final)
neighbor_df.to_csv('datasets/neighbor-df.csv',index=False)  # this is refined neighbor dataframe. It will be used in next questions.


# ## Creating neighbor-districts-modified.json data 

# In[41]:


#Writing neighbor-district-modified.json file

import collections
dict_n={}
for col in neighbor_df:
    
    list1=neighbor_df[col].to_list()
    try:
        while True:
            list1.remove(None)
    except ValueError:
        pass
    list1.sort()
    dict_n[col]=list1
    
    
od = collections.OrderedDict(sorted(dict_n.items()))   #ordered dictionary for printing names in sorted order in json file
with open('output files/neighbor-districts-modified.json', 'w') as json_file:
  json.dump(od, json_file,indent=2)


# In[ ]:




