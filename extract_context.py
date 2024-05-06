from xml.dom import minidom
import os
from pathlib import Path

# dataset_name is name of the xes file.
def read_events(dataset_name, event_logs_folder):
    event_list = []
    file_path = os.path.join(event_logs_folder, dataset_name)
    
    print('Opening xes file at location: ' + str(file_path))

    # Parse the XML file
    dom_tree = minidom.parse(file_path)

    # Get the root element
    root = dom_tree.documentElement

    # Find the 'int' element with key attribute "meta_concept:named_events_total"
    target_int_elements = root.getElementsByTagName('int')

    for int_element in target_int_elements:
        if int_element.getAttribute('key') == "meta_concept:named_events_total":
            target_int_element = int_element
            # Get the child elements of the target 'int' element
            events = target_int_element.getElementsByTagName('*')

            # Save events in the list
            for event in events:
            # Access child element's key and value attributes
                key = event.getAttribute('key')
                event_list.append(key)
            break
    else:
        raise Exception('meta_concept:named_events_total not found in the xes file.')
        
    return event_list

# To save time, event lists can be saved to the disk
def save_events(events, events_file_path):
    with open(events_file_path, 'w') as fp:
        for event in events:
            # write each item on a new line
            fp.write("%s\n" % event)

def get_events(dataset_name, xes_logs_folder):
    # Check if file with events exists.
    events_file_path = os.path.join(xes_logs_folder, 'events_' + dataset_name + '.txt')
    if Path(events_file_path).exists():
        print("Existing event list found! Using the existing list.")
        # Load the events from the file
        with open(events_file_path, "r") as file:
            # Read lines and store them in a list
            events = file.readlines()
            # Remove new line symbol
            events = [event.strip() for event in events]
            return events
    else:
        events = read_events(dataset_name, xes_logs_folder)
        save_events(events, events_file_path)
        return events
        

        