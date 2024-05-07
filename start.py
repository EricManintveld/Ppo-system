from discovery import generate_bpmn, abstract_process_model
import os
import pickle
from data_manager import load_data
from model_manager import get_prediction
from extract_context import get_events
from alarm_manager import check_alarm
from gpt_communication import getRecommendation

# This list of variables can be refactored
# List of file locations
event_log_path = '.\\datasets\\xes\\Road_Traffic_Fine_Management_Process.xes'
splitminer_output_folder = '.\\splitminer_output'
model_name = 'traffic-fine-model'
event_log_name = 'Road_Traffic_Fine_Management_Process.xes'
csv_logs_folder = ".\\datasets\\csv\\"
xes_logs_folder = '.\\datasets\\xes'
scoring_dataset_name = "TrafficFinesUnlabeled_1.csv"
dataset_name = 'Road_Traffic_Fine_Management_Process_labeled_cleaned'
threshold_folder = ".\\thresholds"

### MODULE 1 ###
# Generate process model using split miner.
output_path = os.path.join(splitminer_output_folder, model_name)
generate_bpmn(event_log_path, output_path)
# Convert process model to natural language using pm4py.
abstraction_path = abstract_process_model(output_path + '.bpmn', splitminer_output_folder, model_name)

### MODULE 2 ###
# Extract context from process model by showing LLM the different possible actions.
events = get_events(event_log_name, xes_logs_folder)

### MODULE 3 ###
# Run the alarm system on incoming datapoints.

# Load trained model
with open("models\\traffic_fine_model.pkl", 'rb') as pickle_file:
    model = pickle.load(pickle_file)

# Retrieve data
data_path = os.path.join(csv_logs_folder, scoring_dataset_name)
data_encoded, data = load_data(data_path)

# Get predictions
predictions = get_prediction(model, data_encoded, data)
print("Predictions done!")
print(predictions.head())

# Select a threshold, according to the results of the paper a threshold of 5 to 1 would make sense.
# Assumption: threshold ratio of 5 to 1.
# Raise the alarm when an intervention has to be taken.
cost_undesired_outcome = 5
cost_intervention = 1
alarm_triggered, problem_traces = check_alarm(predictions, threshold_folder, dataset_name, cost_undesired_outcome, cost_intervention)
# OUTPUT: Alarm decision & rows of executed action before alarm was raised.
# For extra context it might be good to include more information like the height of the fine etc. (not only the executed events)

# events_executed is now a list of dataframes.

### MODULE 4 ###
# Combine the outputs from the first 3 modules into a prompt for the LLM.
if alarm_triggered:
    for trace in problem_traces:
        recommendation = getRecommendation(abstraction_path, trace['concept:name'])
        print("Response: " + recommendation)
