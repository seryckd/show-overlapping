"""
Takes a CSV from Mule Anypoint API Manager and passes it into a format that can be
used by overlap.py
"""

import sys
from datetime import timedelta, datetime

# skip first line as the CSV header
next(sys.stdin)

# Application,"Application Name","Message ID","Request Outcome","Request Size","Resource Path","Response Size","Response Time","Runtime Host","Status Code",Timezone,Verb,"Violated Policy Name",Timestamp,"API ID","API Version ID","API Name","API Version Name"
# ,,"1-9fc737d0-3b5e-11eb-b9e8-000d3ae61504",PROCESSED,,/ingestion/api/v1/ping,,5,vmmullobpre011,200,,GET,,2020-12-11T03:11:55.853Z,211436129,16316987,loblaw-ingestion,v1
# ,,"1-a3f18090-3b5e-11eb-b9e8-000d3ae61504",PROCESSED,2947,"/ingestion/api/v1/messages?sender=LOBLAWS.INC&receivers=LCT.GLOBAL&entity=purchaseorder&bulkFormat=CSV&entityVersion=BY-2020.1.0&model=native",182,1318,vmmullobpre011,202,,POST,,2020-12-11T03:12:02.841Z,211436129,16316987,loblaw-ingestion,v1


for line in sys.stdin:
    words = line.rstrip().split(",")

#    if 'ping' in words[5]:
#        continue

    # input is '2020-12-11T03:09:25.841Z'
    # but 'Z' does not seem to be supported by strptime
    # replace 'Z' by 'UTC'
    start_time = datetime.strptime(words[13].replace('Z','UTC'),"%Y-%m-%dT%H:%M:%S.%f%Z")
        
    duration = timedelta(milliseconds=int(words[7]))
    
    #print('{},{},{}'.format(words[2], words[7], words[13]))

    print('{},{},{}'.format(
        start_time.isoformat(), 
        (start_time + duration).isoformat(), 
        words[2].strip('\"')))
    
