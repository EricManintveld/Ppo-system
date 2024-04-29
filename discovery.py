import subprocess
import time
from pathlib import Path
import pm4py
import os

# Generates a BPMN model from event logs using the split miner algorithm.
def generate_bpmn(data_path, output_path):
    #Check if the model already exists
    if Path(output_path + '.bpmn').exists():
        print('Model already exists. No need to regenerate. Using the existing model.')
        return
    else:
        command = "java -cp .\\splitminer\\sm2.jar;.\\splitminer\\lib\\* au.edu.unimelb.services.ServiceProvider SM2 %s %s 0.05" % (data_path, output_path)
        t0 = time.time()
        print("Starting Split miner.")
        subprocess.run(command) # Run the jar file
        t1 = time.time()
        time_taken = t1-t0
        print(f'Running jar is done! It took {time_taken} seconds.')

# Abstracts a BPMN process for interpretation by a llm.
def abstract_process_model(bpmn_path, output_folder, model_name):
    file_path = os.path.join(output_folder, model_name +'.txt')

    # Check if the abstraction already exists
    if Path(file_path).exists():
        print('Abstraction already exists. Using existing abstraction.')
        return file_path

    else:
        bpmn = pm4py.read.read_bpmn(bpmn_path)
        net, im, fm = pm4py.convert_to_petri_net(bpmn)
        net_abstraction = pm4py.llm.abstract_petri_net(net, im, fm)
        
        # Write abstraction to file
        output_file = open(file_path, 'a')
        output_file.write(net_abstraction)
        output_file.close()
        return file_path

