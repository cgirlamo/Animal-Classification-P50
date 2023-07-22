
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

df = gpd.read_file(r'802_HMMSup_FZ.shp')# Read in file
df = pd.DataFrame(df) # Make it a dataframe
df['MT Time'] = pd.to_datetime(df['MT Time']) # Make MT Time a datetime index
df = df.set_index('MT Time')

df = df.between_time('8:00:00','19:00:00') # Select only 
df = df.reset_index()
aug_df = df[df['MT Time'].dt.month == 8] # Seperate into seperate months (for some reason?)

# print(aug_df)

sep_df = df[df['MT Time'].dt.month == 9]
oct_df = df[df['MT Time'].dt.month == 10]
combination = []# Make combination - this should be fine, looked like Leos  
all_p = range(0,3**12)
for i in all_p:
    Tri = []
    quotient = int(i/3)
    remainder = i % 3
    Tri.append(remainder)
    while quotient != 0:
        remainder = quotient % 3
        Tri.append(remainder)
        quotient = int(quotient/3)
    combination.append(Tri)

# Again should be fine, looks like Leo's - no comments so no idea why this here 
comb = []
for i in combination:
    j = i[:]
    l = len(j)
    while l != 16:
        j.append(0)
        l = l + 1
    comb.append(j)
comb = comb

df = df.reset_index() # Reset the index
aug_day = 31 # Get the number of days in each month
sep_day = 30
oct_day = 31
def get_cum(df,days,month, month_val):
    newdf = pd.DataFrame(index = pd.date_range(df.loc[df.index[0],'MT Time'].date(), df.loc[df.index[-1],'MT Time'].date(),freq='1D')) # Make an empty dataframe
    newdf['s'] = None # make a column, s

    run = 0 # Running counter
    num_days = range(1,days) # list of all days in the month
    for x in num_days: # Cycle through all the days in the month
        
        print('Running day {} of {} in {}'.format(x,days, month)) # Print message
        n_df = df[df['MT Time'].dt.date == datetime.date(year = 2021,month = month_val, day = x)] # Testing df
        print(n_df.shape[0])
        if ~n_df.empty: # if test me is not empty
#             print(n_df) # print it out as a test
            if n_df.shape[0] > 11: # If the number of records is greater than 11
                print('Im wokring')
#                
                MCDA = n_df['MCDA'].to_numpy() # Pull out the MCDA and classifications, turn them into numpy arrays
                low = n_df['Low_activi'].to_numpy()
                high = n_df['High_activ'].to_numpy()
                rest = n_df['Resting'].to_numpy()
                C_r = [] # Holder lists
                C_p = []
                for i in comb[0:3**12]: # cycle through comb
                   
                    n = 0 # set n,s, and p to these specific values
                    s = 0
                    p = 1
                    for j in np.arange(0,12): # cycle through 1-12, should be the number of points in each day
#                         print(str(j))
                        if i[j] == 0: # for zero cases, 
                            s = s + MCDA[n] * 0.4 # get the mcda value
                            p = p * (low[n]/(low[n] + high[n] + rest[n])) # set this formula
                        elif i[j] == 1: # for one cases
                            s = s + MCDA[n] * 0.2 # get the mcda value
                            p = p * (rest[n]/(low[n] + high[n] + rest[n]))# set this formula
                        elif i[j] == 2: # for 2 cases
                            s = s + MCDA[n] * 0.4 # set the mcda value value
                            p = p * (high[n]/(high[n] + rest[n] + low[n])) # set this formula
                        n +=1 # n goes one higher    
                    C_r.append(s) # append s to C_r 
                    C_p.append(p) # append p to C_p
                    
#                 print(run/(3**12))
                run += 1
                c = pd.DataFrame(data = {'C_r':C_r, 'C_p':C_p})
        
        
                c['s'] = c["C_r"] * c['C_p']
            else:
                c = pd.DataFrame()
                c.loc[0,'s'] = -1
#         print(c)
        newdf.loc[pd.to_datetime(month + ' ' + str(x) + ' 2021'),'s'] = c['s'].sum()
        
    return(newdf)
oct = get_cum(oct_df, oct_day, 'October',10)
# print(oct)
# # print(oct)
aug = get_cum(aug_df, aug_day, 'August',8)
# print(aug)
sep = get_cum(sep_df, sep_day, 'September',9)
print(sep)
# df = df.set_index('MT Time')
newdf = pd.merge(oct,aug, left_index = True, right_index = True)
newdf = newdf.merge(sep, left_index = True, right_index = True)
# # df = pd.concat([oct,aug,sep])
print(df)
# df = gpd.GeoDataFrame(df, geometry = 'geometry')
# df['MT Time'] = df['MT Time'].astype('str')
newdf.to_csv(r'~\802CumExp.csv')