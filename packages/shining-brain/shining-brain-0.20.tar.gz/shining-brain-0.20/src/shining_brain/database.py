class ColumnDefinition:
    def __init__(self, datatype: str, length: int, default_value=None, is_null: bool = True):
        self.__datatype = datatype
        self.__length = length
        self.__default_value = default_value
        self.__is_null = is_null

    def __str__(self):
        default_value = "" if self.__default_value is None else f' default "{self.__default_value}"'
        return f'{self.__datatype}({self.__length.__str__()}) {"null" if self.__is_null is True else "not null"}{default_value}'


class CreateDefinition:

    def __init__(self, name: str, column_definition: ColumnDefinition, is_last: bool = False):
        self.__name = name
        self.__column_definition = column_definition
        self.__is_last = is_last

    def get_name(self) -> str:
        return self.__name

    def is_last(self) -> bool:
        return self.__is_last

    def __str__(self):
        return f'{self.__name} {self.__column_definition.__str__()}'
