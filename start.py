from discovery import generate_bpmn, abstract_process_model
import os
import pickle
from extract_context import get_events
from alarm_manager import check_alarm
from realtime_simulation import simulate_realtime

from pathlib import Path

# List of file locations
event_log_path = '.\\datasets\\xes\\BPI_Challenge_2017.xes'
splitminer_output_folder = '.\\splitminer_output'
model_name = 'BPI_Challenge_2017_lgbm_model'
event_log_name = 'BPI_Challenge_2017.xes'
csv_logs_folder = ".\\datasets\\csv\\BPI_2017_unlabeled\\"
xes_logs_folder = '.\\datasets\\xes'
scoring_dataset_name = "BPI_2017_unlabeled_single_incomplete.csv"
dataset_name = 'BPI_Challenge_2017'
threshold_folder = ".\\datasets\\thresholds"
model_path = "models\\BPI_Challenge_2017_lgbm_model.pickle"
traces_folder = ".\\datasets\\csv\\BPI_2017_unlabeled\\realtime_traces\\"

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

# Check if model exists
if Path(model_path).exists():
    # Load trained model
    with open(model_path, 'rb') as pickle_file:
        model = pickle.load(pickle_file)

else:
    # Train model
    print('No model found!')
    exit()

# Select a threshold, according to the results of the paper a threshold of 5 to 1 would make sense.
# Assumption: threshold ratio of 5 to 1.
# Raise the alarm when an intervention has to be taken.
cost_undesired_outcome = 5
cost_intervention = 1
#alarm_triggered, problem_traces = check_alarm(predictions, threshold_folder, dataset_name, cost_undesired_outcome, cost_intervention)
# OUTPUT: Alarm decision & rows of executed action before alarm was raised.
# For extra context it might be good to include more information like the height of the fine etc. (not only the executed events)

# events_executed is now a list of dataframes.

### MODULE 4 ###
# Combine the outputs from the first 3 modules into a prompt for the LLM.
simulate_realtime(
    traces_folder=traces_folder,
    conf_threshold_dir= threshold_folder,
    dataset_name=dataset_name,
    c_miss_weight=cost_undesired_outcome,
    c_action_weight=cost_undesired_outcome,
    c_postpone_weight=cost_intervention,
    abstraction_path=abstraction_path,
    model=model
)


