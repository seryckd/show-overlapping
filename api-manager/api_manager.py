"""
Takes a CSV from Mule Anypoint API Manager and passes it into a format that can be
used by overlap.py

A sample file is

# Application,"Application Name","Message ID","Request Outcome","Request Size","Resource Path","Response Size","Response Time","Runtime Host","Status Code",Timezone,Verb,"Violated Policy Name",Timestamp,"API ID","API Version ID","API Name","API Version Name"
# ,,"1-9fc737d0-3b5e-11eb-b9e8-000d3ae61504",PROCESSED,,/ingestion/api/v1/ping,,5,vmmullobpre011,200,,GET,,2020-12-11T03:11:55.853Z,211436129,16316987,loblaw-ingestion,v1
# ,,"1-a3f18090-3b5e-11eb-b9e8-000d3ae61504",PROCESSED,2947,"/ingestion/api/v1/messages?sender=LOBLAWS.INC&receivers=LCT.GLOBAL&entity=purchaseorder&bulkFormat=CSV&entityVersion=BY-2020.1.0&model=native",182,1318,vmmullobpre011,202,,POST,,2020-12-11T03:12:02.841Z,211436129,16316987,loblaw-ingestion,v1
"""

import sys
from datetime import timedelta, datetime

def find_idx(words, idx):
    """
    Looks for the named index in the list. Test for the index name surrounded
    by quotes first, if it is not present then the error will return the index name without quotes
    """
    try:
        return words.index('"' + idx + '"')
    except ValueError:
        return words.index(idx)

def transform(input_stream, ignorePing=False):
    """
    Extracts data from the incoming and outputs the expected format
    """

    # The first line is the list of columns available
    headers = next(input_stream)

    # Extract the indexes for the columns we want to extract
    words = headers.rstrip().split(",")

    idx_MessageId = find_idx(words, 'Message ID')
    idx_ResponseTime = find_idx(words, 'Response Time')
    idx_Timestamp = find_idx(words, 'Timestamp')

    if ignorePing:
        idx_ResourcePath = find_idx(words, 'Resource Path')

    for line in input_stream:
        words = line.rstrip().split(",")

        if ignorePing:
            if  'ping' in words[idx_ResourcePath]:
                continue

        # input is '2020-12-11T03:09:25.841Z'
        # but 'Z' does not seem to be supported by strptime
        # replace 'Z' by 'UTC'
        start_time = datetime.strptime(words[idx_Timestamp].replace('Z','UTC'),"%Y-%m-%dT%H:%M:%S.%f%Z")
            
        duration = timedelta(milliseconds=int(words[idx_ResponseTime]))
        
        print('{},{},{}'.format(
            start_time.isoformat(), 
            (start_time + duration).isoformat(), 
            words[idx_MessageId].strip('\"')))
    
if __name__ == "__main__":
    """
    When run from the command line
    """
    import argparse

    parser = argparse.ArgumentParser(description='Parse Mule Api Manager CSV Report')
    parser.add_argument('--ignorePing', action='store_true', help='Ignore resouce path that contain the word ping')

    args = parser.parse_args()

    transform(sys.stdin, args.ignorePing)
