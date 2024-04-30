from discovery import generate_bpmn, abstract_process_model
import os
import pickle
from data_manager import load_data
from model_manager import make_prediction

### MODULE 1 ###
# Generate process model using split miner.
event_log_path = '.\\datasets\\xes\\Road_Traffic_Fine_Management_Process.xes'
output_folder = '.\\splitminer_output'
model_name = 'traffic-fine-model'

output_path = os.path.join(output_folder, model_name)
generate_bpmn(event_log_path, output_path)
# Convert process model to natural language using pm4py.
abstraction_path = abstract_process_model(output_path + '.bpmn', output_folder, model_name)

### MODULE 2 ###
# Extract context from process model by showing LLM the different possible actions.
# OUTPUT: Context to be fed into the LLM

### MODULE 3 ###
# Run the alarm system on incoming datapoints.
# Load trained model
with open("models\\traffic_fine_model.pkl", 'rb') as pickle_file:
    model = pickle.load(pickle_file)

# Retrieve data
data_folder = ".\\datasets\\csv\\"
dataset_name = "TrafficFinesUnlabeled_1.csv"
data_path = os.path.join(data_folder, dataset_name)
#data = load_data("C:\\Users\\eric.manintveld\\OneDrive - Avanade\\Thesis\\Datasets\\Road Traffic Fine Management Process_1_all\\Road_Traffic_Fine_Management_Process_labeled_cleaned.csv")
data = load_data(data_path)

# Get predictions
result = make_prediction(model, data)
print(result)


# Raise the alarm when an intervention has to be taken.
# OUTPUT: Moment of intervention & the trace that has to be analyzed.

### MODULE 4 ###
# Combine the outputs from the first 3 modules into a prompt for the LLM.