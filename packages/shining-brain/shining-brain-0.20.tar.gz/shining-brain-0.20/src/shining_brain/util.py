import os
from pathlib import Path
import re
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
import yaml
from shining_brain.logger_setup import setup_logger

logger = setup_logger("util.py")


def load_file_into_database(filename, table_name, column_mapping=None, before_statement=None, after_statement=None):
    base = declarative_base()

    db_config = load_configurations("database")

    engine = create_engine(get_url(db_config))
    base.metadata.create_all(engine)

    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    if before_statement is not None:
        session.execute(text(before_statement))
        session.commit()
    if filename.endswith('.csv'):
        data_frame = pd.read_csv(filename)
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        data_frame = pd.read_excel(filename)
    else:
        logger.warning('Unknown file type')
        return

    if column_mapping is not None:
        data_frame.rename(columns=column_mapping, inplace=True)

    data_frame.to_sql(table_name, con=engine, index=False, if_exists='append')
    if after_statement is not None:
        session.execute(text(after_statement))
        session.commit()
        session.close()
    logger.info('Data successfully loaded into the database')


def load_configurations(key):

    script_path = Path(__file__).parent
    filename = 'application.yaml'
    env = os.getenv('active_env')
    if env is not None and env not in ['', 'None']:
        filename = f'application_{env}.yaml'

    yaml_file_path = script_path.parent / 'conf' / filename
    with open(yaml_file_path, 'r', encoding='UTF-8') as file:
        db_config = yaml.safe_load(file)
    return db_config[key]


def get_url(db_config):
    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    database = db_config["database"]
    return f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'


def map_dtype(dtype):
    if "int" in str(dtype):
        return "int"
    if "float" in str(dtype):
        return "decimal(16,6)"
    if "datetime" in str(dtype):
        return "datetime"
    return "varchar(50)"


def to_snake_case(a_text):
    return re.sub(r'\W+', '_', a_text).lower()


def generate_ddl(file_path, table_name="table_name"):
    if file_path.endswith('.csv'):
        data_frame = pd.read_csv(file_path, nrows=1)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data_frame = pd.read_excel(file_path, nrows=1)
    else:
        logger.warning('Unknown file type')
        return None

    ddl = f"create table {table_name} (\n"
    ddl += "    id bigint auto_increment primary key,\n"
    for column, dtype in data_frame.dtypes.items():
        mysql_type = map_dtype(dtype)
        ddl += f"    {to_snake_case(column)} {mysql_type},\n"

    ddl += "    created datetime default current_timestamp () not null,\n"
    ddl += "    updated datetime default current_timestamp () not null,\n"
    return ddl.rstrip(",\n") + "\n);"


def generate_column_mapping(file_path):
    if file_path.endswith('.csv'):
        data_frame = pd.read_csv(file_path, nrows=1)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        data_frame = pd.read_excel(file_path, nrows=1)
    else:
        logger.warning('Unknown file type')
        return None

    column_mapping = {}
    for column in data_frame.columns:
        column_mapping[column] = to_snake_case(column)

    return column_mapping


def gather_file_paths(directory_path, files, pattern):
    dir_path = Path(directory_path)
    if not dir_path.is_dir():
        raise ValueError(f"The path {directory_path} is not a valid directory")

    for file_path in dir_path.iterdir():
        if file_path.is_dir():
            gather_file_paths(file_path, files, pattern)
            continue
        if re.match(pattern, file_path.as_posix()):
            files.append(file_path)
