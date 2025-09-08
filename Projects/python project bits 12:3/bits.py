import pandas as pd # imports
import matplotlib.pyplot as mpl
import seaborn as sb

# set up and cleaning

ds = pd.read_csv("Clean_Dataset.csv")
ds = ds.drop("Unnamed: 0", axis = 1)
ds = ds.drop_duplicates()

# Question 1: How many unique airlines are there, and what are their frequencies? (Barplot)

num_airlines = ds['airline'].nunique()
ind_airlines = ds['airline'].value_counts()
sb.barplot(x = ind_airlines.index, y = ind_airlines)
mpl.title("Frequency of flights by airline", fontsize = 14)
mpl.xlabel("Airline", fontsize = 14)
mpl.ylabel("Number of Flights", fontsize = 14)
mpl.show() 

# Question 2: What is the distribution of flight durations? (Histogram)

sb.histplot(data = ds, x = 'duration')
mpl.title("Distribution of flight durations", fontsize = 14)
mpl.xlabel("Duration", fontsize = 14)
mpl.ylabel("Number of Flights", fontsize = 14)
mpl.show()

# Question 3: What are the average flight prices by airline? (Barplot)
# Average prices below:
# AirAsia       4091.072742
# Air_India    23507.019112
# GO_FIRST      5652.007595
# Indigo        5324.216303
# SpiceJet      6179.278881
# Vistara      30396.536302

avg_prices = ds.groupby('airline')['price'].mean()
sb.barplot(x = avg_prices.index, y = avg_prices)
mpl.title("Average flight prices by airline", fontsize = 14)
mpl.xlabel("Duration", fontsize = 14)
mpl.ylabel("Average Price", fontsize = 14)
mpl.show()

# Question 4: How does the number of stops impact the price of flights? (Scatterplot)
# By looking at the graph, it seems that the average price of flights with more stops is greater than those with less stops.

sb.scatterplot(data = ds, x = 'stops', y = 'price')
mpl.title("Prices of flights versus number of stops", fontsize = 14)
mpl.xlabel("Number of Stops", fontsize = 14)
mpl.ylabel("Price", fontsize = 14)
mpl.show()

# Question 5: What is the relationship between flight duration and price? (Scatterplot)
# Generally the most expensive flights have a duration between 10-20, but increasing duration after that leads to cheaper flights.

sb.scatterplot(data = ds, x = 'duration', y = 'price')
mpl.title("Flight duration versus price", fontsize = 14)
mpl.xlabel("Duration", fontsize = 14)
mpl.ylabel("Price", fontsize = 14)
mpl.show()

# Question 6: What is the average price of flights for different classes? (Barplot)
# The average price for flights taken business class is much higher than that of economy, almost 10 times as much.

avg_classes = ds.groupby('class')['price'].mean()
sb.barplot(x = avg_classes.index, y = avg_classes)
mpl.title("Average price of flights for business and economy", fontsize = 14)
mpl.xlabel("Class", fontsize = 14)
mpl.ylabel("Average Price", fontsize = 14)
mpl.show()

# Question 7: Is there any seasonal trend in flight prices based on the days left before departure? (Scatterplot)
# Flights closer to the departure date do tend to be more expensive, since the range increases on the graph with more values on the upper end closer to 0 days left.

sb.scatterplot(data = ds, x = 'days_left', y = 'price')
mpl.title("Flight prices by days left before departure", fontsize = 14)
mpl.xlabel("Days Left", fontsize = 14)
mpl.ylabel("Price", fontsize = 14)
mpl.show()

# Question 8: What is the average duration of flights for each destination city?
# Average flight durations below:
# Bangalore    12.058039
# Chennai      13.338900
# Delhi        10.513310
# Hyderabad    13.381945
# Kolkata      13.214953
# Mumbai       11.583355

avg_duration = ds.groupby('destination_city')['duration'].mean()
sb.barplot(x = avg_duration.index, y = avg_duration)
mpl.title("Average duration of flights by destination city", fontsize = 14)
mpl.xlabel("Destination City", fontsize = 14)
mpl.ylabel("Duration", fontsize = 14)
mpl.show()
print(avg_duration)
