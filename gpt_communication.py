import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

deployment_name='ppo-35-turbo'


def getCompletion(prompt):
  # Send a completion call to generate an answer
  print('Waiting for GPT to respond...')
  response = client.completions.create(model=deployment_name, prompt=prompt, max_tokens=240) # 240 is the max per minute (request more if needed)
  return response

def generatePrompt(abstraction_path, events_executed):
  # Open abstraction
  with open(abstraction_path, 'r') as file:
    abstraction = file.read()
  prompt = abstraction
  prompt += 'Based on the execution of the following process trace, I predict the result of this trace will be undesirable:'
  for event in events_executed:
    prompt += '"' + event + '" '
  prompt += 'I am the person supervising the execution of this process. An actionable recommendation for a next step is:'

  return prompt


def getRecommendation(abstraction_path, events_executed):
  prompt = generatePrompt(abstraction_path, events_executed)
  response = getCompletion(prompt)
  print(prompt)
  return response.choices[0].text