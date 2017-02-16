
# coding: utf-8

# In[1]:

# Import Pandas for data analysis
from pandas import Series, DataFrame
import pandas as pd


# In[2]:

# Download BP statistical review 2016
get_ipython().system("wget -c 'http://www.bp.com/content/dam/bp/excel/energy-economics/statistical-review-2016/bp-statistical-review-of-world-energy-2016-workbook.xlsx'")


# In[2]:

# Load BP statistical review 2016 Excel-workbook
file_bpstat = pd.ExcelFile('bp-statistical-review-of-world-energy-2016-workbook.xlsx')


# In[3]:

# Get table: Oil-prices 1861-2015 in US dollars per barrel
table_oilprice = file_bpstat.parse('Oil - Crude prices since 1861', header=1, skiprows=2).set_index('Year').dropna()
table_oilprice.index.name = 'year'


# In[4]:

# Examine table
table_oilprice


# In[5]:

# Conversion factors for barrel of crude oil to litres and kWh
L_per_barrel = 158.987
kWh_per_barrel = 1628.2


# In[6]:

# Create a data series of oil-price per litre
oilprice_per_L = table_oilprice['$ 2015'] / L_per_barrel
oilprice_per_L.name = 'dollars_per_L_2015'


# In[7]:

# Export data to CSV
oilprice_per_L.to_csv('crude-oil-price-inflation-corrected.csv', sep='\t', header=True)


# In[9]:

# Switch to inline plotting
get_ipython().magic('pylab inline')


# In[10]:

# Load matplotlib for data plotting/exploration
import matplotlib
matplotlib.style.use('ggplot')
import matplotlib.pyplot as plt


# In[11]:

# Plot oil-price per litre, in 2015 US dollars
oilprice_plot = oilprice_per_L.plot()
oilprice_plot.set_ylabel('2015 US dollars per litre')


# In[12]:

# Global oil price in real US dollars per kWh
oilprice_per_kWh = table_oilprice['$ money of the day'] / kWh_per_barrel
oilprice_per_kWh.name = 'crude oil ($ per kWh)'


# In[13]:

# Gas prices are a bit more complicated, as there seems to be no measure that accurately reflects historical global prices
# See: http://www.bp.com/en/global/corporate/energy-economics/statistical-review-of-world-energy/natural-gas/natural-gas-prices.html
# I will use the Henry Hub price in US dollars per million BTU, which seems to reflect US gas prices (but not necessarily global ones)

table_gasprice = file_bpstat.parse('Gas - Prices ', header=1, skiprows=2, na_values='-',index_col=0)
table_gasprice.index.name = 'year'
gasprice_US_per_MBTU = pd.to_numeric(table_gasprice['US'], errors='coerce').dropna()


# In[14]:

# Conversion factor for million BTU to kWh
kWh_per_MBTU = 293.07107


# In[15]:

# US natural gas price in US dollars per kWh 
gasprice_US_per_kWh = gasprice_US_per_MBTU / kWh_per_MBTU
gasprice_US_per_kWh.name = 'US natural gas ($ per kWh)'


# In[16]:

# Coal prices are also not standardized globally, so I will use the US Central Appalachian coal spot price index

table_coalprice = file_bpstat.parse('Coal - Prices', header=1, skiprows=0, na_values='-',index_col=0)
table_coalprice.index.name = 'year'
coalprice_US_per_tonne = table_coalprice['US Central Appalachian coal spot price index ‡'].dropna()


# In[17]:

# Conversion factor for tonne to kWh
# This figure assumes an average heat content of 20.5 million BTU per tonne of coal used in the US in the period 1987-2015
# Source: EIA Monthly Energy Review, January 2017, appendix A5, http://www.eia.gov/totalenergy/data/monthly/#appendices
# Source data in Excel: http://www.eia.gov/totalenergy/data/browser/xls.cfm?tbl=TA5&freq=a
kWh_per_tonne = 20.5 * kWh_per_MBTU


# In[18]:

# US coal price in US dollars per kWh 
coalprice_US_per_kWh = coalprice_US_per_tonne / kWh_per_tonne
coalprice_US_per_kWh.name = 'US coal ($ per kWh)'


# In[19]:

# Prices in US dollarcents per kWh for all three fuels in one handy table
fuelprice_cents_per_kWh = pd.DataFrame({'crude oil':oilprice_per_kWh}) * 100
fuelprice_cents_per_kWh['natural gas (US)'] = gasprice_US_per_kWh * 100
fuelprice_cents_per_kWh['coal (US)'] = coalprice_US_per_kWh * 100
fuelprice_cents_per_kWh.index = pd.to_numeric(fuelprice_cents_per_kWh.index)


# In[24]:

# Plot fuel-prices in real dollarcents per kWh
fuelprice_fig = plt.figure(figsize=(10,6), dpi=100)
fuelprice_ax = fuelprice_fig.add_subplot(1,1,1)
fuelprice_cents_per_kWh.ix[1970:].plot(ax = fuelprice_ax)
fuelprice_ax.set_ylabel('US dollarcents per kWh')


# In[25]:

# Save plot as PNG and SVG
fuelprice_fig.savefig('fuelprices-1970-2015.png')
fuelprice_fig.savefig('fuelprices-1970-2015.svg')

