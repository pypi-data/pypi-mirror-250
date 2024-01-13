import pytest

from shining_brain.database import ColumnDefinition, CreateDefinition


@pytest.mark.parametrize('datatype, length, default_value, is_null, expected', [
    ('varchar', 50, "Evan", True, 'username varchar(50) null default "Evan"'),
    ('varchar', 50, None, True, 'username varchar(50) null'),
    ('varchar', 50, "Evan", False, 'username varchar(50) not null default "Evan"')
])
def test_column_name_and_column_definition(datatype, length, default_value, is_null, expected):
    username_column_definition = ColumnDefinition(datatype, length, default_value, is_null)
    username = CreateDefinition('username', username_column_definition)
    assert username.__str__() == expected
