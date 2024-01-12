"""
__main__.py

This script is the main entry point of the application. It checks if a CSV file path is provided as a command line argument, 
and then checks if the file exists. The CSV file is expected to contain data for the PVGenerators module.

Author: Gerald Jones
Email: gjones2@vols.utk.edu
Creation Date: 2024-01-07
Last Edited: 2024-01-07
"""
import argparse
import json
import pandas as pd
import joblib
import time
from .PVGenerators import MonthlyHourlyPVGenerator as PVGenerator

def main():
    parser = argparse.ArgumentParser(description='Process a JSON file.')
    parser.add_argument('json_file', type=str, help='Path to the JSON file')

    args = parser.parse_args()

    with open(args.json_file, 'r') as f:
        data = json.load(f)

    for name, path in data['paths'].items():
        # df = pd.read_csv(path)
        ts = time.time()
        cap = float(name.split("MW")[0])
        print("Generating {} capacity PV generator".format(cap))
        pv_generator = PVGenerator(path, PVCap=cap,)
        joblib.dump(pv_generator, f"{data['destination']}/PVgen-{name}.sav")
        print("Time to generate PV generator: {}".format(time.time()-ts))

if __name__ == "__main__":
    main()