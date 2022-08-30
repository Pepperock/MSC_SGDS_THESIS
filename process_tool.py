import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image 
import pandas as pd 
def empty_col(df, col_name, col_type):
    df[col_name] = np.nan
    df[col_name] = df[col_name].astype(col_type)
    
    return df


def name_to_num(df, col_name, symbol, new_col):
    list0 = []
    for row in df.iterrows():
        name1 = str(row[1][col_name])
        id = name1.split(symbol)[0]
        #list[0].append(id)
        df.at[row[0], new_col] = id
    return df


def num_to_name(df, col, new_col):
    df[new_col] = np.nan
    df[new_col] = df[new_col].astype('string')
    for row in df.iterrows():
        num_name = row[1][col]
        val = str(num_name) + '.jpg'
        df.at[row[0], new_col] = val
    return df 

def array_valid(series1):
    series2 = series1.tolist()
    series3 = np.array(series2)
    return series3

def find_digit(list0):
    ans = []
    for element in list0:
        ss = ''
        for character in element:
            if character.isdigit():
                ss = ss + character
        ans.append(ss)
    return ans 

def get_image(path):
    img = image.load_img(path, target_size = (224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    return x 

def create_str_aer_tb(list1):
    names = list1
    df = pd.DataFrame(names, columns = ['name'])
    df = empty_col(df, 'street', 'object')
    df = empty_col(df, 'aerial', 'object')

    return df

def create_street_tb(list1):
    names = list1
    df = pd.DataFrame(names, columns = ['name'])
    df = empty_col(df, 'street', 'object')
    return df

def read_img_sa(df, path_street, path_aerial):
    for i in df.iterrows():
        x = get_image(path_street + str(i[1]['name']))
        df.at[i[0], 'street'] = x[0]
        x = get_image(path_aerial + str(i[1]['name']))
        df.at[i[0], 'aerial'] = x[0]
    return df 

def read_img_street(df, path_street, name_col):
    for i in df.iterrows():
        try:
            x = get_image(path_street + str(i[1][name_col]))
            df.at[i[0], 'street'] = x[0]
        except:
            print(str(i[1][name_col]))
    return df 

def dense_preprocess(df, col_name, new_col):
    df = empty_col(df, new_col, 'object')
    for row in df.iterrows():
        unp = row[1][col_name]
        df.at[row[0], new_col] = tf.keras.applications.densenet.preprocess_input(unp)
    
    return df 




