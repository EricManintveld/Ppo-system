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
    conf_threshold = load_threshold(conf_threshold_dir)
    traces = get_traces(traces_folder)
    for trace in traces:
        data = trace[0]
        data_encoded = trace[1]
        # Now predict line by line. Every time we move to the next line, all previous lines are included
        for index, event in enumerate(data_encoded):
            # Index starts at 0 for first event
            # Create a slice 'index' long from data_encoded and run the prediction model
            number_of_events = index + 1
            events_to_analyze_encoded = data_encoded[:number_of_events]
            events_to_analyze_regular = data[:number_of_events]
            # Run prediction
            predictions = get_prediction(model, events_to_analyze_encoded, events_to_analyze_regular)
            # Check if the last prediction in the predictions dataframe is larger than the conf_threshold
            last_row = predictions.iloc[-1]
            if last_row['prediction'] >= conf_threshold:
                # Activate the LLM and break 
                # (Assumption: After intervening once, the process will end in a desirable outcome. 
                # Because if we run again once new data is available, we should trigger at the same event again, not the new one)
                events_executed = predictions['concept:name'].to_list()
                raise_alarm(conf_threshold, events_executed, abstraction_path, predictions)
                break


def export_random_traces(data, traces_folder):
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
    conf_file = os.path.join(conf_threshold_dir, "optimal_confs_BPI_Challenge_2017_5_1_0.pickle")
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

# Returns a list of traces found in the realtime_traces folder
# The returned variable is a list of lists of data and data_encoded, which are dataframes
def get_traces(traces_folder):
    traces = []
    files = os.listdir(traces_folder)
    for file in files:
        # Retrieve data
        file_path = os.path.join(traces_folder, file)
        data_encoded, data = load_data(file_path)
        trace = [data, data_encoded]
        traces.append(trace)
    return traces

