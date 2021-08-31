#!/usr/bin/env python
# coding: utf-8

# In[77]:


import csv
import pandas as pd
xls = pd.read_csv('Liferay_table.csv', sep = '\t', header = None)
list_pdf = xls.fillna(0).values.tolist()
table_el = []
table_idx = []
for i in range(len(list_pdf)):
    if list_pdf[i][0] != 0:
        table_col = []
        list_filter = [el for el in list_pdf[i] if el != 0]
        if len(list_filter) != 1:
            table_idx.append(i)
            for j in range(len(list_filter)):
                table_col.append(list_filter[j])    
        table_el.append(table_col)
    else:
        table_col = []
        for k in range(len(list_pdf[i])):
            if list_pdf[i][k] != 0:
                table_col.append(list_pdf[i][k])
                table_idx.append(i)
        table_el.append(table_col) 

for idx in range(len(table_el) - 1,-1,-1):
    if table_el[idx] == []:
        del(table_el[idx])


textfile = open("table_file.txt", "w")
for element in table_el:
    for el in element:
        textfile.write(el + "\n")
textfile.close()

textfileid = open("table_idx.txt", "w")
for element in table_idx:
    textfileid.write(str(element) + "\n")
textfileid.close()


# In[51]:


table_elements = []
# Assuming that you have loaded data into a lines variable. 
for line in table_el:
    for el in line:
        table_elements.append(el.strip().split('\n'))
        
list_elements = []
for el in table_elements:
    for element in el:
        list_elements.append(element)


# In[31]:


from pd3f import extract
# use: >> http://localhost:3001/api/v1/json/...[server job code]
text, tables = extract('Liferay_no_hf.pdf', tables=False, experimental=False, force_gpu=False, lang="multi", fast=False, parsr_location="localhost:3001")


# In[33]:


import json
with open('Liferay_nohf.json') as f:
    data = json.load(f)


# In[34]:


def sentence_join(data):
    for idx, pages in enumerate(data['pages']):
        for idx2, para in enumerate(data['pages'][idx]['elements']):
            for idx3, line in enumerate(data['pages'][idx]['elements'][idx2]['content']):
                if 'content' in line:
                    sentence = ""
                    for idx4, word in enumerate(data['pages'][idx]['elements'][idx2]['content'][idx3]['content']):
                        sentence = sentence + " " + word['content']
                line['content'] = sentence
    return data


# In[59]:


def element_match(table_el, data):
    table_info = []
    for idx, pages in enumerate(data['pages']):
        for idx2, para in enumerate(data['pages'][idx]['elements']):
            count = 0
            for idx3, line in enumerate(data['pages'][idx]['elements'][idx2]['content']):
                if any(word in line['content'] for word in table_el):
                    count += 1
                else:
                    break
            if count > 4:
                pageno = data['pages'][idx]['pageNumber']
                bbox_l = data['pages'][idx]['elements'][idx2]['box']['l']
                bbox_t = data['pages'][idx]['elements'][idx2]['box']['t']
                bbox_w = data['pages'][idx]['elements'][idx2]['box']['w']
                bbox_h = data['pages'][idx]['elements'][idx2]['box']['h']
                table_info.append(pageno)
                table_info.append(bbox_l)
                table_info.append(bbox_t)
                table_info.append(bbox_w)
                table_info.append(bbox_h) 
    return table_info
                    


# In[55]:


data_join = sentence_join(data)


# In[60]:


table_info = element_match(list_elements, data_join)


# In[68]:


textfile2 = open("table_info.txt", "w")
for k in table_info:
    textfile2.write(str(k) + "\n")
textfile2.close()

