
# coding: utf-8

# In[1]:

# Import Pandas for data analysis
from pandas import Series, DataFrame
import pandas as pd


# In[2]:

# Import some custom functions for managing IEA energy data
import ieadatatools as iea
#dreload(iea)


# In[3]:

# Load IEA CO2 highlights dataset 
tables = iea.load_co2highlights()


# In[4]:

# Select data for 2014
tables_2014 = iea.select_year(tables, 2014)


# In[5]:

# Select Total Primary Energy Supply, in kWh per person per day
tpes_2014 = tables_2014['TPES_KWh_per_person_per_day']


# In[6]:

# Load Human Development Index data, downloaded from the UNDP: http://hdr.undp.org/en/data#
hdi = pd.read_table('Human Development Index (HDI).csv', skiprows = 1, encoding = 'iso-8859-15', sep = ',', index_col = 1)
hdi.index = hdi.index.str.strip()


# In[7]:

# Get data for 2014, drop unavailable data
hdi_2014 = hdi['2014'].dropna()


# In[8]:

# Load matplotlib for data plotting/exploration
import matplotlib
matplotlib.style.use('ggplot')
import matplotlib.pyplot as plt


# In[9]:

# Create a dataframe with TPES and HDI, only keep rows with defined values for both
data = DataFrame({'primary energy use (kWh/person/day)': tpes_2014, 'HDI': hdi_2014}).dropna()


# In[12]:

# Switch to inline plotting
get_ipython().magic('pylab inline')


# In[15]:

# Open a new matplotlib graph
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
# Scatter plot: TPES vs HDI
ax.scatter(data['primary energy use (kWh/person/day)'], data['HDI'])


# In[16]:

# Use GGPlot for pretty plotting, including country labels
from ggplot import *


# In[17]:

# Add an explicit column with country labels, GGPlot doesn't seem to use the index by default
data['Country'] = data.index


# In[18]:

# Create a scatter plot with text labels
tpes_vs_hdi = ggplot(data, aes(x = 'primary energy use (kWh/person/day)', y = 'HDI', label = 'Country')) + geom_text(check_overlap = True, size = 6) + ggtitle('Energy Use and the Human Development Index')


# In[20]:

# Save the plot as SVG
tpes_vs_hdi.save('tpes_vs_hdi_2014.svg')


# In[21]:

# Save the plot as PNG
tpes_vs_hdi.save('tpes_vs_hdi_2014.png')

