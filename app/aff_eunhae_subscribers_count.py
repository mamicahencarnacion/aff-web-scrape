"""
    Created by Ma. Micah Encarnacion on 09/07/2020
"""
import csv
import operator

subscribers = {}

with open('subscriptions.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0

    for row in csv_reader:

        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1

        if row["username"] in subscribers.keys():
            subscribers[row["username"]] += 1
        else:
            subscribers[row["username"]] = 1

        line_count += 1
    print(f'Processed {line_count} lines.')

index = 0
subscribers_sorted = dict(sorted(subscribers.items(), key=operator.itemgetter(1),reverse=True))
for sub, count in subscribers_sorted.items():
    if index > 10:
        break
    print(sub, ":\t", count)
    index += 1
