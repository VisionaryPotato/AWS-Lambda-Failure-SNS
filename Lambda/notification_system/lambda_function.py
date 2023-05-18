import json
import boto3

def lambda_handler(event, context):
  
    resource = event['requestContext']['functionArn']
    functionName = resource.split(":")[-2]
    errorMessage = event['responsePayload']['errorMessage']
    subject = f"Error in {functionName} Lambda Function"
    message = f"An error has been found in {functionName}.\n\nResource: {resource}\n\nError Message: {errorMessage}\n\nPlease go back and fix any issues to prevent any delays."

    boto3.client('sns').publish (
      TargetArn = "", # TODO: Paste SNS Topic ARN Here
      Subject =  subject,
      Message = message
    )
  
    return {
      "statusCode":200,
      "message": "Sucessfuly deployed SNS message.",
      "resource" : resource,
      "error_message": errorMessage
    }
