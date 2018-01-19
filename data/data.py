# Neven Recchia 27968018

# NOTE from VAST Challenge website: Two rows in the Sunday Mini-Challenge 1 data appear to have format errors (lines 4332994 and 10932427).
# NOTE: Attraction 62: Liggement Fix-me-up is positioned in Entry Corridor, but only accessible from Tundra Land. Therefore it is grouped under Tundra Land.
# NOTE: Attraction 32: Raptor Race is positioned in Coaster Alley, but only accessible from Wet Land. Therefore, it is grouped under Wet Land.
# NOTE: [X: 42,60,67, Y: 37] is the viewing area for the water rapids ride. Therefore, I added entries and a fake mapid to the attraction list for these locations.
# NOTE: Friday: There are 3557 IDs who checkin at least once.

import csv
import numpy as np
import pandas as pd


# read in park movement data
move = pd.read_csv('park-movement-Fri-FIXED-2.0.csv')

# select all rows with check-ins
move2 = move[move.type == 'check-in']

# print out full checkin data
print('printing inital checkin csv')
move2.to_csv('checkin.csv', index = False)




# read in the check-ins file
check = pd.read_csv('checkin.csv', encoding = 'ISO-8859-1')

# count check-ins grouped by id
g = check.groupby('id')
check = check.set_index('id')
check['chkcount'] = g.size()
check = check.reset_index()

# output check-in counts by id to file
print('printing checkin csv with count added')
check.to_csv('checkinct.csv', index = False)




# read in the updated check-ins file
check2 = pd.read_csv('checkinct.csv', encoding = 'ISO-8859-1')

# extract the first row of each id
check2 = check2.groupby('id').first().reset_index()

# iterates through and counts the size of each group by matching timestamp, check-in counts, x position, and y position
for index, row in check2.iterrows():
	check2['gsize'] = check2.groupby(['Timestamp', 'chkcount','X','Y'])['Timestamp'].transform('count')

# output check-in counts and group sizes to file
print('printing checkin csv with count and group size')
check2.to_csv('checkingsize.csv', index = False)




# # read in the updated check-ins file
# check3 = pd.read_csv('checkingsize.csv', encoding = 'ISO-8859-1')

# # iterate through and calculate the number of groups for each group size
# for index, row in check3.iterrows():
# 	check3['ngroup'] = check3.groupby(['gsize'])['chkcount'].transform('count') / check3['gsize']
# 	check3['ngroup'] = check3['ngroup'].astype(int)

# # output check-in counts, group size, and number of groups
# print('printing checkin csv with count added')
# check3.to_csv('checkinfull.csv', index = False)




# read in attractions and friday movements csv
attr = pd.read_csv('AttractionList.csv', encoding = 'ISO-8859-1')

# read in the updated check-ins file
checkin = pd.read_csv('checkingsize.csv', encoding = 'ISO-8859-1')
# drop columns for merge
checkin = checkin.drop(checkin.columns[[1,3,4]], axis = 1)

# merge tables
friday = pd.merge(left = move, right = checkin, how = 'inner', on = ['id','type'])
friday = pd.merge(left = friday, right = attr, how = 'left', on = ['X','Y'])

friday['hour'] = pd.DatetimeIndex(friday['Timestamp']).hour

friday = friday.drop(friday.columns[0], axis = 1)

# output merged friday csv
print('printing friday csv')
friday.to_csv('fridaychk.csv', index = False)