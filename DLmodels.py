import coatnet
import tensorflow as tf
import pandas as pd 
from tensorflow.keras.models import Sequential 
from tensorflow.keras import layers

def dense_tb(X2):
    img_width = 224
    img_height = 224
    dense_t = tf.keras.applications.DenseNet201(weights = 'imagenet', include_top = False, input_shape = (img_width, img_height, 3))
    dense_t.trainable = False

    model_t = Sequential()
    model_t.add(dense_t)
    model_t.add(layers.GlobalAveragePooling2D())

    pred_result = model_t.predict(X2)
    feature_df = pd.DataFrame(pred_result)

    return feature_df

def vgg16_tb(X2):
    img_width = 224
    img_height = 224
    vgg_t = tf.keras.applications.VGG16(weights = 'imagenet', include_top = False, input_shape = (img_width, img_height, 3))
    vgg_t.trainable = False

    vgg_model = Sequential()
    vgg_model.add(vgg_t)
    vgg_model.add(layers.GlobalAveragePooling2D())

    pred_result = vgg_model.predict(X2)
    feature_df = pd.DataFrame(pred_result)

    return feature_df


def eff_tb(X2):
    img_width = 224
    img_height = 224
    eff_t = tf.keras.applications.EfficientNetV2M(weights = 'imagenet', include_top = False, input_shape = (img_width, img_height, 3))
    eff_t.trainable = False

    eff_model = Sequential()
    eff_model.add(eff_t)
    eff_model.add(layers.GlobalAveragePooling2D())

    pred_result = eff_model.predict(X2)
    feature_df = pd.DataFrame(pred_result)

    return feature_df

def res_tb(X2):
    img_width = 224
    img_height = 224
    res_t = tf.keras.applications.ResNet50(weights = 'imagenet', include_top = False, input_shape = (img_width, img_height, 3))
    res_t.trainable = False

    res_model = Sequential()
    res_model.add(res_t)
    res_model.add(layers.GlobalAveragePooling2D())

    pred_result = res_model.predict(X2)
    feature_df = pd.DataFrame(pred_result)

    return feature_df


def coat_tb(X2):
    img_width = 224
    img_height = 224
    coat_t = coatnet.coatnet7(include_top = False, input_shape = (img_width, img_height, 3))
    coat_t.trainable = False

    coat_model = Sequential()
    coat_model.add(coat_t)
    coat_model.add(layers.GlobalAveragePooling2D())

    pred_result = coat_model.predict(X2)
    feature_df = pd.DataFrame(pred_result)

    return feature_df