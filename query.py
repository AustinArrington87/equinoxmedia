import csv 
import json
import sys
from datetime import datetime
from statistics import mean

# increase CSV size limit 
csv.field_size_limit(sys.maxsize)

# create arrays to store before and after data 
fullSample = []
beforeSample = []
afterSample = []

# read in CSV data, focus on createdOn and metrics 
csv_file = 'bikeExport.csv'

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fullSample.append(
            (row.get('createdOn'), row.get('metrics'))
        )

# change made on 2021-07-30 --> so everything after that goes in afterSample bucket
for data in fullSample:
    datestring = data[0]
    dt = datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S.%f")
    if dt >= datetime.fromisoformat("2021-07-30"):
        afterSample.append(data[1])
    else:
        beforeSample.append(data[1])

# buckets for min and max RSSI (before and after event)
max_rssi_b = []
min_rssi_b = []
max_rssi_a = []
min_rssi_a = []
json_objects_b = []
json_objects_a = []
# load string into JSON object 

for sample in beforeSample:
    jsonObj = json.loads(sample)
    json_objects_b.append(jsonObj)

for sample in afterSample:
    jsonObj = json.loads(sample)
    json_objects_a.append(jsonObj)

#before 
for obj in json_objects_b:
    try:
        max_rssi_b.append(obj['pm_benchmark_rssi_max'])
    except:
        pass
    try:
        min_rssi_b.append(obj['pm_benchmark_rssi_min'])
    except:
        pass

#after 
for obj in json_objects_a:
    try:
        max_rssi_a.append(obj['pm_benchmark_rssi_max'])
    except:
        pass
    try:
        min_rssi_a.append(obj['pm_benchmark_rssi_min'])
    except:
        pass

# average min and max RSSI - before update
before_min = mean(min_rssi_b)
before_max = mean(max_rssi_b)
# average min and max RSSI - after update
after_min = mean(min_rssi_a)
after_max = mean(max_rssi_a)

print("Avg RSSI Before 07-30-21 update | Min_RSSI: ", before_min, "| Max_RSSI: ", before_max)
print("Before Sample Size: ", len(min_rssi_b))
print("------------------------------------------------------------------------------------")
print("Avg RSSI After 07-30-21 update | Min_RSSI: ", after_min, "| Max_RSSI: ", after_max)
print("After Sample Size: ", len(min_rssi_a))
