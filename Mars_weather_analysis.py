# %% [markdown]
# # Module 12 Challenge
# ## Deliverable 2: Scrape and Analyze Mars Weather Data

# %%
# Import relevant libraries
from splinter import Browser
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import datetime

# %%
browser = Browser('chrome')

# %% [markdown]
# ### Step 1: Visit the Website
# 
# Use automated browsing to visit the [Mars Temperature Data Site](https://static.bc-edx.com/data/web/mars_facts/temperature.html). Inspect the page to identify which elements to scrape.
# 
#    > **Hint** To identify which elements to scrape, you might want to inspect the page by using Chrome DevTools to discover whether the table contains usable classes.
# 

# %%
# Visit the website
# https://static.bc-edx.com/data/web/mars_facts/temperature.html
url = "https://static.bc-edx.com/data/web/mars_facts/temperature.html"
browser.visit(url)

# %% [markdown]
# ### Step 2: Scrape the Table
# 
# Create a Beautiful Soup object and use it to scrape the data in the HTML table.
# 
# Note that this can also be achieved by using the Pandas `read_html` function. However, use Beautiful Soup here to continue sharpening your web scraping skills.

# %%
# Create a Beautiful Soup Object
html=browser.html
soup = BeautifulSoup(html, 'html.parser')

# %%
# Extract all rows of data
table = soup.find('table', class_='table')

# %% [markdown]
# ### Step 3: Store the Data
# 
# Assemble the scraped data into a Pandas DataFrame. The columns should have the same headings as the table on the website. Here’s an explanation of the column headings:
# 
# * `id`: the identification number of a single transmission from the Curiosity rover
# * `terrestrial_date`: the date on Earth
# * `sol`: the number of elapsed sols (Martian days) since Curiosity landed on Mars
# * `ls`: the solar longitude
# * `month`: the Martian month
# * `min_temp`: the minimum temperature, in Celsius, of a single Martian day (sol)
# * `pressure`: The atmospheric pressure at Curiosity's location

# %% [markdown]
# https://www.freecodecamp.org/news/python-split-string-how-to-split-a-string-into-a-list-or-array-in-python/#:~:text=The%20split()%20method%20is,a%20list%20of%20these%20substrings.&text=In%20this%20example%2C%20we%20split,using%20the%20split()%20method.
# 
# checked syntax for splitting at this site

# %%
# Create an empty list
table_data = []
# Loop through the scraped data to create a list of rows
rows = table.find_all('tr', class_='data-row')
for row in rows:
    table_data.append(row.text.split())


# %%
# Create a Pandas DataFrame by using the list of rows and a list of the column names
columns = table.find('tr')
columns = columns.text.split()

Mars_temp_df = pd.DataFrame(table_data, columns=columns)

# %%
# Confirm DataFrame was created successfully
Mars_temp_df.head(50)

# %% [markdown]
# ### Step 4: Prepare Data for Analysis
# 
# Examine the data types that are currently associated with each column. If necessary, cast (or convert) the data to the appropriate `datetime`, `int`, or `float` data types.
# 
#   > **Hint** You can use the Pandas `astype` and `to_datetime` methods to accomplish this task.
# 

# %%
# Examine data type of each column
Mars_temp_df.dtypes

# %%
# Change data types for data analysis
Mars_temp_df['sol']=Mars_temp_df['sol'].astype('int64')
Mars_temp_df['ls']=Mars_temp_df['ls'].astype('int64')
Mars_temp_df['month']=Mars_temp_df['month'].astype('int64')
Mars_temp_df['min_temp']=Mars_temp_df['min_temp'].astype('float64')
Mars_temp_df['pressure']=Mars_temp_df['pressure'].astype('float64')
Mars_temp_df['terrestrial_date'] = pd.to_datetime(Mars_temp_df['terrestrial_date'])

# %%
# Confirm type changes were successful by examining data types again
Mars_temp_df.dtypes

