import os
from model_manager import get_prediction
from data_manager import load_data
import pickle
from gpt_communication import get_recommendation
from datetime import datetime
import time
from random import sample
import random

def predict_all(traces_folder, model):
    # Get list of files in the folder
    traces = []
    files = os.listdir(traces_folder)
    print('Found the following files in the folder: ')
    for file in files:
        # Retrieve data
        file_path = os.path.join(traces_folder, file)
        data_encoded, data = load_data(file_path)

        # Remove a random number of rows to simulate a running process trace.
        trace_length, num_cols = data_encoded.shape
        random_number = random.randint(1,trace_length-1)
        print('Random number is: ' + str(random_number))
        print('Before removing events: ' + str(data_encoded.shape))
        print(type(data_encoded))
        data_encoded = data_encoded[:-random_number]
        data = data[:-random_number]
        print('After removing events: ' + str(data_encoded.shape))

        # Get predictions
        predictions = get_prediction(model, data_encoded, data)
        traces.append(predictions)

    return traces


def simulate_realtime(traces_folder, model, conf_threshold_dir, abstraction_path):
    traces = predict_all(traces_folder, model)
    for trace in traces:
        events_executed = []
        for index, event in trace.iterrows():
            events_executed.append(event['concept:name'])
            # Load conf threshold
            conf_threshold = load_threshold(conf_threshold_dir)
            print('conf_threshold = ' + str(conf_threshold))

            conf_threshold = 0.7 # For testing
            if event['prediction'] >= conf_threshold:
                raise_alarm(conf_threshold, events_executed, abstraction_path, trace)
                break


def simulate_realtime_last(traces_folder, model, conf_threshold_dir, abstraction_path):
    traces = predict_all(traces_folder, model)
    # Load conf_threshold
    conf_threshold = load_threshold(conf_threshold_dir)
    conf_threshold = 0.7 # For testing

    # Now check for every trace is the alarm should be triggered.
    for trace in traces:
        # Check the predicted probability of the last row
        last_row = trace.iloc[-1]
        if last_row['prediction'] >= conf_threshold:
            events_executed = []
            for index, event in trace.iterrows():
                events_executed.append(str(event['Action']) + ": " + str(event['concept:name']))
            # Raise the alarm
            raise_alarm(conf_threshold, events_executed, abstraction_path, trace)


def export_random_traces(data, traces_folder):
    # trace = dataframe[dataframe['case:concept:name'] == trace_id]

    # First get all unique ids in the dataset
    unique_trace_ids = data['case:concept:name'].unique().tolist()
    random_trace_ids_sample = sample(unique_trace_ids, 10)

    for trace_id in random_trace_ids_sample:
        trace = data[data['case:concept:name'] == trace_id]
        # Export to csv
        file_path = os.path.join(traces_folder, 'trace_' + str(trace_id) + '.csv')
        trace.to_csv(file_path, index=False)

def load_threshold(conf_threshold_dir):
    # Load conf threshold
    conf_file = os.path.join(conf_threshold_dir, "optimal_confs_BPI_Challenge_2017_5_1_0.pickle") # Hardcoded to 5 1 0
    with open(conf_file, "rb") as fin:
        conf_threshold = pickle.load(fin)['conf_threshold']
    return conf_threshold


# Raises the alarm by contacting the GPT and saving its output in the recommendations folder
def raise_alarm(conf_threshold, events_executed, abstraction_path, trace):
    print('ALARM!!!!!')
    recommendation = get_recommendation(abstraction_path, events_executed) # Find the events that were executed in the trace
    recommendation_output_dir = ".\\recommendations"
    current_time = str(datetime.now()).replace(" ", "_").replace(".", "_").replace(":", "_")
    
    file_name = 'recommendation_' + str(current_time)
    file_path = os.path.join(recommendation_output_dir, file_name + '.txt')
    output = str(trace) + '\nconf_threshold: ' + str(conf_threshold) + "\n" + str(events_executed) + "\n\nResponse: " + str(recommendation)
    with open(file_path, 'w') as outfile:
        outfile.write(output)
        outfile.close()
    # Wait to reset tokens
    print('Waiting 15 seconds to reset tokens.')
    time.sleep(15)
    print('Proceeding...')

