import re

pattern = re.compile(r'^[a-z_][a-z0-9_]{0,63}$', re.I)


def assert_legal_table_name(name: str):
    if pattern.match(name) is None:
        raise AssertionError('illegal table name')
