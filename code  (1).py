#!/usr/bin/env python
# coding: utf-8

# # Objective 1
# 

# Profile & QA the data
# Your first objective is to read in the AirBnB listings data, calculate basic profiling metrics, 
# change column datatypes as necessary, and filter down to only Paris Listings.

# In[1]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import chardet as ch


# # to get encoding of the file listing.csv

# In[2]:


# with open(r'E:/dataset/Listings.csv','rb') as f:
#     result=ch.detect(f.read())
#     print(result)
#  charset_normalizer===> A Python library that detects the encoding of text files. It is considered a modern and robust alternative to the chardet library.
from charset_normalizer import from_path 

# Detect encoding
result = from_path(r'E:/dataset/Listings.csv').best()
# best()====>Among the detected encodings, this method selects the one with the highest confidence score
#            Returns a CharsetMatch object containing detailed information about the detected encoding

# print(result)
print(result.encoding)  # Display the detected encoding


# # Import/Open the Listings.csv file

# In[3]:


# some notes
#  low memory =true (default value)= 1)The file is processed in smaller chunks to reduce memory usage.
#               2)Pandas guesses the data types of each column as it reads chunks.
#               3)If pandas encounters inconsistent data within a column (e.g., numbers in some rows and text in others), it may infer the column as object (a general-purpose type for strings and mixed data).
# low memory =false = 1) loads the file into memory at once, ensuring consistent column types.
#                    2)This behavior ensures better reliability at the cost of higher memory usage.
#                      3) Handling Mixed Data 
data = pd.read_csv(r'E:/dataset/Listings.csv',encoding='hp_roman8',low_memory=False,parse_dates=['host_since'])
data.head()


# In[4]:


data.info()


# # Cast any date columns as a datetime format

# In[5]:


data['host_since']=pd.to_datetime(data['host_since'])


# In[6]:


data.info()


# # Filter the data down to rows where the city is Paris, and keep only the columns ‘host_since’, ‘neighbourhood’, ‘city’, ‘accommodates’, and ‘price’

# In[7]:


filter_data=data.query("city=='Paris' ").loc[:,['host_since','neighbourhood','city','accommodates','price']]
# filter_data= data[data['city']=='Paris'] === filter_data=data.query("city=='Paris' ")
# filter_data.info()
filter_data.info()
# mov=filter_data[['host_since','neighbourhood','city','accommodates','price']]== 
# ===filter_data=data.query("city=='Paris' ").loc[:,['host_since','neighbourhood','city','accommodates','price']]
# mov.info()


# # QA the Paris listings data: check for missing values, and calculate the minimum, maximum, and average for each numeric field

# In[8]:


filter_data.isna().any()


# In[9]:


# filter_data=filter_data['host_since'].fillna('00.00.00')
filter_data.dropna(inplace=True)


# In[10]:


filter_data.isna().sum()


# In[11]:


filter_data.describe()


# In[12]:


filter_data.query("price == 0 and accommodates==0 ").count()


# # Objective 2

# Prepare the data for visualization:
# Your second objective is to produce DataFrames that will be used in visualizations 
# by aggregating and manipulating the listings data in several ways.

# # task1
# Create a table named paris_listings_neighbourhood that groups Paris listings by 'neighbourhood' 
# and calculates the mean price (sorted low to high)

# In[13]:


filter_data_neighbourhood=filter_data.groupby('neighbourhood').agg({'price':'mean'}).sort_values('price')
filter_data_neighbourhood.tail()


# # task2
# Create a table named paris_listings_accomodations, filter down to the most expensive neighborhood, 
# group by the ‘accommodations’ column, and add the mean price for each value of ‘accommodates’ 
# (sorted low to high)

# In[14]:


filter_data_accommodates=filter_data.query(" neighbourhood == 'Elysee'").groupby('accommodates').agg({'price':'mean'}).sort_values('price')
filter_data_accommodates.tail()


# # task3
# Create a table called paris_listings_over_time grouped by the ‘host_since’ year,
# and calculate the average price and count of rows representing the number of new hosts

# In[24]:


# filter_data['year']=filter_data['host_since'].dt.year
# filter_data_over_time=filter_data.groupby('year').agg({'neighbourhood':'count','price':'mean'})
# filter_data.head()
# filter_data_over_time.head()

filter_data_over_time=(filter_data.set_index('host_since').resample('y').agg({'neighbourhood':'count','price':'mean'}))
filter_data_over_time.head()


# # Objective 3
# Visualize the data and summarize findings:
# Your final objective is to build visuals to show the number of new hosts by year,
# overall average price by year and neighborhood, and average price 
# for various types of listings in Paris' most expensive neighborhood.

# # task1
# Create a horizontal bar chart of the average price by neighborhood in Paris, and make sure to add a title and change axis labels as needed

# In[33]:


import seaborn as sns
(filter_data_neighbourhood.plot.barh(title='average lisiting price by paris neghbourhood',ylabel='the price per night'    ))
#                                     xlabel="the price per night",
#                                     ylabel='neighbourhood'))
sns.despine()


# # task2
# Create a horizontal bar chart of the average price by ‘accommodates’ in Paris’ most expensive neighborhood, 
# and make sure to add a title and change axis labels as needed

# In[43]:


(filter_data_accommodates.plot(kind='barh',xlabel="price",ylabel='accommodates'))


# # task3
# Create two line charts: one showing the count of new hosts over time, and one showing average price. 
# Set the y-axis limit to 0, add a title, and change axis labels as needed

# In[63]:


filter_data[filter_data['year']==2008]
# filter_data1.info()


# In[ ]:




