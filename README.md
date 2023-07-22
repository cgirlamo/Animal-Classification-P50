# Animal-Classification-P50

This Repository is a home for code and procedures related to the classification of animal behavior utilizing UNM's Center for Advanced Computing Resources (CARC) system.

Code is contributed by Zhuoming Liu and Chris Girlamo



Supervised HMM.ipynb (Author: Chris Girlamo):
Inputs: 
- Csv file containing accelerometer data with observationally labelled data for a portion of the dataset
This jupyter notebook utilizes training data to run a supervised Hidden Markov Model. When running the entire process, this script should be ran first. The input is GPS and accelerometer data cleaned using Zhuoming Liu's method.This script results in a csv file containing the classifications for each accelerometer reading.


Unsupervised HMM Process.ipynb (Author: Chris Girlamo):
Inputs: csv file containing accelerometer data
This jupyter notebook utilizes the entire input dataset to train an unsupervised Hidden Markov Model. When running the entire process, this script should be ran first. The input is GPS and accelerometer Data cleaned using Zhuoming Liu's method. This script results in a csv file containing the classifications for each accelerometer reading.

The Supersized and Unsupervised HMM scripts can be run concurrently, and the results of both scripts can be utilzed in the following scripts

Classification Rate (Supervised).ipynb (Author: Chris Girlamo):
Inputs:
- Shapefile containing GPS data cleaned using Zhouming Liu's method
- Csv file output from either the supervised or unsupervised HMM script
This script utilizes the classifications resulting from either a supervised or unsupervised Hidden Markov Model. It splits the acceleromter classifications into the same timing as the GPS intervals, and then calculates a rate using the formula (classifications of one category)/(total Number of classifications). This script results in a shapefile containing the classification rate of active and inactive behaviors

Fuzzy Reclassification.ipynb (Author: Chris Girlamo)
Inputs:
- Shapefile output from the classification rate tool
This script utilizes fuzzy logic defined in Chris Girlamo's Thesis to determine High activity, low activity, and resting fuzzy membership utilzing GPS speed and the classification rate of active behavior for each point.

Cumulative Exposure.py (Author Zhuoming Liu (Revised by Chris Girlamo))
*** Warning - this script should only be run using a high powered computing system such as UNM's CARC wheeler virtual machine. This script may still take several hours to run with larger datasets, and the user should be prepared for this. 
Inputs:
- Shapefile output from fuzzy reclassification tool
- Potential for Exposure to AUM waste surface generated through GIS-MCDA process
This script utilizes methods explained in Zhuoming Liu's Thesis to calculate a cumulative exposure potential value for each day utiliziing the fuzzy classifications calculated in the script above and the results of a GIS-Multi Criteria Decision Analysis (GIS-MCDA) Model to predict the potential for exposure to AUM waste. This script was originally written by Zhuoming Liu, and was modified by Chris Girlamo to include numpy operators which reduced the processing time. 
