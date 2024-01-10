import json
from abc import abstractmethod

from mysql.connector import MySQLConnection
from typing_extensions import TypedDict, Unpack, override, Literal, List, Callable

from tidb_vector.document import VectorDocument, VectorDocumentSearchResult


class CollectionBaseOptions(TypedDict):
    table_prefix: str
    name: str
    dimensions: int


class VectorCollection:
    get_connection: Callable[[], MySQLConnection]
    table_prefix: str
    name: str
    dimensions: int

    def __init__(
            self,
            get_connection: Callable[[], MySQLConnection],
            table_prefix: str,
            **kwargs: Unpack[CollectionBaseOptions]):
        self.get_connection = get_connection
        self.table_prefix = table_prefix
        self.name = kwargs['name']
        self.dimensions = kwargs['dimensions']

    def insert(self, documents: [VectorDocument]):
        if len(documents) == 0:
            return
        sql, args = self.get_insert_sql(documents)
        print(sql, len(args))
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                connection.commit()
                print(cursor.rowcount)

    def delete(self, document_id: str):
        pass

    def similarity_search(self, vector: [float], limit: int = -1) -> List[VectorDocumentSearchResult]:
        docs = []
        sql = self.get_similarity_search_sql(limit)

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                cursor.execute(sql, [str(vector)])
                rows = cursor.fetchall()
                for row in rows:
                    docs.append(VectorDocumentSearchResult(*row))
        return docs

    def get_create_table_sql(self) -> str:
        return """
        CREATE TABLE """ + self.table_prefix + self.name + """ (
            id VARCHAR(64) NOT NULL,
            vector VECTOR NOT NULL,
            content LONGTEXT NOT NULL,
            metadata JSON NOT NULL,
            PRIMARY KEY (id)
        );
        """

    def get_insert_sql(self, documents: List[VectorDocument]) -> [str, any]:
        tmpl = ''
        comma = ''
        values = []

        for document in documents:
            tmpl += comma + '(%s, %s, %s, %s)'
            comma = ', '
            values.append(document.id)
            values.append(str(document.vector))
            values.append(document.content)
            values.append(json.dumps(document.metadata))

        return """
        INSERT INTO """ + self.table_prefix + self.name + """ (id, vector, content, metadata)
        VALUES """ + tmpl + """
        """, values

    def get_similarity_search_sql(self, limit: int):
        return """
        SELECT 
            id, 
            content, 
            metadata, 
            vec_cosine_distance(vector, %s) as distance 
        FROM """ + self.table_prefix + self.name + """
        ORDER BY distance ASC
        """ + ('' if limit == -1 else (" LIMIT " + str(limit))) + """
        """

    def get_delete_sql(self) -> str:
        pass

    def validate_options(self, **kwargs: Unpack[CollectionBaseOptions]) -> bool:
        return True
