# First import the two 'datasets'
import pandas as pd
from data_manager import load_data
from model_manager import get_prediction
import pickle
from pathlib import Path

model_path = "models\\BPI_Challenge_2017_lgbm_model.pickle"

# Check if model exists
if Path(model_path).exists():
    # Load trained model
    with open(model_path, 'rb') as pickle_file:
        model = pickle.load(pickle_file)

else:
    # Train model
    print('No model found!')
    exit()


data_regular_encoded, data_regular = load_data('.\\datasets\\csv\\test\\BPI_first_regular.csv')
data_deviant_encoded, data_deviant = load_data('.\\datasets\\csv\\test\\BPI_first_regular.csv')

predictions_regular = get_prediction(model, data_regular_encoded, data_deviant)
predictions_deviant = get_prediction(model, data_deviant_encoded, data_deviant)

print ('Regular:')
print(predictions_regular.head(1))
print('Deviant:')
print(predictions_deviant.head(1))

