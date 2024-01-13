from shining_brain.util import load_file_into_database, generate_ddl, generate_column_mapping
from shining_brain.logger_setup import setup_logger

logger = setup_logger('main.py')


def refresh_data(filename, table_name):
    filepath = f"/Users/thomas/Documents/english-language/{filename}.csv"
    logger.info('\n \n%s\n', generate_ddl(filepath, table_name))
    column_mapping = generate_column_mapping(filepath)
    before_statement = f'delete from {table_name} where id > 0'
    load_file_into_database(filepath, table_name, column_mapping, before_statement)


if __name__ == '__main__':
    refresh_data('wordbank', 'word_bank')
    refresh_data('transactions', 'transaction')
