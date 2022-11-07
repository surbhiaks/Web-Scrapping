#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# ### Extracting the links, data & content from the first 100 pages:

# In[28]:


url_pages = []
# urls_list = []
for i in range(0,101):
    url = f"https://www.contractsfinder.service.gov.uk/Search/Results?&page={i}#dashboard_notices"
    url_pages.append(url)
for m in url_pages:
    response = requests.get(m)
    page_contents = response.text
    doc = BeautifulSoup(page_contents,"html.parser")


# In[30]:


datas = []
for i in url_pages:
    response = requests.get(i)
    page_contents = response.content
    doc = BeautifulSoup(page_contents,"html.parser")
    data = doc.find_all("div",{"class":"search-result-entry"})
    for d in data:
        datas.append(list(d.stripped_strings))


# In[31]:


lists = []
for d in range(len(datas)):
#     for i in datas
    lists.append(datas[d][0])


# In[32]:


lists = set(lists)
key = list(lists)
key.sort()
keys = []
for i in key:
    print(i)
    keys.append(i)


# In[33]:


main_content=[]
for i in url_pages:
    response = requests.get(url)
    page_contents = response.content
    doc = BeautifulSoup(page_contents,"html.parser")
    content = doc.find_all(class_="search-result")
    print(content)
    for i in content:
        main_content.append(list(i.stripped_strings))


# In[34]:


Heading = []
Sub_heading = []
for m in main_content:
    Heading.append(m[0])
    Sub_heading.append(m[1])


# In[35]:


Approach_to_market_date = []
Closing = []
Contract_location = []
Contract_value = []
Notice_status = []
Procurement_stage = []
Publication_date = []
for m in main_content:
    if keys[0]in m:
        iloc = m.index(keys[0])+1
        Approach_to_market_date.append(m[iloc])
    else:
        Approach_to_market_date.append(np.nan)
    if keys[1]in m:
        iloc = m.index(keys[1])+1
        Closing.append(m[iloc])
    else:
        Closing.append(np.nan)
    if keys[2]in m:
        iloc = m.index(keys[2])+1
        Contract_location.append(m[iloc])
    else:
        Contract_location.append(np.nan)
    if keys[3]in m:
        iloc = m.index(keys[3])+1
        Contract_value.append(m[iloc])
    else:
        Contract_value.append(np.nan)
    if keys[4]in m:
        iloc = m.index(keys[4])+1
        Notice_status.append(m[iloc])
    else:
        Notice_status.append(np.nan)
    if keys[5]in m:
        iloc = m.index(keys[5])+1
        Procurement_stage.append(m[iloc])
    else:
        Procurement_stage.append(np.nan)
    if keys[6]in m:
        iloc = m.index(keys[6])+1
        Publication_date.append(m[iloc])
    else:
        Publication_date.append(np.nan)


# ### Creating a DataFrame

# In[200]:


df = pd.DataFrame({"Heading":Heading,"Sub_Heading":Sub_heading,"Closing":Closing,"Notice_status":Notice_status,"Contract_location":Contract_location,"Contract_value":Contract_value,"Publication_date":Publication_date,"Procurement_stage":Procurement_stage,"Approach_to_market_date":Approach_to_market_date})


# ### Converting Approach_to_market_date, Closing, Publication_date into datetime

# In[201]:


df["Approach_to_market_date"] = pd.to_datetime(df["Approach_to_market_date"])


# In[202]:


df["Closing"] = pd.to_datetime(df["Closing"])


# In[203]:


for i in range(len(df["Publication_date"])):
    df["Publication_date"][i]=df["Publication_date"][i].split(",")[0]


# In[204]:


df["Publication_date"] = pd.to_datetime(df["Publication_date"])


# ### Converting Contract_value from object to float

# In[220]:


vals = []
for i in df["Contract_value"]:
    if type(i)!=float:
        x = i.replace("£","")
        z = x.replace(",","")
        y = z.split("to")
        num_list = []
        for num in y:
            num_list.append(float(num))
        vals.append((sum(num_list)/len(num_list)))
    else:
        vals.append(i)


# In[221]:


df["Contract_value"]=vals


# In[222]:


df.head(2)


# ### Data Visualisation

# In[211]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[218]:


plt.figure(figsize=(17,15))
ax = sns.barplot(x = "Contract_location",y = "Contract_value" ,hue="Procurement_stage",data = df)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()
plt.show()


# In[219]:


plt.figure(figsize=(17,15))
ax = sns.countplot(x = "Contract_location",hue="Procurement_stage",data = df)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()
plt.show()


# In[224]:


df.head(1)


# In[228]:


fig,ax = plt.subplots(figsize=(20,5))

sns.kdeplot(df[df["Procurement_stage"]=="Opportunity"]["Closing"], shade=True, color="blue", label="Opportunity",ax=ax)
sns.kdeplot(df[df["Procurement_stage"]=="Future Opportunity"]["Closing"], shade=True, color="green", label="Future Opportunity",ax=ax)
sns.kdeplot(df[df["Procurement_stage"]=="Early engagement"]["Closing"], shade=True, color="red", label="Early engagement",ax=ax)

ax.set_xlabel("closing")
ax.set_ylabel("Counts")

fig.suptitle("Closing vs.  Procurement stage")

ax.legend();


# ### Saving Dataframe to CSV

# In[232]:


df.to_csv("Internship_task.csv")


# In[ ]:




