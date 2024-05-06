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
  print('Sending a test completion job')
  response = client.completions.create(model=deployment_name, prompt=prompt, max_tokens=50)
  print(prompt+response.choices[0].text)
  return response

def generatePrompt():
  prompt = 'Write a slogan for an ice cream shop.'
  return prompt

def getRecommendation():
  prompt = generatePrompt()
  response = getCompletion(prompt)
  return response.choices[0].text