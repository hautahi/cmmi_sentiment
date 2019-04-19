"""
This program runs sentiment analysis using swn and vader algorithms,
which are lexicon or rule-based algorithms
"""

# Load packages
import time
from functions import swn_polarity, vader_polarity
import pandas as pd

# ----------------------
# Run SWN Analysis
# ----------------------

print("Running SWN Analysis ...")
start_time = time.time() 

# Read data
d = pd.read_csv("CMS-2018-0132.csv")

# Loop over comments
d['score'] = ""
for index, row in d.iterrows():
    
    comment = row['commentText']
    score = swn_polarity(comment)
    
    # Add to dataframe
    row['score'] = score
    d.iloc[index]  = row

# Print dataframe
d.to_csv("./output/swn_analysis.csv",index=False)

print("--- %s seconds ---" % (time.time() - start_time))

# ----------------------
# Run Vader Analysis
# ----------------------

print("Running Vader Analysis ...")
start_time = time.time() 

# Read data
d = pd.read_csv("CMS-2018-0132.csv")

d['score'] = ""
for index, row in d.iterrows():
    
    comment = row['commentText']
    score = vader_polarity(comment)

    # Add to dataframe
    row['score'] = score
    d.iloc[index]  = row

# Print dataframe
d.to_csv("./output/vader_analysis.csv",index=False)

print("--- %s seconds ---" % (time.time() - start_time))
