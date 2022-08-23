#!/usr/bin/env python
# coding: utf-8

# # Answer2

# In[2]:


#preprocessing neighbor data frame
import pandas as pd
import json
import re

#loading neighbour-districts data
with open('datasets/neighbor-districts.json') as json_file:
    data = json.load(json_file)
    
neighbor_df=pd.DataFrame.from_dict(data,orient='index')
neighbor_df=neighbor_df.transpose()



#removing bad symbols and removing spelling ambgiuities
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




neighbor_df=neighbor_df.replace(to_replace='konkan division',value=None,regex=True)
neighbor_df=neighbor_df.replace(to_replace='noklak',value=None,regex=True)
neighbor_df=neighbor_df.replace(to_replace='niwari',value=None,regex=True)
neighbor_df=neighbor_df.replace(to_replace='mumbai suburban',value=None,regex=True)
neighbor_df = neighbor_df.drop('konkan division', axis=1)   #running drop function twice gives error. If you want to run twice then run first cell again
neighbor_df = neighbor_df.drop('noklak', axis=1)
neighbor_df = neighbor_df.drop('niwari', axis=1)
neighbor_df = neighbor_df.drop('mumbai suburban', axis=1)




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
    
    
import csv
edge_list=[]
for key in dict_n:
    neighbors=dict_n[key]
    for i in neighbors:
        edge_list.append([key,i])
        
edge_list.sort()


with open('output files/edge-graph.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerows(edge_list) 


# In[ ]:




