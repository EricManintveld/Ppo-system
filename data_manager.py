# Converts 'incoming' data into usable JSON string.

from alarmsystem.DatasetManager import DatasetManager
import numpy as np
from sklearn.pipeline import FeatureUnion
import pickle

def convert_data(raw_data):
    calibrate = False
    split_type = "temporal"
    oversample = False
    calibration_method = "beta"

    train_ratio = 0.8
    val_ratio = 0.2

    # read the data
    print('Starting DatasetManager')
    dataset_manager = DatasetManager(raw_data)
    print('DatasetManager started.')
    data = dataset_manager.read_dataset()
    print('Reading dataset done.')
    print("Shape after reading: " + str(data.shape))

    min_prefix_length = 1
    max_prefix_length = int(np.ceil(data.groupby(dataset_manager.case_id_col).size().quantile(0.9)))
    print("Max prefix length: " + str(max_prefix_length))
    
    prefixes = dataset_manager.generate_prefix_data(data, min_prefix_length, max_prefix_length) 
    print("Shape after generating predix data: " + str(prefixes.shape))

    # Load encoder
    with open("encoders\\encoder_Road_Traffic_Fine_Management_Process_labeled_cleaned.pickle", 'rb') as pickle_file:
        feature_combiner = pickle.load(pickle_file)
    data = feature_combiner.transform(prefixes)

    print("Shape after encoding prefixes: " + str(data.shape))

    return data

def load_data(data_path):
    data = convert_data(data_path)
    return data