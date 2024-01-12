import datetime
import pytest
from antimatter.tags import ColumnTag, SpanTag
from antimatter.capsule import Capsule, CapsuleBindings  # Replace with your actual module name
import antimatter_engine as ae

@pytest.fixture
def mock_capsule_bindings(monkeypatch, capsule_tags, column_names, column_tags, redacted_data, data_span_tags, extra_info):
    mock_capsule_bindings = CapsuleBindings(None, [])
    
    # mock the read_all_with_tags method
    monkeypatch.setattr(
        mock_capsule_bindings, 
        'read_all_with_tags', 
        lambda _: (capsule_tags, column_names, column_tags, redacted_data, data_span_tags, extra_info)
    )

    return mock_capsule_bindings

@pytest.mark.parametrize(
    "capsule_tags, column_names, column_tags, redacted_data, data_span_tags, extra_info",
    [
        # Test case 1
        (
            [],  # capsule_tags
            ['email', 'bytes', 'fname', 'bio', 'duration', 'dt', 'float', 'age', 'status', 'id'],  # column_names
            [[], [], [], [], [], [], [], [ae.PyTag('tag.antimatter.io/pii/age', 0, '', 'manual', (1, 0, 0)), ae.PyTag('tag.antimatter.io/pii/other', 0, '', 'manual', (1, 0, 0))], [], []],  # column_tags
            [
                [b'allen@gmail.com', b'fdsa', b'Allen', b'{redacted} on {redacted} 9 1974 in Cheverly, MD', b'{redacted}', b'{redacted}', b'3.14', b'{redacted}', b'True', b'44'],
                [b'this is an email address: {redacted}', b'asdf', b'Bob', b'Born on November 1 1985 in Pittsburg, PA.', b'{redacted}', b'2024-01-10T14:44:07.625505', b'6.28', b'{redacted}', b'False', b'33']
            ],  # redacted_data
            [
                [[], [], [], [ae.PySpanTag(start=0, end=4, tag=ae.PyTag('tag.antimatter.io/pii/first_name', 1, '', 'manual', (1,0,0))), ae.PySpanTag(start=8, end=16, tag=ae.PyTag('tag.antimatter.io/pii/first_name', 1, '', 'manual', (1,0,0)))], [ae.PySpanTag(start=0, end=7, tag=ae.PyTag('tag.antimatter.io/pii/id', 1, '', 'manual', (1,0,0)))], [ae.PySpanTag(start=0, end=26, tag=ae.PyTag('tag.antimatter.io/pii/date_of_birth', 1, '', 'manual', (1,0,0)))], [], [], [], []],
                [[ae.PySpanTag(start=26, end=39, tag=ae.PyTag('tag.antimatter.io/pii/email_address', 1, '', 'manual', (1,0,0)))], [], [], [], [ae.PySpanTag(start=0, end=7, tag=ae.PyTag('tag.antimatter.io/pii/id', 1, '', 'manual', (1,0,0)))], [], [], [], [], []
            ]],  # data_span_tags
            '{"dict_list": {}, "_coltype": {"email": "string", "bytes": "bytes", "fname": "string", "bio": "string", "duration": "timedelta", "dt": "date_time", "float": "float", "age": "int", "status": "bool", "id": "int"}, "_metadtype": "dict_list"}'  # extra_info
        ),
        # Additional test cases can be added here
    ]
)
def test_data_with_tags(mock_capsule_bindings):
    capsule = Capsule(mock_capsule_bindings)
    result = capsule.data_with_tags(read_params={}, column_major=False)

    # validate expected list lengths for result
    assert len(result) == 2
    assert len(result[0]) == 10
    assert len(result[1]) == 10

    # validate span tags were created
    assert len(result[0][3]['spans']) == 2
    spans = result[0][3]['spans']
    assert spans[0].__class__ == SpanTag and spans[1].__class__ == SpanTag
    assert spans[0].start == 0 and spans[0].end == 4
    assert spans[1].start == 8 and spans[1].end == 16
    assert len(result[0][4]['spans']) == 1

    # validate column tags were created
    assert len(result[0][7]['column_tags']) == 2
    assert result[0][7]['column_tags'][0].__class__ == ColumnTag
    assert result[0][7]['column_tags'][1].__class__ == ColumnTag

    # sanity check on unmolested bytes
    assert result[1][0]['bytes'] == b'this is an email address: {redacted}'
    assert result[1][1]['bytes'] == b'asdf'
    assert result[1][2]['bytes'] == b'Bob'
    assert result[1][3]['bytes'] == b'Born on November 1 1985 in Pittsburg, PA.'
    assert result[1][4]['bytes'] == b'{redacted}'
    assert result[1][5]['bytes'] == b'2024-01-10T14:44:07.625505'
    assert result[1][6]['bytes'] == b'6.28'
    assert result[1][7]['bytes'] == b'{redacted}'
    assert result[1][8]['bytes'] == b'False'
    assert result[1][9]['bytes'] == b'33'

    # validate the data conversions for redacted and unredacted data
    assert result[1][0]['data'] == 'this is an email address: {redacted}'
    assert result[1][1]['data'] == b'asdf'
    assert result[1][2]['data'] == 'Bob'
    assert result[1][3]['data'] == 'Born on November 1 1985 in Pittsburg, PA.'
    assert result[1][4]['data'] == datetime.timedelta(0)
    assert result[1][5]['data'] == datetime.datetime.strptime('2024-01-10 14:44:07.625505', "%Y-%m-%d %H:%M:%S.%f")
    assert result[1][6]['data'] == 6.28
    assert result[1][7]['data'] == 0
    assert result[1][8]['data'] == False
    assert result[1][9]['data'] == 33