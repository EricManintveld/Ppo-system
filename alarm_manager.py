import os
import pickle

def check_alarm(predictions, conf_threshold_dir, dataset_name, c_miss_weight, c_action_weight, c_postpone_weight=0):
    # load the optimal confidence threshold
    conf_file = os.path.join(conf_threshold_dir, "optimal_confs_%s_%s_%s_%s.pickle" % (dataset_name, c_miss_weight, c_action_weight, c_postpone_weight))

    with open(conf_file, "rb") as fin:
        conf_threshold = pickle.load(fin)['conf_threshold']

    alarm_raised = False
    traces = [] # Empty list for storing traces that trigger the alarm.

    # TODO: need to check per case_id. Now it just checks every event seperatly. 
    # Therefore adding the trace to the log multiple times if the predicted value exceeds to threshold in different steps of the trace.

    # trigger alarms according to conf_threshold
    unique_trace_ids = predictions['case:concept:name'].unique().tolist()

    for trace_id in unique_trace_ids:
        events = predictions[predictions['case:concept:name'] == trace_id]
        # Only want to check the last event in the trace.
        last_event = events.iloc[-1]
        # Check if last_event triggers the alarm.
        if last_event['prediction'] >= conf_threshold:
            # Raise alarm
            print('ALARM!!!')
            # Return the trace that triggered the alarm.
            trace_id = last_event['case:concept:name']
            trace = get_trace(trace_id, predictions)
            # Add trace to the row and break 
            traces.append(trace)
            alarm_raised = True
    return alarm_raised, traces

def get_trace(trace_id, dataframe):
    trace = dataframe[dataframe['case:concept:name'] == trace_id]
    return trace


