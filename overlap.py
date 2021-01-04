from datetime import timedelta, datetime
import sys, argparse

# Expecting file in the format
# start timestamp, stop timestamp, id

parser = argparse.ArgumentParser(description='Count overlapping date ranges')
parser.add_argument('-f', '--file', help='File to read from. If not present reads from the input stream')

args = parser.parse_args()

# split each line into two points, 'begin' and 'end'
def read_input(input_stream):
    for line in input_stream:
        words = line.rstrip().split(",")
        nodes[words[0]] = 'begin', words[2]
        nodes[words[1]] = 'end', words[2]

# dictionay/mapping
nodes = {}

if args.file != None:
    with open(args.file) as files:
        read_input(files)
else:
    read_input(sys.stdin)

# retrieve List of keys and sort points in place, earliest first
keys = list(nodes)
keys.sort()

max_overlap = 0
max_bucket = []
current_overlap = 0

open_bucket_start = ''
open_bucket_end = ''
open_bucket = []

def print_bucket(bucket_start, bucket_end, bucket):
    start_ts = datetime.fromisoformat(bucket_start)
    end_ts = datetime.fromisoformat(bucket_end)
    bucket_duration = round((end_ts - start_ts).total_seconds() * 1000)
    print('{},{},{},{},{}'
        .format(bucket_start, bucket_end, bucket_duration, len(bucket), bucket))

for k in keys:

    # close the open bucket
    if (open_bucket_start != ''):
        print_bucket(open_bucket_start, k, open_bucket)

    # Start a new bucket as a copy of the previous one
    open_bucket_start = k
    open_bucket = open_bucket.copy()

    if nodes[k][0] == 'begin':
        # Add in the new id to the current bucket
        open_bucket.append(nodes[k][1])

        current_overlap += 1

        if current_overlap > max_overlap:
            max_overlap = current_overlap
            max_bucket = open_bucket

    else:
        # Remove the id from the current bucket
        open_bucket.remove(nodes[k][1])

        current_overlap -= 1
