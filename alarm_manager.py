import os
import pickle
import pandas as pd

def check_alarm(predictions, conf_threshold_dir, dataset_name, c_miss_weight, c_action_weight, c_postpone_weight=0):
    # load the optimal confidence threshold
    conf_file = os.path.join(conf_threshold_dir, "optimal_confs_%s_%s_%s_%s.pickle" % (dataset_name, c_miss_weight, c_action_weight, c_postpone_weight))

    with open(conf_file, "rb") as fin:
        conf_threshold = pickle.load(fin)['conf_threshold']

    predicted_probability = predictions['prediction']

    # trigger alarms according to conf_threshold
    for event in predicted_probability:
        print(event)
        if event >= conf_threshold: # Select last row, since this is the prediction
            # Raise alarm
            print('ALARM!!!')
            return True, predictions['concept:name']
    # No need to raise the alarm 
    return False