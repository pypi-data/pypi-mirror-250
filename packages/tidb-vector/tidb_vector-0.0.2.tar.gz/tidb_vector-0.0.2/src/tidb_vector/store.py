from mysql.connector import MySQLConnection, connect
from mysql.connector.errors import ProgrammingError
from typing_extensions import Union, Unpack, List

from tidb_vector.collection import VectorCollection, CollectionBaseOptions
from tidb_vector.config import ConnectionConfig
from tidb_vector.exceptions import VectorCollectionValidationException
from tidb_vector.utils import assert_legal_table_name


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
        Open a Vector Collection with given name, if not exists, will create new one.

        :param name: The name of the Vector Collection (without prefix)
        :param dimensions: NOT USED YET The dimensions of the Vector Collection
        :param m: NOT USED YET TODO
        :param ef_construction: NOT USED YET TODO
        :return: A Vector Collection
        """
        name = kwargs["name"]
        collection = VectorCollection(
            get_connection=lambda: self.get_connection(),
            table_prefix=self.table_name_prefix,
            **kwargs)

        sql = self.__get_show_create_table_sql(name)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql)
                    cursor.fetchone()
                    return collection
                except ProgrammingError:
                    sql = self.__get_create_table_sql(name=name)
                    cursor.execute(sql)
        return collection

    def list_collections(self) -> List[str]:
        """
        List all Vector Collections in this store.

        :return: Names of Vector Collections
        """
        sql = self.__get_list_table_sql()
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return list(map(lambda x: str(x[0])[len(self.table_name_prefix):], rows))

    def delete_collection(self, name: str):
        """
        Delete a Vector Collection with given name
        :param name: The name of the Vector Collection to delete
        :return:
        """
        sql = self.__get_drop_table_sql(name=name)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def __get_show_create_table_sql(self, name: str) -> str:
        assert_legal_table_name(self.table_name_prefix + name)
        return f"""
        SHOW CREATE TABLE {self.table_name_prefix + name};
        """

    def __get_create_table_sql(self, name: str) -> str:
        assert_legal_table_name(self.table_name_prefix + name)
        return f"""
        CREATE TABLE {self.table_name_prefix + name} (
            id VARCHAR(64) NOT NULL,
            vector VECTOR NOT NULL,
            content LONGTEXT NOT NULL,
            metadata JSON NOT NULL,
            PRIMARY KEY (id)
        );
        """

    def __get_list_table_sql(self) -> str:
        assert_legal_table_name(self.table_name_prefix)
        return f"""
        SHOW TABLES LIKE '{self.table_name_prefix}%';
        """

    def __get_drop_table_sql(self, name: str) -> str:
        assert_legal_table_name(self.table_name_prefix + name)
        return f"""
        DROP TABLE {self.table_name_prefix + name};
        """
