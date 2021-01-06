import sys
from datetime import timedelta, datetime

# skip first line as the CSV header
next(sys.stdin)

for line in sys.stdin:
    words = line.rstrip().split(",")

    # input is '2020-12-11T03:09:25.841Z'
    # but 'Z' does not seem to be supported by strptime
    # replace 'Z' by 'UTC'
    start_time = datetime.strptime(words[13].replace('Z','UTC'),"%Y-%m-%dT%H:%M:%S.%f%Z")
        
    duration = timedelta(milliseconds=int(words[7]))
    
    print('{},{},{}'.format(start_time.isoformat(), (start_time + duration).isoformat(), words[2]))
    
