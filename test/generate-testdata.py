
from datetime import timedelta, datetime
import random, argparse

parser = argparse.ArgumentParser(description='Generate test data')
parser.add_argument('--count', type=int, default=5, dest='count', help='number of output rows')

args = parser.parse_args()

n = datetime.now()

for i in range(args.count):
    start_offset = timedelta(milliseconds=random.randint(1000, 360000))
    end_offset = timedelta(milliseconds=random.randint(1, 60000))
    start = n + start_offset
    end = start + end_offset
      
    print('{},{},id{}'.format(start.isoformat(), end.isoformat(), i))
