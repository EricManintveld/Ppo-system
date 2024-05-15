import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment_name='ppo-35-turbo'


def get_completion(prompt):
  # Send a completion call to generate an answer
  print('Waiting for GPT to respond...')
  response = client.completions.create(model=deployment_name, prompt=prompt, max_tokens=240) # 240 is the max per minute (request more if needed)
  return response

def generate_prompt(abstraction_path, events_executed):
  # Open abstraction
  with open(abstraction_path, 'r') as file:
    abstraction = file.read()
  prompt = abstraction
  prompt += 'Based on the execution of the following process trace, I predict the result of this trace will be undesirable:'
  for event in events_executed:
    prompt += '"' + event + '" '
  prompt += 'I am the person supervising the execution of this process. An actionable recommendation for a next step is:'

  return prompt


def get_recommendation(abstraction_path, events_executed):
  prompt = generate_chat_prompt(abstraction_path, events_executed)
  response = get_chat_completion(prompt)
  return response.choices[0].message.content

def get_chat_completion(prompt):
  print('Temperature = 0.3, waiting for response...')
  response = client.chat.completions.create(
    model=deployment_name,
    messages=prompt,
    max_tokens=240,
    temperature=0.3,
  )
  return response

def generate_chat_prompt(abstraction_path, events_executed):
  prompt = []

  # Open abstraction
  with open(abstraction_path, 'r') as file:
    abstraction = file.read()

  # Create system message
  content = "Assistant is an intelligent chatbot designed to help executors of a process find an actionable recommendation to improve the outcome of the process. The recommendation should be applied during day-to-day process executions. The process executor does not have the authority to make large changes to the overall structure of the process. The executor is able to contact the customer."
  content += "The process in question is decribed by the following petri net: " + str(abstraction)
  
  system_message = {"role": "system", "content": content}
  prompt.append(system_message)

  # Create user example message
  event_trace_example = "A_Create_Application -> A_Submitted -> W_Handle leads -> A_Concept -> Accepted -> O_CreateOffer -> O_Created -> O_Sent (online only)"
  user_example_message_content = "Without intervention, the following active process trace will end in a negative outcome:  " + event_trace_example + ". Please give me an actionable recommendation to improve the outcome of this process."
  user_example_message = {"role": "user", "content":user_example_message_content}
  prompt.append(user_example_message)

  # Create example assistent message
  assistent_example_message_content = 'Send an e-mail to the customer to inform them about the current status of the application.'
  assistent_example_message = {"role": "assistant", "content": assistent_example_message_content}
  prompt.append(assistent_example_message)

  # Create actual message we want to get a response on 
  event_trace_natural_language = ""
  for event in events_executed:
    event_trace_natural_language += str(event) + " -> "
  # Remove last arrow
  event_trace_natural_language = event_trace_natural_language[:-4]

  user_message_content = "Without intervention, the following active process trace will end in a negative outcome:  " + event_trace_natural_language + ". Please give me an actionable recommendation to improve the outcome of this process."
  user_message = {"role": "user", "content":user_message_content}
  prompt.append(user_message)

  return prompt