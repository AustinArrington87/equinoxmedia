import csv
import numpy as np

auth_list = []
subscriber_list = []
auth_file = 'auth.csv'
subscriber_file='subscriber.csv'

with open(auth_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        auth_list.append(
            row.get('id')
        )

#print(auth_list)
print("Auth0 Users: ", len(auth_list))

with open(subscriber_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        subscriber_list.append(
            (row.get('USER_ID'), row.get('ACTIVE_USER_COUNT'))
        )

active_subscribers = []

#print(subscriber_list)
print("Total Subscribers: ", len(subscriber_list))

for subscriber in subscriber_list:
    if subscriber[1] == '1':
        active_subscribers.append(subscriber)

print("Active Subscribers: ", len(active_subscribers))

percentSubscribersActive = round(len(active_subscribers)/len(subscriber_list), 2)
print("Percent of Subscribers Active (%) : ", str(percentSubscribersActive*100))

percentSingleAppSubscribers = round(len(auth_list)/len(active_subscribers), 2)
print("Percent Active Subscribers Using Single App (%): ", str(percentSingleAppSubscribers*100))

# show me any elements in auth_list not in active_subscriber_list 
adjusted_subscriber_auth_list = np.setdiff1d(auth_list, active_subscribers)

print("======================================")

print("No. IDs in auth_list not in active subscribers: ", str(len(adjusted_subscriber_auth_list)))

# write out CSV of IFs in auth_list not in active_subscribers
header = ['id']
with open('auth_not_subscriber.csv', 'w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    # write header
    writer.writerow(header)
    for id in adjusted_subscriber_auth_list:
        id = id
        data = [id]
        writer.writerow(data)
        
adjusted_auth_user_len =  len(auth_list) - len(adjusted_subscriber_auth_list)
print("Adjusted Auth0 Users: ", adjusted_auth_user_len)
adjustedPercentSubscribersActive = round(adjusted_auth_user_len/len(active_subscribers), 2)
print("Adjusted Percent Active Subscribers Using Single App (%): ", str(adjustedPercentSubscribersActive*100))
