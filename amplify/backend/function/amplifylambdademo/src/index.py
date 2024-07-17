import json
import boto3

# Bedrock client used to interact with APIs around models
bedrock = boto3.client(
    service_name='bedrock', 
    region_name='us-east-1'
)

bedrock_runtime = boto3.client(
     service_name='bedrock-runtime', 
     region_name='us-east-1'
)

def handler(event, context):

    model_id = "amazon.titan-text-lite-v1"
    
    print("Event is ###",event)
    prompt = json.loads(event.get('body')).get('query')

    print("the prompt is", prompt)
    # The payload to be provided to Bedrock 
    body = json.dumps(
    {
        "inputText": prompt, 
        "textGenerationConfig":{
        "maxTokenCount": 50,
        "temperature": 0.7,
        "topP": 1}
    }
    )
    
    # The actual call to retrieve an answer from the model
    response = bedrock_runtime.invoke_model(
    body=body, 
    modelId=model_id, 
    accept='application/json', 
    contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    print("response is:", response_body)
    # The response from the model now mapped to the answer
    answer = response_body['results'][0]['outputText']
    
    return {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
        'body': json.dumps({ "Answer": answer })
    }