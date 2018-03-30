
# coding: utf-8

# In[1]:

import os,sys
import numpy as np
import pickle
import math
import gc


# In[2]:

src_dir = os.path.join(os.getcwd(), os.pardir, '../')
sys.path.append(src_dir)


# In[3]:

DATA_ROOT = "/media/felipe/SAMSUNG/delicious/delicioust140"
TAGINFO = DATA_ROOT+"/taginfo.xml"
INTERIM_DATA_ROOT = os.path.abspath("../../data/interim/delicious-t140/")
MAX_NB_WORDS = 5000
SEED= 42
SAMPLE_FRAC = 0.1


# In[4]:

from src.data.delicious_t140 import get_full_from_cache
from src.utils.dataframes import sample_rows
from src.features.delicious_t140 import clean_text_delicious


# In[5]:

df = get_full_from_cache(INTERIM_DATA_ROOT,with_contents=True)


# In[6]:

np.random.seed(SEED)


# In[7]:

num_rows = len(df)

def get_indices(total_rows, step):
    
    max_num_parts = math.ceil(total_rows/step)
    
    for i in range(0,max_num_parts):
        min_row = i*step
        max_row = min(min_row + step,total_rows-1)
        
        yield (min_row,max_row)


# In[8]:

df.head()


# In[9]:

[i for i in get_indices(len(df),10000)]


# In[ ]:

df.index[0:11000]


# In[10]:

df2 = df.drop(df.index[0:60000])


# In[13]:

del df


# In[22]:

foo = gc.collect()
print(foo)

