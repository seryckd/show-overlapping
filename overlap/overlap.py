from datetime import timedelta, datetime
import sys, argparse

# Expecting file in the format
# start timestamp, stop timestamp, id


def add_point(nodes, point_ts, point_type, id):
    """ Adds a point to the node dictionary"""

    if point_ts in nodes:
        nodes[point_ts].append((point_type, id))
    else:
        nodes[point_ts] = [(point_type, id)]

def read_input(input_stream):
    """ Splits a line into two points, begin and end """

    nodes = {}

    for line in input_stream:
        words = line.rstrip().split(",")
        id = words[2]
        add_point(nodes, words[0], 'b', id)
        add_point(nodes, words[1], 'e', id)

    return nodes

def parse(input, showIds = False):

    nodes = read_input(input)

    # retrieve List of keys and sort points in place, earliest first
    node_points = list(nodes)
    node_points.sort()

    max_overlap = 0
    open_bucket_start = ''
    open_bucket = []

    if showIds:
        print('Start, End, Duration, Count, Ids')
    else:
        print('Start, End, Duration, Count')

    for node_point in node_points:

        # close the open bucket
        if (open_bucket_start != ''):

            # output the bucket details
            start_ts = datetime.fromisoformat(open_bucket_start)
            end_ts = datetime.fromisoformat(node_point)
            bucket_duration = round((end_ts - start_ts).total_seconds() * 1000)

            if showIds:
                print('{},{},{},{},{}'
                    .format(start_ts, end_ts, bucket_duration, len(open_bucket), open_bucket))
            else:
                print('{},{},{},{}'
                    .format(start_ts, end_ts, bucket_duration, len(open_bucket)))

        # Start a new bucket as a copy of the previous one
        open_bucket_start = node_point
        open_bucket = open_bucket.copy()

        for points in nodes[node_point]:

            if points[0] == 'b':
                # Add in the new id to the current bucket
                open_bucket.append(points[1])

            else:
                # Remove the id from the current bucket
                open_bucket.remove(points[1])

        max_overlap = max(max_overlap, len(open_bucket))

    print ("max-bucket ", max_overlap)

"""
When run the command line
"""
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Count overlapping date ranges')
    parser.add_argument('-f', '--file', help='File to read from. If not present reads from the input stream')
    parser.add_argument('-i', '--ids', help='Output the ids for each bucket', action='store_true')

    args = parser.parse_args()

    # Read from the specified file.  If no file specified then default to the 
    # system input
    if args.file != None:
        with open(args.file) as files:
            parse(files, args.ids)
    else:
        parse(sys.stdin, args.ids)
