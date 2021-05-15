#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, sys
import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit

pd.set_option('display.max_columns', None)


module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import utils.explore_utils as eu


# In[2]:


type_map = {
    'decision_date' : 'str',
    'filing_date' : 'str',
    'Court Name' : 'category',
    'Party of Appointing President' : 'category',
    'CIRCUIT' : 'category',
    'JURIS' : 'category',
    'NOS' : 'category',
    'ORIGIN' : 'category',
    'RESIDENC' : 'category',
    'CLASSACT' : 'category',
    'DEMANDED' : 'float64',
    'TERMDATE' : 'str',
    'DISP' : 'category',
    'PROCPROG' : 'category',
    'NOJ' : 'category',
    'AMTREC' : 'category',
    'JUDGMENT' : 'category',
    'TAPEYEAR' : 'float64',
    'district' : 'category',
    'office' : 'category',
    'county' : 'category',
    'TRCLACT' : 'category',
    'PROSE' : 'category',
    'arbit' : 'category',
    'transoff' : 'category',
    'trmarb' : 'category',
    'ifp' : 'category',
    'statuscd' : 'category'
}

cols_to_drop = [
    'decision_date',
#     'filing_date',
    'TERMDATE',
    'TAPEYEAR'
]

df = pd.read_csv(
    '/scratch/ayl316/ttml_mr_data/processed_data_2/new_cases.csv.zip', 
    dtype = type_map, 
    parse_dates = ['decision_date', 'filing_date', 'TERMDATE']
).rename(columns = {
    'Court Name' : 'court_name',
    'Party of Appointing President' : 'party'
}).drop(columns = cols_to_drop)


df['filing_year'] = pd.DatetimeIndex(df['filing_date']).year
df['filing_year'] = df['filing_year'].astype(str).astype('category')
df = df.drop(columns = ['filing_date'])

for col in ['party', 'TRCLACT', 'PROSE', 'arbit', 'transoff', 'trmarb', 'ifp', 'statuscd', 'filing_year']:
    if not '-8' in df[col].cat.categories:
        df[col] = df[col].cat.add_categories('-8')
    df[col] = df[col].fillna('-8')

df['district_year'] = df['district'].astype(str) + '_' + df['filing_year'].astype(str)


# In[3]:


df.info()


# In[4]:


feature_cols = [
#     'NOJ',
#     'JUDGMENT',
#     'PROSE',
#     'trmarb',
    'CLASSACT',
    'JURIS',
#     'TRCLACT',
#     'ifp', (too many nulls)
#     'statuscd',
#     'PROCPROG',
#     'CIRCUIT',
#     'transoff',
    'ORIGIN',
#     'arbit', (too many nulls)
    'office',
#     'court_name',
    'NOS',
    'district',
#     'TAPEYEAR',
    'RESIDENC',
#     'DISP',
    'filing_year',
    'district_year'
]

target_col = 'party'

# eu.cat_heat_map(df, feature_cols)


# In[5]:


df[feature_cols]


# In[6]:




df = df[(df[target_col] == 'Republican') | (df[target_col] == 'Democratic')]


for col in feature_cols:
    if df[col].dtype.name == 'category':
        df[col] = df[col].cat.remove_unused_categories()

X = df[feature_cols]
y = df[target_col]


y = y.cat.add_categories(['1', '0'])
y[y == 'Democratic'] = '1'
y[y == 'Republican'] = '0'
y = y.cat.remove_unused_categories()


# In[7]:


enc = OneHotEncoder(drop = 'first')
enc.fit(X)
X_ohe = enc.transform(X).toarray()

# scaler = StandardScaler().fit(X_ohe)
# X_scaled = pd.DataFrame(
#     scaler.transform(X_ohe),
#     columns = enc.get_feature_names(feature_cols)
# )

X_scaled = pd.DataFrame(
    X_ohe,
    columns = enc.get_feature_names(feature_cols)
)

X_scaled = sm.add_constant(X_scaled)


# In[8]:


print("X scaled:", X_scaled.shape)


# In[ ]:


lin_reg = sm.OLS(list(y.astype(float)), X_scaled).fit()
lin_pvalues = lin_reg.pvalues


# In[ ]:


print("Lin p_values < 0.05:", lin_pvalues[lin_pvalues < 0.05])


# In[ ]:


print("Lin p_values > 0.05:", lin_pvalues[lin_pvalues > 0.05].shape)


# In[ ]:


def get_ohe_col_indices(ohe_cols, col_name):
    x = pd.Series(ohe_cols)
    return list(x[x.str.startswith(col_name)].index)


def get_complement_indices(n_cols, indices):
    return sorted(set(range(n_cols)) - set(indices))


# In[ ]:


sig_map = {}

for col in list(lin_pvalues[lin_pvalues < 0.05].index):
    if '_' in col:
        col_name = col.split('_')[0]
        col_value = col.split('_')[1]
        
        if 'filing_year' in col:
            col_name = 'filing_year'
            col_value = col.split('_')[2]
        
        if col_name in sig_map.keys():
            sig_map[col_name].append(col_value)
        else:
            sig_map[col_name] = [col_value]


# In[ ]:


print(sig_map)


# In[ ]:


print(lin_reg.summary())


# In[ ]:


non_control_indices = get_complement_indices(len(lin_reg.params), get_ohe_col_indices(X_scaled.columns, 'district_year'))
control_indices = get_ohe_col_indices(X_scaled.columns, 'district_year')

A = np.identity(len(lin_reg.params))
A = A[non_control_indices, :]
A = A[1:, :]
print(lin_reg.f_test(A))

A = np.identity(len(lin_reg.params))
A = A[control_indices, :]
A = A[1:, :]
print(lin_reg.f_test(A))


# In[ ]:




