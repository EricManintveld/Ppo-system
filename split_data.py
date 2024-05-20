import pandas as pd
from sklearn.model_selection import train_test_split
from random import sample

df = pd.read_csv('.\\datasets\\csv\\BPI_2017_labeled.csv')

unique_trace_ids = df['case:concept:name'].unique().tolist()
number_of_train_samples = int(0.8 * len(unique_trace_ids))
train_trace_ids_sample = sample(unique_trace_ids, number_of_train_samples)

train_traces = []

for trace_id in train_trace_ids_sample:
        trace = df[df['case:concept:name'] == trace_id]
        train_traces.append(trace)

df_train = pd.concat(train_traces)
df_train.to_csv('.\\datasets\\csv\\BPI_2017_labeled_train.csv', index=False)

# Now grab the remaining ids
# list(set(list_2).difference(list_1))
test_trace_ids = list(set(unique_trace_ids).difference(train_trace_ids_sample))

test_traces = []

for trace_id in test_trace_ids:
        trace = df[df['case:concept:name'] == trace_id]
        test_traces.append(trace)

df_test = pd.concat(test_traces)

# Remove labels from test
df_test = df_test.drop(columns=['label'])

df_test.to_csv('.\\datasets\\csv\\BPI_2017_unlabeled_test.csv', index=False)
