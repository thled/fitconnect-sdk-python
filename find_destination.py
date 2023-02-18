from read_config import read_config_multi_environment
from fitconnect import FITConnectClient, Environment
import argparse
import json
import logging
import sys

# parse command line arguments
parser = argparse.ArgumentParser(
                    prog = 'find_destination',
                    description = 'This script uses sender clients to check if a destination exists in any FIT-Connect environment')

parser.add_argument('-c', '--config', help='Path to config file', default='conf/find_destination.yaml')
parser.add_argument('destination_id', help='The destination that is being searched for')

args = parser.parse_args()

# configure logging. Uncomment to enable logging. Python's default logging level
# is WARN.
logging.basicConfig()
logging.getLogger('fitconnect').level = logging.INFO

# read config_file
config = read_config_multi_environment(args.config)

# Run through all environments read from the configuration file
for environment in config['environments']:
    # initialize SDK for specific environment (insecure=True to allow access to staging/prod)
    fitc = FITConnectClient(Environment[environment], config['environments'][environment]['client_id'], config['environments'][environment]['client_secret'], insecure=True)

    # query destinaton and collect response
    response = fitc.get_destination(args.destination_id)
    # get status
    status = response.ok
    # get status_code
    statusCode = response.status_code

    # convert response content into a JSON
    if statusCode != 503: # run only if service available
        jsonValue = json.loads(response.content.decode())
        if status == True:
            print(f"Environment {environment}: Destination {jsonValue['destinationId']} is {jsonValue['status']}.")
        elif status == False:
            print (f"Environment {environment}: {jsonValue['detail']}.")
    else:
        print(f"Environment {client}: Service not available.")
