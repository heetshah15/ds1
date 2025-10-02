import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv', index_col='Year')

    # Create scatter plot
    plt.scatter(df.index, df['CSIRO Adjusted Sea Level'])

    # Create first line of best fit
    lr = linregress(df.index, df['CSIRO Adjusted Sea Level'])
    slope, intercept = lr.slope, lr.intercept
    x_range = pd.Series(range(df.index.min(), 2051))
    plt.plot(x_range, intercept + slope * x_range, 'r', label='Line of Best Fit')

    # Create second line of best fit
    df_2000 = df[df.index >= 2000]
    lr2 = linregress(df_2000.index, df_2000['CSIRO Adjusted Sea Level'])
    slope2, intercept2 = lr2.slope, lr2.intercept
    x_range2 = pd.Series(range(2000, 2051))
    plt.plot(x_range2, intercept2 + slope2 * x_range2, 'g', label='2000 Onwards')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()