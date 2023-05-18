import json
import boto3

def lambda_handler(event, context):
  
    resource = event['requestContext']['functionArn']
    functionName = resource.split(":")[-2]
    errorMessage = event['responsePayload']['errorMessage']
    
    subject = f"Error in {functionName} Lambda Function"
    message = f"\
An error has been found in {functionName}.\n\n\
Resource: {resource}\n\n\
Error Message: {errorMessage}\n\n\
Please go back and fix any issues to prevent any delays.\

    client = boto3.client('sns')
    client.publish (
      TargetArn = "arn:aws:sns:us-east-2:842059350697:Lambda_Failure_SNS", #SNS Topic ARN
      Subject =  subject, # Subject of Email
      Message = message
    )
  
    return {
      "statusCode":200,
      "message": "Sucessfuly deployed SNS message.",
      "resource" : resource,
      "error_message": errorMessage
      #"error_type": errorType,
      #"error_trace" : errorTrace
    }
