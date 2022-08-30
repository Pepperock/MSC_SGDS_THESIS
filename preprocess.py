import tensorflow as tf 
from process_tool import empty_col


def dense_preprocess(df, col_name, new_col):
    df = empty_col(df, new_col, 'object')
    for row in df.iterrows():
        unp = row[1][col_name]
        df.at[row[0], new_col] = tf.keras.applications.densenet.preprocess_input(unp)
    
    return df 

def res_preprocess(df, col_name, new_col):
    df = empty_col(df, new_col, 'object')
    for row in df.iterrows():
        unp = row[1][col_name]
        df.at[row[0], new_col] = tf.keras.applications.resnet.preprocess_input(unp)
    
    return df 

def vgg16_preprocess(df, col_name, new_col):
    df = empty_col(df, new_col, 'object')
    for row in df.iterrows():
        unp = row[1][col_name]
        df.at[row[0], new_col] = tf.keras.applications.vgg16.preprocess_input(unp)
    
    return df 

def eff_preprocess(df, col_name, new_col):
    df = empty_col(df, new_col, 'object')
    for row in df.iterrows():
        unp = row[1][col_name]
        df.at[row[0], new_col] = tf.keras.applications.efficientnet.preprocess_input(unp)
    
    return df 