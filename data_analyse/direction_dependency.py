import pandas as pd 
import numpy as np
import os
import keras_preprocessing
import random
import tensorflow as tf
import process_tool
import DLmodels
import preprocess 
from process_tool import empty_col
from process_tool import array_valid
from process_tool import read_img_sa
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import pickle 

#load trained svm models

wealth_path = './models/wealth_str_svm.sav'
safe_path = './models/safety_str_svm.sav'
lively_path = './models/lively_str_svm.sav'

wealth_svm = pickle.load(open(wealth_path, 'rb'))
lively_svm = pickle.load(open(lively_path, 'rb'))
safe_svm = pickle.load(open(safe_path, 'rb'))
headings = ['heading0', 'heading90', 'heading180', 'heading270']

#function for read imgs into df with 4 direction columns
#the img was names in the form of xxx1.jpg, xxx2.jpg, xxx3.jpg, xxx4.jpg for 4 directions

def read_img_4d(df, path):
  for row in df.iterrows():
    root_name = row[1]['id']
    for i in range(0,4):
      file_end = str(i+1) + '.jpg'
      file_name = root_name + file_end
      pic_path = path + file_name
      try:
        x = process_tool.get_image(pic_path)
        df.at[row[0], headings[i]] = tf.keras.applications.densenet.preprocess_input(x[0])
      except:
        print(root_name)



def svc_pred(df1,df2,df3,df4,svm_model):
   scaler = StandardScaler()
   df1 = scaler.fit_transform(df1)
   df2 = scaler.fit_transform(df2)
   df3 = scaler.fit_transform(df3)
   df4 = scaler.fit_transform(df4)

   pred1 = svm_model.predict(df1)
   pred2 = svm_model.predict(df2)
   pred3 = svm_model.predict(df3)
   pred4 = svm_model.predict(df4)
  
   pred1df = pd.DataFrame(pred1, columns = ['heading0_pred'])
   pred2df = pd.DataFrame(pred2, columns = ['heading90_pred'])
   pred3df = pd.DataFrame(pred3, columns = ['heading180_pred'])
   pred4df = pd.DataFrame(pred4, columns = ['heading270_pred'])
   concat_4d = pd.concat([pred1df, pred2df, pred3df, pred4df], axis = 1)

   return concat_4d


#read data to dfs
safe_4d = pd.read_csv('./direction4data/safe_4direction.csv')
wealth_4d = pd.read_csv('./direction4data/wealth_4direction.csv')
lively_4d = pd.read_csv('./direction4data/lively_4direction.csv')

safe_4d_street = empty_col(safe_4d, 'heading0', 'object')
safe_4d_street = empty_col(safe_4d_street, 'heading90', 'object')
safe_4d_street = empty_col(safe_4d_street, 'heading180', 'object')
safe_4d_street = empty_col(safe_4d_street, 'heading270', 'object')

wealth_4d_street = empty_col(wealth_4d, 'heading0', 'object')
wealth_4d_street = empty_col(wealth_4d_street, 'heading90', 'object')
wealth_4d_street = empty_col(wealth_4d_street, 'heading180', 'object')
wealth_4d_street = empty_col(wealth_4d_street, 'heading270', 'object')

lively_4d_street = empty_col(lively_4d, 'heading0', 'object')
lively_4d_street = empty_col(lively_4d_street, 'heading90', 'object')
lively_4d_street = empty_col(lively_4d_street, 'heading180', 'object')
lively_4d_street = empty_col(lively_4d_street, 'heading270', 'object')

read_img_4d(safe_4d_street, './direction4data/safe_direction/')
read_img_4d(lively_4d_street, './direction4data/lively_direction/')
read_img_4d(wealth_4d_street, './direction4data/wealth_direction/')

#safe_4d_street.to_pickle('./direction4data/safe_4d.pkl')
#wealth_4d_street.to_pickle('./direction4data/wealth_4d.pkl')
#lively_4d_street.to_pickle('./direction4data/lively_4d.pkl')

# feature tables for safety perception of 4 headings
safe0 = DLmodels.dense_tb(safe_4d_street['heading0'])
safe90 = DLmodels.dense_tb(safe_4d_street['heading90'])
safe180 = DLmodels.dense_tb(safe_4d_street['heading180'])
safe270 = DLmodels.dense_tb(safe_4d_street['heading270'])

safe_4d_pred = svc_pred(safe0, safe90, safe180, safe270, lively_svm) #class outputs for all 4 direction imgs
safe_4d_pred['class'] = 0
safe_4d_pred['class'][0:100] = 1
#use sum as indicators for num of right and wrong classification
safe_4d_pred['total_sum'] = safe_4d_pred['heading0_pred'] + safe_4d_pred['heading90_pred'] + safe_4d_pred['heading180_pred'] + safe_4d_pred['heading270_pred']
safe_dependency_tb = safe_4d_pred.groupby(['class', 'total_sum']).count() #groupby to get num of wrong classification 



# do the same for lively and wealth
lively0 = DLmodels.dense_tb(lively_4d_street['heading0'])
lively90 = DLmodels.dense_tb(lively_4d_street['heading90'])
lively180 = DLmodels.dense_tb(lively_4d_street['heading180'])
wealth270 = DLmodels.dense_tb(lively_4d_street['heading270'])

lively_4d_pred = svc_pred(lively0, lively90, lively180, lively270, lively_svm)
lively_4d_pred['class'] = 0
lively_4d_pred['class'][0:100] = 1
lively_4d_pred['total_sum'] = lively_4d_pred['heading0_pred'] + lively_4d_pred['heading90_pred'] + lively_4d_pred['heading180_pred'] + lively_4d_pred['heading270_pred']
lively_dependency_tb = lively_4d_pred.groupby(['class', 'total_sum']).count()

wealth0 = DLmodels.dense_tb(wealth_4d_street['heading0'])
wealth90 = DLmodels.dense_tb(wealth_4d_street['heading90'])
wealth180 = DLmodels.dense_tb(wealth_4d_street['heading180'])
wealth270 = DLmodels.dense_tb(wealth_4d_street['heading270'])

wealth_4d_pred = svc_pred(wealth0, wealth90, wealth180, wealth270, lively_svm)
wealth_4d_pred['class'] = 0
wealth_4d_pred['class'][0:100] = 1
wealth_4d_pred['total_sum'] = wealth_4d_pred['heading0_pred'] + wealth_4d_pred['heading90_pred'] + wealth_4d_pred['heading180_pred'] + wealth_4d_pred['heading270_pred']
wealth_dependency_tb = wealth_4d_pred.groupby(['class', 'total_sum']).count()


#save reuslts
safe_dependency_tb.to_csv("./data/safety_direction_table.csv")
wealth_dependency_tb.to_csv("./data/wealth_direction_table.csv")
lively_dependency_tb.to_csv("./data/lively_direction_table.csv")