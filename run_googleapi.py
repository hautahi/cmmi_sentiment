"""
This program runs sentiment analysis using the google api algorithm,
which is based on a pre-trained model.
"""

# Load packages
import time
from functions import clean_text, get_sentiment_score
import pandas as pd

# ----------------------
# Run Google API Analysis
# ----------------------

# Define Parameters
output_file = "./output/google_analysis.csv"

print("Running Google API Analysis ...")
start_time = time.time() 

# Read data
d = pd.read_csv("CMS-2018-0132.csv")

if os.path.isfile(output_file):
    d = pd.read_csv(output_file)
else:
    d = pd.read_csv("CMS-2018-0132.csv")
    d['score'] = ""

# Loop over comments
for index, row in d.iterrows():
    
    if row['score'] == "":
        print(index)
    
        comment = row['commentText']

        text = clean_text(comment)
        score = get_sentiment_score(text)
    
        # Add to dataframe
        row['score'] = score
        d.iloc[index]  = row

        # Print dataframe
        d.to_csv(output_file,index=False)

print("--- %s seconds ---" % (time.time() - start_time))

