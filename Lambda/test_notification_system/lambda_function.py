import json
import time

def test_timeout_error():
    # Default lambda function has a timeout time of 3 sec.
    time.sleep(3)
    
def test_syntax_error():
    #array = [) #Uncomment to test Syntax error
    pass
    
def test_mathematical_error():
    result = 10/0 # Division by zero error
    return result
    
def lambda_handler(event, context):
    # Uncomment functions to test notification system.
    #test_timeout_error()
    #test_mathematical_error()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

