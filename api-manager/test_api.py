import api_manager
import pytest

def execute(capsys, input):
    api_manager.transform(iter(input))
    return capsys.readouterr().out


def test_all_fields(capsys):
    input = [
        'Application,"Application Name","Message ID","Request Outcome","Request Size","Resource Path","Response Size","Response Time","Runtime Host","Status Code",Timezone,Verb,"Violated Policy Name",Timestamp,"API ID","API Version ID","API Name","API Version Name"',
        ',,"MYID001,PROCESSED,,/ingestion/api/v1/ping,,5,hostname,200,,GET,,2020-12-11T03:11:55.853Z,211436129,16316987,ingestion-api,v1'
    ]
    assert execute(capsys, input) == '2020-12-11T03:11:55.853000,2020-12-11T03:11:55.858000,MYID001\n'

def test_min_fields(capsys):
    input = [
        '"Message ID","Resource Path","Response Time",Timestamp',
        '"MYID001,/ingestion/api/v1/ping,5,2020-12-11T03:11:55.853Z,211436129'
    ]
    assert execute(capsys, input) == '2020-12-11T03:11:55.853000,2020-12-11T03:11:55.858000,MYID001\n'

def test_diff_order(capsys):
    input = [
        'Timestamp,"Resource Path","Message ID","Response Time"',
        '2020-12-11T03:11:55.853Z,/ingestion/api/v1/ping,MYID001,5'
    ]
    assert execute(capsys, input) == '2020-12-11T03:11:55.853000,2020-12-11T03:11:55.858000,MYID001\n'

def test_missing_fiel(capsys):
    with pytest.raises(ValueError, match="'Timestamp' is not in list"):
        input = [
            '"Resource Path","Message ID","Response Time"',
        ]
        execute(capsys, input)

def test_no_quotes(capsys):
    input = [
        'Application,Application Name,Message ID,Request Outcome,Request Size,Resource Path,Response Size,Response Time,Runtime Host,Status Code,Timezone,Verb,Violated Policy Name,Timestamp,API ID,API Version ID,API Name,API Version Name',
        ',,"MYID001,PROCESSED,,/ingestion/api/v1/ping,,5,hostname,200,,GET,,2020-12-11T03:11:55.853Z,211436129,16316987,ingestion-api,v1'
    ]
    assert execute(capsys, input) == '2020-12-11T03:11:55.853000,2020-12-11T03:11:55.858000,MYID001\n'
