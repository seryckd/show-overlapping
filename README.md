# Overview

| written to learn Python

Show overlapping threads or api calls based on start time and duration

Given an input file in the format 'start,end,id'

```
2020-12-30T21:56:44.967572,2020-12-30T21:57:44.042572,id0
2020-12-30T21:57:43.006572,2020-12-30T21:58:35.771572,id1
```

outputs the following 

```
2020-12-30T21:56:44.967572,2020-12-30T21:57:43.006572,58039,1,['id0']
2020-12-30T21:57:43.006572,2020-12-30T21:57:44.042572,1036,2,['id0', 'id1']
2020-12-30T21:57:44.042572,2020-12-30T21:58:35.771572,51729,1,['id1']
```

It is used to discover the amount of parallelism, which can be useful when correlated with other statistics like the process time.

# Generate Test Data

_generate-testdata.py_ provides testdata

```
python3 generate-testdata.py --count 30 | python3 overlap.py
```