import os
import re

import pandas as pd
import pytest

from shining_brain.util import generate_ddl, generate_column_mapping, to_snake_case, gather_file_paths, load_configurations


def test_generate_ddl_from_csv():
    data_frame = pd.DataFrame({
        'Name': ['Alice'],
        'Start Date': ['2020-02-02'],
        'Age': [18],
        'Salary': [5000.50],
    })
    data_frame.to_csv('./test_data.csv', index=False)

    expected_ddl = (
        "create table table_001 (\n"
        "    id bigint auto_increment primary key,\n"
        "    name varchar(50),\n"
        "    start_date varchar(50),\n"
        "    age int,\n"
        "    salary decimal(16,6),\n"
        "    created datetime default current_timestamp () not null,\n"
        "    updated datetime default current_timestamp () not null\n"
        ");"
    )

    filename = './test_data.csv'
    assert generate_ddl(filename, 'table_001') == expected_ddl


def test_generate_ddl_from_xlsx():
    data_frame = pd.DataFrame({
        'Name': ['Alice'],
        'Start Date': ['2020-02-02'],
        'Age': [18],
        'Salary': [5000.50],
    })
    data_frame.to_excel('./test_data.xlsx', index=False)

    expected_ddl = (
        "create table table_001 (\n"
        "    id bigint auto_increment primary key,\n"
        "    name varchar(50),\n"
        "    start_date varchar(50),\n"
        "    age int,\n"
        "    salary decimal(16,6),\n"
        "    created datetime default current_timestamp () not null,\n"
        "    updated datetime default current_timestamp () not null\n"
        ");"
    )

    filename = './test_data.xlsx'
    assert generate_ddl(filename, 'table_001') == expected_ddl


def test_generate_column_mapping():
    data_frame = pd.DataFrame({
        'Name': ['Alice'],
        'Start Date': ['2020-02-02'],
        'Age': [18],
        'Salary': [5000.50],
    })
    data_frame.to_excel('./test_data.xlsx', index=False)

    expected_column_mapping = {
        'Name': 'name',
        'Start Date': 'start_date',
        'Age': 'age',
        'Salary': 'salary'
    }

    filename = './test_data.xlsx'
    assert generate_column_mapping(filename) == expected_column_mapping


@pytest.mark.parametrize("text, expected", [
    ('Name', 'name'),
    ('name', 'name'),
    ('User Name', 'user_name'),
    ('User name', 'user_name'),
    ('user name', 'user_name'),
    ('user Name', 'user_name'),
    ('user Name', 'user_name'),
    ('first middle last', 'first_middle_last'),
    ('first middle/last', 'first_middle_last'),
])
def test_to_snake_case(text, expected):
    assert to_snake_case(text) == expected


def test_gather_file_paths():
    files = []
    gather_file_paths('.', files, r'^[\w/-]+(_\d{0,8}_to_\d{8})*(.xlsx|.csv)$')
    assert len(files) == 2


@pytest.mark.parametrize("text", [
    'dir/name_20190101_to_20221231.xlsx',
    'dir-dir/name_20190101_to_20221231.xlsx',
    'name_20190101_to_20221231.xlsx',
    'name_name1_20190101_to_20221231.xlsx',
    'name.csv'
])
def test_file_names(text):
    pattern = r'^[\w/-]+(_\d{0,8}_to_\d{8})*(.xlsx|.csv)$'
    assert re.match(pattern, text)


@pytest.mark.parametrize("env, expected", [
    ('test', 'localhost:3306'),
    ('None', '127.0.0.1:3306')
])
def test_to_snake_case(env, expected):
    os.environ['active_env'] = env
    host = load_configurations('database')['host']
    os.environ['active_env'] = 'None'
    assert host == expected
