def format_sql(sql: str) -> str:
    return ' '.join(
        filter(lambda s: s != '',
               map(lambda s: s.strip(),
                   sql.split('\n')))
    )

