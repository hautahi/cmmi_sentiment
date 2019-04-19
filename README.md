# CMMI Sentiment Analysis

This code runs three types of sentiment analysis on public comment data.

- `functions.py` defines all the necessary functions.

- `run_swn_vader.py` runs the lexicon-based swn and vader algorithms and saves the sentiment score in two different files within the `output` folder.

- `run_googleapi.py` runs the pre-trained model available via the google api. This requires an authentication json file, which should be stored in this directory and called `mycreds.json`.

- `CMS-2018-0132.csv` is the input data of 500 public comments.
