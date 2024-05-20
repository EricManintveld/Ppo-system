# Converts 'incoming' data into usable JSON string.

from alarmsystem.DatasetManager import DatasetManager
import numpy as np
from sklearn.pipeline import FeatureUnion
import pickle

def convert_data(raw_data):
    # read the data
    print('Starting DatasetManager')
    dataset_manager = DatasetManager(raw_data)
    print('DatasetManager started.')
    data = dataset_manager.read_dataset()
    print('Reading dataset done.')

    min_prefix_length = 1
    #max_prefix_length = int(np.ceil(data.groupby(dataset_manager.case_id_col).size().quantile(0.9))) # Original
    max_prefix_length = int(np.ceil(data.groupby(dataset_manager.case_id_col).size().quantile(0.97)))
    
    prefixes = dataset_manager.generate_prefix_data(data, min_prefix_length, max_prefix_length) 

    # Load encoder
    with open("encoders\\encoder_BPI_Challenge_2017.pickle", 'rb') as pickle_file:
        feature_combiner = pickle.load(pickle_file)
    data_encoded = feature_combiner.transform(prefixes)

    return data_encoded, data

def load_data(data_path):
    data_encoded, data = convert_data(data_path)
    return data_encoded, data