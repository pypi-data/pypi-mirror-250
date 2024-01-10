from mysql.connector import MySQLConnection, connect
from mysql.connector.errors import ProgrammingError
from typing_extensions import Union, Unpack

from tidb_vector.collection import VectorCollection, CollectionBaseOptions
from tidb_vector.config import ConnectionConfig
from tidb_vector.exceptions import VectorCollectionValidationException


class VectorStore:
    table_name_prefix: str
    config: dict

    def __init__(
            self,
            table_name_prefix: str = 'vector_collection_',
            **kwargs
    ):
        """
        Connect to a TiDB Vector Store.

        :param table_name_prefix: Table prefix for Vector Collections
        :param kwargs: Mysql connector options
        """
        self.table_name_prefix = table_name_prefix
        config = ConnectionConfig()
        db_conf = {
            "host": config.tidb_host,
            "port": config.tidb_port,
            "user": config.tidb_user,
            "password": config.tidb_password,
            "database": config.tidb_db_name,
            "autocommit": False,
            # mysql-connector-python will use C extension by default,
            # to make this example work on all platforms more easily,
            # we choose to use pure python implementation.
            "use_pure": True,
            **kwargs
        }

        if config.ca_path:
            db_conf["ssl_verify_cert"] = True
            db_conf["ssl_verify_identity"] = True
            db_conf["ssl_ca"] = config.ca_path
        self.config = db_conf

    def get_connection(self) -> MySQLConnection:
        return connect(**self.config)

    def open_collection(self, **kwargs: Unpack[CollectionBaseOptions]) -> VectorCollection:
        """
        Open and verify a Vector Collection with given name, if not exists, will create one with config.

        :param name: The name of the Vector Collection (without prefix)
        :param dimensions: The dimensions of the Vector Collection
        :param m: TODO
        :param ef_construction: TODO
        :return: A Vector Collection
        """
        collection = self.__connect_collection(kwargs['name'])
        if collection is None:
            collection = self.__create_collection(**kwargs)
        if not collection.validate_options(**kwargs):
            raise VectorCollectionValidationException("Collection not match options.")
        return collection

    def list_collections(self) -> [str]:
        """
        List all Vector Collections in this store.

        :return: Names of Vector Collections
        """
        pass

    def delete_collection(self, name: str):
        """
        Delete a Vector Collection with given name
        :param name: The name of the Vector Collection to delete
        :return:
        """
        pass

    def __connect_collection(self, name: str) -> Union[VectorCollection, None]:
        """
        Connect to a Vector Collection with given name. Returns None if it doesn't exist.
        :param name: name of the Vector Collection.
        :return: connected Vector Collection.
        """
        collection = VectorCollection(
            get_connection=lambda: self.get_connection(),
            table_prefix=self.table_name_prefix,
            name=name,
            dimensions=-1)

        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute("""
                    SHOW CREATE TABLE """ + self.table_name_prefix + name + """;
                    """)
                    cursor.fetchone()
                    return collection
                except ProgrammingError:
                    return self.__create_collection(name=name, dimensions=-1)

    def __create_collection(self, **kwargs: Unpack[CollectionBaseOptions]) -> VectorCollection:
        """
        Create a new Vector Collection with given options
        :param name: Name of the Vector Collection
        :param dimensions: The dimensions of the Vector Collection
        :param m: TODO
        :param ef_construction: TODO
        :return: A Vector Collection
        """
        collection = VectorCollection(lambda: self.get_connection(), self.table_name_prefix, **kwargs)
        sql = collection.get_create_table_sql()
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        return collection
