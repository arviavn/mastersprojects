#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import lzma
import ast
from pympler import asizeof
import os


# In[2]:


def compress_message(message):
    compressed_message = lzma.compress(message)
    return compressed_message


# In[3]:


def decompress_message(compressed_message):
    decompressed_message = lzma.decompress(compressed_message)
    dic_str = str(decompressed_message).replace("\"","")[1:]
    result = ast.literal_eval(dic_str)
    return result


# In[4]:


def gen_adjacency_list(edges_dataframe):
    adjlist = {}
    start = pd.Timestamp.now()
    for index, edge in edges_dataframe.iterrows():
        src = edge[0]
        trg = edge[1]

        if src not in adjlist.keys():
            adjlist[src] = {'out_vertices': [trg],
                           'in_vertices': []}
        else:
            adjlist[src]['out_vertices'].append(trg)

        if trg not in adjlist.keys():
            adjlist[trg] = {'in_vertices': [src],
                           'out_vertices': []}
        else:
            adjlist[trg]['in_vertices'].append(src)
    timetaken = pd.Timestamp.now() - start
#     print(timetaken)
    return adjlist, timetaken


# In[5]:


def calculate_degree(adjacency_list):
    start = pd.Timestamp.now()
    degree = {v: {"in": len(adjacency_list[v]['in_vertices']), "out": len(adjacency_list[v]['out_vertices'])} for v in adjacency_list}
    timetaken = pd.Timestamp.now() - start
    return degree, timetaken


# In[6]:


def compress_adj_list(adj):
    start = pd.Timestamp.now()    
    compressed_adj_list = {v: compress_message(str(adj[v]).encode('utf-8')) for v in adj}
    timetaken = pd.Timestamp.now() - start
    cmpr_ratio = asizeof.asizeof(adj)/asizeof.asizeof(compressed_adj_list)
    return compressed_adj_list, cmpr_ratio, timetaken


# In[7]:


def apply_lzma(edges_dataframees_dataframe, file_name):
    report = {}
    
    adjacency_list,adjacency_list_tt = gen_adjacency_list(edges_dataframe)
    
    compressed_adjacency_list, compression_ratio, compression_time = compress_adj_list(adjacency_list)

    nodes_count = len(adjacency_list)
    in_edges_count = sum([len(adjacency_list[vertex]['in_vertices']) for vertex in adjacency_list])
    out_edges_count = sum([len(adjacency_list[vertex]['out_vertices']) for vertex in adjacency_list])
    
    
    report[file_name] = {"graph_creation_time" : adjacency_list_tt,
                         "nodes_count" : nodes_count,
                         "in_edges_count": in_edges_count,
                         "out_edges_count": out_edges_count,
                         "compression_time": compression_time,
                         "compression_ratio": compression_ratio}
    
    return compressed_adjacency_list, report


# In[ ]:


resulting_report = {}
compressed_data_list = {}
directory = "./filestobecompressed/"

for filename in os.listdir(directory):
    filename_without_ext = str(filename).split(".")[0]

    start_edges_df_read = pd.Timestamp.now()    
    edges_dataframe = pd.read_csv((directory + filename), sep= " ",header=None, low_memory=True,)
    timetaken_edges_df_read = pd.Timestamp.now() - start_edges_df_read
    print(filename_without_ext, "\ttime : ", timetaken_edges_df_read)    
#     print(edges_dataframe.head(10))
    
    compressed_adjacency_list, report = apply_lzma(edges_dataframe, filename_without_ext)
    
    resulting_report.update(report)
    compressed_data_list[filename_without_ext] = compressed_adjacency_list
    
#     print(filename) 
#     print(filename, "\tlen : ", len(df[0]), "\ttime : ", timetaken_edges_df_read)
#     tdic[str(filename).split(".")[0]] = pd.read_csv(('./second/' + filename), sep= " ",header=None)


# In[ ]:




