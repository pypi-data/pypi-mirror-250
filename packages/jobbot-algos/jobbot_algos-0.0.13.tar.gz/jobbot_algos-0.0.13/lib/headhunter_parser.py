#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import fastcore.basics as fcb
from time import sleep
from random import uniform
import re
from jobbot_algos.postgres import PostgresConnector


# # сlass HeadHunterParser:

# In[2]:


class HeadHunterParser:
    
    base_url='https://api.hh.ru/vacancies'
    
    def __init__(self, ssh_username:str, ssh_password:str, postgres_username:str, postgres_password:str):
        
        postgres_creds = {'ssh_host':'185.247.17.122',
                          'ssh_username':ssh_username,
                          'ssh_password':ssh_password,
                          'local_host':'localhost',
                          'postgres_username':postgres_username,
                          'postgres_password':postgres_password,
                          'database':'jobbot_db'}
        
        self.pc = PostgresConnector(**postgres_creds)


# ### run:

# In[3]:


@fcb.patch_to(HeadHunterParser)

def run(self, professional_role:int, area:int, save_to_postgres=False) -> pd.DataFrame:
    
    # 1. GET URLS:
    urls = []
    for page in range(20):
        
        params = {'professional_role':professional_role, 'area':area, 'per_page':100, 'page':page} 
        json = requests.get(self.base_url, params=params).json()
        
        # break if pages are over:
        if len(json['items'])==0: break
        
        urls += pd.Series(json['items']).apply(lambda x: x['url']).to_list()
        
        # sleep:
        sleep(uniform(3,5))
        
    # 2. GET VACANCIES' INFO:
    dfs = []
    for url in urls:

        json = requests.get(url).json()

        df = pd.DataFrame({'id':[json['id']], 
                           'name':[json['name']], 
                           'profession':[json['professional_roles'][0]['name']],
                           'salary':[json['salary']], 
                           'key_skills':[json['key_skills']], 
                           'experience':[json['experience']], 
                           'description':[json['description']], 
                           'schedule':[json['schedule']],
                           'company':json['employer']['name']})

        dfs.append(df)
        sleep(uniform(1,3))

    data = pd.concat(dfs)
    data['description'] = data['description'].apply(lambda x: re.sub(re.compile('<.*?>'), '', x))
    data['key_skills']  = data['key_skills'].apply(lambda x: ', '.join([d['name'] for d in x]))
    data['experience']  = data['experience'].apply(lambda x: x['name'])
    data['schedule']    = data['schedule'].apply(lambda x: x['id'])
    data['salary_from'] = data['salary'].apply(lambda x: x['from'] if type(x)==dict else None)
    data['salary_to']   = data['salary'].apply(lambda x: x['to'] if type(x)==dict else None)
    data['currency']    = data['salary'].apply(lambda x: x['currency'] if type(x)==dict else None)
    data['area'] = area
    data = data[['id', 'area', 'profession', 'name', 'company', 'key_skills', 'experience', 'description', 'schedule', 'salary_from', 'salary_to', 'currency']]
    
    if save_to_postgres:
        self.pc.save(df=data, table_name='hh_vacancies', schema='main_schema', if_table_exists="append")
        
    return data


# In[4]:


# %%time
# hh = HeadHunterParser()
# data = hh.run(professional_role=165, area=1)
# pc.execute(f"DELETE FROM main_schema.hh_vacancies WHERE area = {data['area'].values[0]} AND profession = '{data['profession'].values[0]}'")
# pc.save(df=data, table_name='hh_vacancies', schema='main_schema', if_table_exists="append")


# In[1]:


# postgres_creds = {'ssh_host':'185.247.17.122',
#                   'ssh_username':'root',
#                   'ssh_password':'aRGgMeM7wBQ2m*',
#                   'local_host':'localhost',
#                   'postgres_username':'jobbot',
#                   'postgres_password':'12345',
#                   'database':'jobbot_db'
#                  }


# In[2]:


# pc = PostgresConnector(**postgres_creds)
# pc.check_connection()

