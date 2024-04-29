import pandas as pd
from discovery import generate_bpmn, abstract_process_model
import os

### MODULE 1 ###
# Generate process model using split miner.
event_log_path = '.\\splitminer\\repair.xes.gz'
output_folder = '.\\splitminer_output'
model_name = 'repair-model'

output_path = os.path.join(output_folder, model_name)
generate_bpmn(event_log_path, output_path)
# Convert process model to natural language using pm4py.
abstraction_path = abstract_process_model(output_path + '.bpmn', output_folder, model_name)

### MODULE 2 ###
# Run the alarm system on incoming datapoints.
# Raise the alarm when an intervention has to be taken.
# OUTPUT: Moment of intervention & the trace that has to be analyzed.

### MODULE 3 ###
# Extract context from process model by showing LLM the different possible actions.
# OUTPUT: Context to be fed into the LLM

### MODULE 4 ###
# Combine the outputs from the first 3 modules into a prompt for the LLM.