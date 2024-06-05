from pathlib import Path
import os
import pickle

def get_prediction(model, data_encoded, data):
    result = model.predict(data_encoded)
    # Add results as column in dataframe
    data['prediction'] = result
    return data

def train_model():
    # Step one: Optimize classfier's (lgbm) hyperparameters.
    hyperparameters = get_hyperparameters()


    # Step two: Training the classifier
    # write_lgbm_predictions.py
    
    # Step three: Optimize the alarming threshold
    # optimize_threshold.py

def get_hyperparameters():
    # First check if optimized parameters already exist.
    hyperparameter_output_dir = 'C:/Users/eric.manintveld/OneDrive - Avanade/Thesis/Code/PPO-System/datasets/optimized_hyperparameters'
    hyperparameter_file = 'optimal_confs_BPI_Challenge_2017_5_1_0.pickle'
    hyperparameter_path = os.path.join(hyperparameter_output_dir, hyperparameter_file)
    if Path(hyperparameter_path).exists():
        print('Existing hyperparameters found. Using the existing ones.')
        # Load hyperparameters
        with open(hyperparameter_path, 'rb') as pickle_file:
            hyperparameters = pickle.load(pickle_file)

    else:
        print('No existing hyperparameters found. Generating them is not implemented yet. Implement them manually.')
        exit()

    return hyperparameters

