from witwidget.notebook.visualization import WitWidget
from witwidget.notebook.visualization import WitConfigBuilder
import pandas as pd
import numpy as np
import tensorflow as tf
import functools
import train


def create_feature_spec(df, columns=None):
    feature_spec = {}
    if columns == None:
        columns = df.columns.values.tolist()
    for f in columns:
        if df[f].dtype is np.dtype(np.int64):
            feature_spec[f] = tf.io.FixedLenFeature(shape=(), dtype=tf.int64)
        elif df[f].dtype is np.dtype(np.float64):
            feature_spec[f] = tf.io.FixedLenFeature(shape=(), dtype=tf.float32)
        else:
            feature_spec[f] = tf.io.FixedLenFeature(shape=(), dtype=tf.string)
    return feature_spec


df = pd.DataFrame.from_dict(train.dataset)
print(df)

est_mobilenet_v2 = tf.keras.estimator.model_to_estimator(
    keras_model=train.network)

features_and_labels = ['images', "pitch"]
feature_spec = create_feature_spec(df, features_and_labels)

label_column = 'Over-50K'

dataset = np.load('data.npz')


def make_label_column_numeric(df, label_column, test):
    df[label_column] = np.where(test(df[label_column]), 1, 0)


def df_to_examples(df, columns=None):
    examples = []
    if columns == None:
        columns = df.columns.values.tolist()
    for index, row in df.iterrows():
        example = tf.train.Example()
        for col in columns:
            if df[col].dtype is np.dtype(np.int64):
                example.features.feature[col].int64_list.value.append(
                    int(row[col]))
            elif df[col].dtype is np.dtype(np.float64):
                example.features.feature[col].float_list.value.append(row[col])
            elif row[col] == row[col]:
                example.features.feature[col].bytes_list.value.append(
                    row[col].encode('utf-8'))
        examples.append(example)
    return examples


# Load up the test dataset
test_df = [dataset['images'], dataset['pitch']]
#make_label_column_numeric(test_df, label_column, lambda val: val == '>50K.')
test_examples = df_to_examples(test_df[0:num_datapoints])

# Setup the tool with the test examples and the trained classifier
config_builder = WitConfigBuilder(test_examples).set_estimator_and_feature_spec(
    est_mobilenet_v2, feature_spec)
WitWidget(config_builder)
