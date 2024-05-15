import os
from model_manager import get_prediction
from data_manager import load_data
import pickle
from gpt_communication import get_recommendation
from datetime import datetime
import time

def predict_all(traces_folder, model):
    # Get list of files in the folder
    traces = []
    files = os.listdir(traces_folder)
    print('Found the following files in the folder: ')
    for file in files:
        print(file)
        # Retrieve data
        file_path = os.path.join(traces_folder, file)
        data_encoded, data = load_data(file_path)

        # Get predictions
        predictions = get_prediction(model, data_encoded, data)
        traces.append(predictions)

    return traces

def simulate_realtime(traces_folder, model, conf_threshold_dir, dataset_name, c_miss_weight, c_action_weight, c_postpone_weight, abstraction_path):
    traces = predict_all(traces_folder, model)
    for trace in traces:
        events_executed = []
        for event in traces.index:
            events_executed.append(event['concept:name'])
            # if proba is higher than threshold
            # Load conf threshold
            conf_file = os.path.join(conf_threshold_dir, "optimal_confs_%s_%s_%s_%s.pickle" % (dataset_name, c_miss_weight, c_action_weight, c_postpone_weight))
            with open(conf_file, "rb") as fin:
                conf_threshold = pickle.load(fin)['conf_threshold']

            print('conf_threshold = ' + str(conf_threshold))

            if event['prediction'] >= conf_threshold:
                print('ALARM!!!!!')
                # GPT
                recommendation = get_recommendation(abstraction_path, events_executed) # Find the events that were executed in the trace
                # exit
                recommendation_output_dir = ".\\recommendations"
                current_time = str(datetime.now()).replace(" ", "_").replace(".", "_").replace(":", "_")
                
                file_name = 'recommendation_' + str(current_time)
                file_path = os.path.join(recommendation_output_dir, file_name + '.txt')
                output = str(trace) + "Response: " + str(recommendation)
                with open(file_path, 'wb') as outfile:
                    outfile.write(output)
                    outfile.close()
                # Wait one and a half minute to reset the tokens
                print('Waiting 90 seconds to reset tokens.')
                time.sleep(90)
                print('Proceeding...')
                break
