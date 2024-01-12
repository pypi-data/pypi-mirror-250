"""
__main__.py

This script is the main entry point of the DemandGenerators application. It takes a path to a JSON file as a command-line argument. 
The JSON file is expected to contain data paths and a name for the Demand_Generators.DataGenerators() object.

The script does the following:
1. Parses the command-line argument to get the JSON file path.
2. Opens and loads the JSON file into a dictionary.
3. Uses the dictionary to create a Demand_Generators.DataGenerators() object.
4. Stores the Demand_Generators.DataGenerators() object using joblib. The name of the joblib file is taken from the "name" key in the JSON file.
"""
import argparse
import json
import joblib
from .DemandGenerators import DemandNodeSimulator as DataGenerators

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file.')
    parser.add_argument('json_file', type=str, help='Path to the JSON file')

    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        data = json.load(f)

    # generate the demand generator object using the paths to 
    # the demand profile data
    demand_generator = DataGenerators(data['paths'])

    # store it at the disignated path under the name key
    joblib.dump(demand_generator, f"{data['name']}.sav")

if __name__ == "__main__":
    main()