# %% [markdown]
# ### Step 5: Analyze the Data
# 
# Analyze your dataset by using Pandas functions to answer the following questions:
# 
# 1. How many months exist on Mars?
# 2. How many Martian (and not Earth) days worth of data exist in the scraped dataset?
# 3. What are the coldest and the warmest months on Mars (at the location of Curiosity)? To answer this question:
#     * Find the average the minimum daily temperature for all of the months.
#     * Plot the results as a bar chart.
# 4. Which months have the lowest and the highest atmospheric pressure on Mars? To answer this question:
#     * Find the average the daily atmospheric pressure of all the months.
#     * Plot the results as a bar chart.
# 5. About how many terrestrial (Earth) days exist in a Martian year? To answer this question:
#     * Consider how many days elapse on Earth in the time that Mars circles the Sun once.
#     * Visually estimate the result by plotting the daily minimum temperature.
# 

# %%
# 1. How many months are there on Mars?
Mars_temp_df['month'].value_counts()


# %%
print("There are 12 months on Mars")

# %%
# 2. How many Martian days' worth of data are there?
Mars_temp_df['sol'].count()


# %%
# 3. What is the average low temperature by month?
Mars_avgs = Mars_temp_df.groupby(['month']).mean()
Mars_avgs

# %%
# Plot the average temperature by month
Mars_avgs['min_temp'].plot(kind="bar")

plt.title('Minimum Temperature by Mars Month')
plt.xlabel('Month')
plt.ylabel('Minimum Temperature')
plt.show()

# %%
# Identify the coldest and hottest months in Curiosity's location
sorted_avgs = Mars_avgs.sort_values(by='min_temp', ascending=True)
sorted_avgs['min_temp'].plot(kind='bar')
plt.title('Minimum Temperature by Mars Month in Order')
plt.xlabel('Month')
plt.ylabel('Minimum Temperature')
plt.show()

# %%
print("The coldest month is the 3rd month, and the warmest month is the 8th month.")

# %%
# 4. Average pressure by Martian month
Mars_avgs

# %%
# Plot the average pressure by month
sorted_avgP = Mars_avgs.sort_values(by='pressure', ascending=True)
sorted_avgP['pressure'].plot(kind='bar')
plt.title('Average Pressure by Mars Month in Order')
plt.xlabel('Month')
plt.ylabel('Average Pressure')
plt.show()

# %%
# 5. How many terrestrial (earth) days are there in a Martian year?

# get first date in dataset stored as a variable
first_date = Mars_temp_df['terrestrial_date'].iloc[0]
first_mars_date = Mars_temp_df['sol'].iloc[0]


#calculate number of days into the dataset into a new column of Mars_temp_df
Mars_temp_df['Earth Days Elapsed']=Mars_temp_df['terrestrial_date'] - first_date


Mars_temp_df.plot(x='sol', y='min_temp', kind='line', label=None, grid=True)

plt.title('Minimum Temperature by Earth Date')
plt.xlabel('Earth Days')
plt.ylabel('Minimum Temperature')
plt.show()


# %% [markdown]
# The peaks in temperature seem to occur with regular spacing.  Perhaps between 600 to 700 earth days.

# %%
# use loc to find only rows with min temp = -66 degrees

peak_temp_1= Mars_temp_df.loc[Mars_temp_df['min_temp']== -66,:]

peak_temp_1.head(60)

# %% [markdown]
# 774	798	2014-12-31	854	262	9	-66.0	910.0	867 days
# 1292	1318	2016-07-12	1398	184	7	-66.0	751.0	1426 days
# 
# Looks like the 2nd and 3rd peaks occur around 8oo earth days and 1500 earth days.
# 1500-800 = 700
# 
# The first peak is around 100 days .
# 800 - 100 =700   
# A round number for the earth days in a Martian year is 700

# %%
print("Based on averages, the coldest month is the 3rd month, and the warmest month is the 8th month on Mars.")

print("Again based on averages, the lowest pressures on Mars occur during the 6th month, with the highest pressures during the 9th pmonth.")

print("A Martian year is approximately 700 days long.  This is the approximate time span between temperature peaks over multiple Martian years.")

# %% [markdown]
# Atmospheric pressure is, on average, lowest in the sixth month and highest in the ninth.

# %% [markdown]
# The distance from peak to peak is roughly 1425-750, or 675 days. A year on Mars appears to be about 675 days from the plot. Internet search confirms that a Mars year is equivalent to 687 earth days.

# %% [markdown]
# ### Step 6: Save the Data
# 
# Export the DataFrame to a CSV file.

# %%
# Write the data to a CSV
Mars_temp_df.to_csv("output/marstemps.csv",index=False)

# %%
browser.quit()

# %%



