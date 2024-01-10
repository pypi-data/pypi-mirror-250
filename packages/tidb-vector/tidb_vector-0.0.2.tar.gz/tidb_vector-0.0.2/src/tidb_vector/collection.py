import json
from itertools import repeat

from mysql.connector import MySQLConnection
from typing_extensions import TypedDict, Unpack, override, Literal, List, Callable

from tidb_vector.document import VectorDocument, VectorDocumentSearchResult
from tidb_vector.utils import assert_legal_table_name


class CollectionBaseOptions(TypedDict):
    table_prefix: str
    name: str
    dimensions: int


class VectorCollection:
    get_connection: Callable[[], MySQLConnection]
    name: str
    dimensions: int
    table_name: str

    def __init__(
            self,
            get_connection: Callable[[], MySQLConnection],
            table_prefix: str,
            **kwargs: Unpack[CollectionBaseOptions]):
        self.get_connection = get_connection
        self.name = kwargs['name']
        self.table_name = table_prefix + self.name
        self.dimensions = kwargs.get('dimensions', -1)
        assert_legal_table_name(self.table_name)

    def insert(self, documents: List[VectorDocument]):
        """
        Inserts documents into Vector Collection
        :param documents: List of documents
        """
        if len(documents) == 0:
            return
        sql, args = self.__get_insert_sql(documents)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                connection.commit()

    def delete(self, document_ids: List[str]):
        """
        Deletes documents from Vector Collection
        :param document_ids: ids to delete
        """
        n = len(document_ids)
        if n == 0:
            return
        sql = self.__get_delete_sql(n)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, document_ids)
                connection.commit()

    def cosine_similarity(self, vector: [float], limit: int = -1) -> List[VectorDocumentSearchResult]:
        """
        Sort stored Vector Documents by cosine similarity
        :param vector: The query vector
        :param limit: Max amount of document to return. -1 represents no limit
        :return:
        """
        docs = []
        sql = self.__get_cosine_similarity_sql(limit)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, [str(vector)])
                rows = cursor.fetchall()
                for row in rows:
                    docs.append(VectorDocumentSearchResult(*row))
        return docs

    def __get_insert_sql(self, documents: List[VectorDocument]) -> [str, any]:
        values = []

        for document in documents:
            values.append(document.id)
            values.append(str(document.vector))
            values.append(document.content)
            values.append(json.dumps(document.metadata))

        return f"""
        INSERT INTO {self.table_name} (id, vector, content, metadata)
        VALUES {', '.join(repeat('(%s, %s, %s, %s)', len(documents)))}
        """, values

    def __get_cosine_similarity_sql(self, limit: int):
        assert type(limit) is int
        return f"""
        SELECT 
            id, 
            content, 
            metadata, 
            1 - vec_cosine_distance(vector, %s) as similarity 
        FROM {self.table_name}
        ORDER BY similarity DESC
        {'' if limit == -1 else (" LIMIT " + str(limit))}
        """

    def __get_delete_sql(self, count: int) -> str:
        return f"""
        DELETE
        FROM {self.table_name}
        WHERE id IN ({', '.join(repeat('%s', count))})
        """
