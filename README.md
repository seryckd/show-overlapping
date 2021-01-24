# Overview

Determine the number of overlapping threads or api calls based upon the start time and end times and 
output the maximum number.

It is used to discover the amount of parallelism, which can be useful in debugging issues or configuring for
optimal processing.

Optionally show the identifier for each process as well.

Written to learn Python.

## Input

Given an input file in the format 'start,end,process id'

```
2020-12-30T21:56:44.967572,2020-12-30T21:57:44.042572,id0
2020-12-30T21:57:43.006572,2020-12-30T21:58:35.771572,id1
```

## Output

Outputs lines in the form 'start, end, number of processes, list of each process'

```
2020-12-30T21:56:44.967572,2020-12-30T21:57:43.006572,58039,1,['id0']
2020-12-30T21:57:43.006572,2020-12-30T21:57:44.042572,1036,2,['id0', 'id1']
2020-12-30T21:57:44.042572,2020-12-30T21:58:35.771572,51729,1,['id1']
```

# Generate Test Data

_generate-testdata.py_ provides testdata

```
python3 generate-testdata.py --count 30 | python3 overlap.py
```

unit cases

* 0 duration; begin and end points are the same
* two lines with the same begin point


# Notes

Written as part of learning Python.


start,end,id




