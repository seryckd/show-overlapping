import overlap
import pytest

def execute(capsys, input):
    overlap.parse(iter(input))
    return capsys.readouterr().out


def test_same_begin(capsys):
    input = [
        '2020-12-11T03:17:11.177000,2020-12-11T03:17:12.627000,A',
        '2020-12-11T03:17:11.177000,2020-12-11T03:17:12.407000,B'
    ]
    assert execute(capsys, input) == 'Start, End, Duration, Count\n' \
        '2020-12-11 03:17:11.177000,2020-12-11 03:17:12.407000,1230,2\n' \
        '2020-12-11 03:17:12.407000,2020-12-11 03:17:12.627000,220,1\n' \
        'max-bucket  2\n'
    
def test_same_end(capsys):
    input = [
        '2020-12-11T03:17:11.177000,2020-12-11T03:17:12.627000,A',
        '2020-12-11T03:17:11.400000,2020-12-11T03:17:12.627000,B'
    ]
    assert execute(capsys, input) == 'Start, End, Duration, Count\n' \
        '2020-12-11 03:17:11.177000,2020-12-11 03:17:11.400000,223,1\n' \
        '2020-12-11 03:17:11.400000,2020-12-11 03:17:12.627000,1227,2\n' \
        'max-bucket  2\n'

def test_same_range(capsys):
    input = [
        '2020-12-11T03:17:11.177000,2020-12-11T03:17:12.627000,A',
        '2020-12-11T03:17:11.177000,2020-12-11T03:17:12.627000,B'
    ]
    assert execute(capsys, input) == 'Start, End, Duration, Count\n' \
        '2020-12-11 03:17:11.177000,2020-12-11 03:17:12.627000,1450,2\n' \
        'max-bucket  2\n'
