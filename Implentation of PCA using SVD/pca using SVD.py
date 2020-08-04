#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler


# In[2]:


movies = pd.read_excel("C:/Users/ArviROG/Desktop/movie.xlsx",sheet_name='Movie_data')
ratings = pd.read_excel("C:/Users/ArviROG/Desktop/movie.xlsx",sheet_name='Rating')


# In[3]:


ratings.describe()
print(ratings.shape)


# In[4]:


print(movies.shape)
movies.describe()


# In[5]:


movies.head(5)


# In[6]:


movies.head(5)


# In[7]:


def replace_name(x):
    return movies[movies['movieId']==x].title.values[0]

ratings.movieId = ratings.movieId.map(replace_name)


# In[8]:


ratings.movieId.head(5)


# In[9]:


M = ratings.pivot_table(index=['userId'], columns=['movieId'], values='rating')


# In[10]:


print(M.shape)
M.head(6)


# In[11]:


M.describe()


# In[12]:


df1 = M.replace(np.nan, 0, regex=True)
df1


# In[20]:


X_std = StandardScaler().fit_transform(df1)
X_std


# In[21]:


svd = TruncatedSVD(n_components=240)
svd


# In[22]:


U = svd.fit_transform(X_std)
U


# In[23]:


VT = svd.components_
VT


# In[24]:


S = svd.explained_variance_ratio_
S.shape
S


# In[25]:


print(svd.explained_variance_ratio_.sum())
plt.plot(np.cumsum(S))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.show()


# In[ ]:




