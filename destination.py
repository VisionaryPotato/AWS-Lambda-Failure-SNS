import os
import sys
import json
import subprocess

if len(sys.argv) < 2:
    print("No arguments provided.")
    sys.exit()

# Access command-line arguments
DESTINATION = sys.argv[1]  # The first argument (index 1) after the script name


def checkProcess(process):
    if process.returncode != 0:
        print("Command failed!❌\n\t{process.stderr}")

def updateFunction(function):
    print(f"\t↳Destination not found. Adding failure destination: {function} -> {DESTINATION}")
    destination_arn = f"arn:aws:lambda:us-east-2:842059350697:function:{DESTINATION}"
    command = [
        "aws", "lambda", "put-function-event-invoke-config",
        "--function-name", function,
        "--region", "us-east-2",
        "--destination-config", json.dumps({"OnFailure": {"Destination": destination_arn}})
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    checkProcess(process)
    if(process.returncode == 0):
        print("\t\t↳Destination Added ✅")


def checkConfig(function):
    if DESTINATION == function:
        return

    print(f"Getting {function} Configuration...")
    command = ["aws", "lambda", "list-function-event-invoke-configs", "--function-name", function, "--no-cli-pager"]
    process = subprocess.run(command, capture_output=True, text=True)
    checkProcess(process)
    json_object = json.loads(process.stdout).get("FunctionEventInvokeConfigs")

    if not json_object:
        updateFunction(function)
    else:
       for object in json_object:
            failure_destination = object.get("DestinationConfig").get("OnFailure").get("Destination")
            if failure_destination and DESTINATION in failure_destination:
                print(f"\t↳Destination already exists.\n")
            else:
                updateFunction(function)


def getFunctions(obj):
    json_object = json.loads(obj)
    for function in json_object.get("Functions"):
        functionName = function.get("FunctionName")
        checkConfig(functionName)


def main():
    print(f"Checking Failure Destinations to {DESTINATION}\n")
    command = ["aws", "lambda", "list-functions", "--no-cli-pager"]
    process = subprocess.run(command, capture_output=True, text=True)
    checkProcess(process)

    getFunctions(process.stdout)


if __name__ == '__main__':
    main()