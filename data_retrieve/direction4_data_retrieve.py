import pandas as pd 
import numpy as np
from img_retrieve import StreetViewer_heading

# sample 100 class1 and class0
#get lat and lon for each sample
safe1 = pd.read_csv("./data/safe_high2000.csv")
safe2 = pd.read_csv("./data/safe_low.csv")
safe_sa = pd.read_csv("./data/safe_street_aerial.csv")
safe_sa2 = safe_sa[safe_sa.aerial.isna() == False]
safe_sub_sample = safe_sa2[['name','id','picid','class']]
safe_1 = safe_sub_sample[safe_sub_sample['class'] == 1].sample(100)
safe_0 = safe_sub_sample[safe_sub_sample['class'] == 0].sample(100)
safe_high = safe1[['id','lat','lon','qscore']]
safe_low = safe2[['id','lat','lon','qscore']]
safe_sample1 = pd.merge(safe_1, safe_high, left_on = 'id', right_on= 'id', how = 'left')
safe_sample0 = pd.merge(safe_0, safe_low, left_on = 'id', right_on= 'id', how = 'left')
safe_direction_sample = pd.concat([safe_sample1, safe_sample0], axis = 0)

wealth1 = pd.read_csv("./data/high_wealth.csv")
wealth2 = pd.read_csv("./data/low_wealth.csv")
wealth_sa = pd.read_pickle('./data/wealth_street_aerial.pkl') # the pickle file contain aerial and street image input 224 224 3
wealth_sa = wealth_sa[wealth_sa.aerial.isna() == False]
wealth_sub_sample = wealth_sa[['name','pic_name','picid','class']]
wealth_1 = wealth_sub_sample[wealth_sub_sample['class'] == 1].sample(100)
wealth_0 = wealth_sub_sample[wealth_sub_sample['class'] == 0].sample(100)
wealth_high = wealth1[['id','lat','lon','qscore']]
wealth_low = wealth2[['id','lat','lon','qscore']]
wealth_sample1 = pd.merge(wealth_1, wealth_high, left_on = 'name', right_on= 'id', how = 'left')
wealth_sample0 = pd.merge(wealth_0, wealth_low, left_on = 'name', right_on= 'id', how = 'left')
wealth_direction_sample = pd.concat([wealth_sample1, wealth_sample0], axis = 0)

lively1 = pd.read_csv("./data/high_lively.csv")
lively2 = pd.read_csv("./data/low_lively.csv")
lively_sa = pd.read_pickle('./data/lively_street_aerial.pkl')
lively_sa = lively_sa[lively_sa.aerial.isna() == False]
lively_sub_sample = lively_sa[['name','pic_name','picid','class']]
lively_1 = lively_sub_sample[lively_sub_sample['class'] == 1].sample(100)
lively_0 = lively_sub_sample[lively_sub_sample['class'] == 0].sample(100)
lively_high = lively1[['id','lat','lon','qscore']]
lively_low = lively2[['id','lat','lon','qscore']]
lively_sample1 = pd.merge(lively_1, lively_high, left_on = 'name', right_on= 'id', how = 'left')
lively_sample0 = pd.merge(lively_0, lively_low, left_on = 'name', right_on= 'id', how = 'left')
lively_direction_sample = pd.concat([lively_sample1, lively_sample0], axis = 0)


api_key = "" #enter your google street view api

#download 4 diretion svi for each sample
def get_direction4pic(df, name_col, topic, path):
  list1 = [0, 90, 180, 270]
  for row in df.iterrows():
    lat = row[1]['lat']
    lon = row[1]['lon']
    coords = str(lat)+','+str(lon)
    i = 0
    picname_root = row[1][name_col]
    for angle in list1:
      i += 1
      pic_name = picname_root + str(i) 
      outputs = path
      try:
          street_img = StreetViewer_heading(api_key, coords, angle, outputs, pic_name)
          street_img.get_meta()
          street_img.get_pic()
      except:
          print(row[1]['picid'])

get_direction4pic(safe_direction_sample, 'id', 'safe', './data/safe_direction/')
get_direction4pic(wealth_direction_sample, 'id', 'wealth', './data/wealth_direction/')
get_direction4pic(lively_direction_sample, 'id', 'lively', './data/lively_direction/')
