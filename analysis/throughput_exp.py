import json
import argparse
from collections import defaultdict
from typing import Dict, Any
import pandas as pd
from matplotlib import pyplot as plt
import pandas.plotting._matplotlib
df = pd.DataFrame()

def max_bytecounts_at_same_time(file_path: str) -> Dict[str, Any]:
    # Load data from the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
   
    # Dictionary to store the count of bytecounts per timestamp
    time_bytecount_map = defaultdict(int)

    # Process each entry in the data
    for entry in data:
        for progress in entry["progress"]:
            timestamp = progress["time"]
            time_bytecount_map[timestamp] += 1

    # Find the maximum count and the corresponding timestamp(s)
    max_count = max(time_bytecount_map.values())
    max_timestamps = [time for time, count in time_bytecount_map.items() if count == max_count]

    return {
        "max_count": max_count,
        "timestamps": max_timestamps
    }

# Function to read a file and parse JSON
def parse_json_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to calculate duration in milliseconds
def calculate_duration(progress):
    start_time = int(progress[0]['time'])
    end_time = int(progress[-1]['time'])
    return end_time - start_time

# Function to calculate exponential moving average of throughput for each ID
# def calculate_throughput(data, alpha=0.3):
#     throughput_map = {}
#     window_size = 5
#     # Loop through each upload data
#     for upload in data:
#         id = upload['id']
#         progress = upload['progress']

#         # Extract time and byte counts for this progress
#         byte_counts = pd.Series([progress_obj['bytecount'] for progress_obj in progress])
#         times = pd.Series([progress_obj['time'] for progress_obj in progress])

#         # Calculate the EMA for byte counts over time
#         ema_throughputs = round(byte_counts.ewm(alpha=0.5, adjust=True).sum()/
#                                 (times.max() -
#                                     times.min()), 2)
#         throughput_list = ema_throughputs.tolist()

#         print(final_list)

#     return final_list


# Function to calculate throughput for each interval and apply EMA
def calculate_throughput(data, alpha=0.15, loopval = 2):
    throughput_map = {}

    # Loop through each upload data
    for upload in data:
        id = upload['id']
        progress = upload['progress']

        # Extract time and byte counts for this progress
        byte_counts = [progress_obj['bytecount'] for progress_obj in progress]
        times = [int(progress_obj['time']) for progress_obj in progress]

        # List to store calculated throughput for each interval
        throughput = []
        interval_times = []  # List to store timestamps aligned with throughput calculations

        # Calculate throughput for each interval between consecutive byte counts
        for i in range(loopval, len(byte_counts)):
            byte_sum = 0
            for j in range(i,i-loopval,-1):
                byte_sum = byte_sum + byte_counts[j]
            time_diff = times[i] - times[i-loopval]
            if time_diff == 0:
                print(times[i])
                # Calculate throughput if time difference is non-zero
            throughput_value = byte_sum / time_diff
            throughput.append(throughput_value)
            interval_times.append(times[i])  # Use the current timestamp for this interval

        # Convert throughput list to pandas Series
        throughput_series = pd.Series(throughput)

        # Calculate the exponential moving average (EMA) of throughput
        throughput_ema = throughput_series.ewm(alpha=alpha, adjust=False).mean()

        # Store the EMA results as a list for easier readability
        throughput_map[id] = throughput_ema.tolist()

        # Prepare DataFrame for plotting
        if len(interval_times) == len(throughput_ema):
            df = pd.DataFrame({'Throughput': throughput_ema.tolist(), 'Time': interval_times})

            # Plotting
            df.plot(kind='scatter', x='Time', y='Throughput')
            plt.xlabel('Time')
            plt.ylabel('Throughput')
            plt.title(f'Throughput vs Time for {id}')
            plt.show()
        else:
            print(f"Length mismatch after EMA: Throughput EMA length = {len(throughput_ema)}, Interval Times length = {len(interval_times)}")

    return throughput_map

def aggregateTCPflows():
    # Loop through each upload data
    initial_max_time = 0
    ending_time = 0
    initial_time = 0
    for upload in data:
        id = upload['id']
        progress = upload['progress']
        if (int(progress[0]["time"]) > initial_time):
            initial_max_time = int(progress[0]["time"])            

        print("0: ", progress[0]["time"])
        print("1: ", progress[1]["time"])
    print (initial_time)

    


parser = argparse.ArgumentParser(
    prog="throughput_sma.py",
    description="Throughput calculation"
    )
parser.add_argument("serverName")
args=parser.parse_args()

loop = max_bytecounts_at_same_time("analysis/output/" +args.serverName+"/byte_time.json")

# Load data from file
data = parse_json_from_file("analysis/output/" +args.serverName+"/byte_time.json")

# Load data from file
data = parse_json_from_file("analysis/output/" +args.serverName+"/byte_time.json")

# Calculate throughput by IDs
# throughput_by_ids = calculate_throughput(data, loopval=loop['max_count'])

# Print throughput by IDs
# print("Throughput by IDs:", throughput_by_ids)

aggregateTCPflows()