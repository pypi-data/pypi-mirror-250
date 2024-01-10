from typing import Union

from tidb_vector.collection import VectorCollection
from tidb_vector.config import ConnectionConfig
from tidb_vector.exceptions import VectorCollectionValidationException


class VectorStore:
    def __init__(
            self,
            connection_config: ConnectionConfig,
            table_name_prefix: str = 'vector_collection_',
    ):
        """
        Connect to a TiDB Vector Store.

        :param connection_config: TiDB connection config
        :param table_name_prefix: Table prefix for Vector Collections
        """
        pass

    def open_collection(
            self,
            name: str,
            dimensions: int,
            m: int,
            ef_construction: int
    ) -> VectorCollection:
        """
        Open and verify a Vector Collection with given name, if not exists, will create one with config.

        :param name: The name of the Vector Collection (without prefix)
        :param dimensions: The dimensions of the Vector Collection
        :param m: TODO
        :param ef_construction: TODO
        :return: A Vector Collection
        """
        collection = self.__connect_collection(name)
        if collection is None:
            collection = self.__create_collection(name, dimensions, m, ef_construction)
        if not self.__verify_collection(name, dimensions, m, ef_construction):
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
        pass

    def __create_collection(
            self,
            name: str,
            dimensions: int,
            m: int,
            ef_construction: int
    ) -> VectorCollection:
        """
        Create a new Vector Collection with given options
        :param name: Name of the Vector Collection
        :param dimensions: The dimensions of the Vector Collection
        :param m: TODO
        :param ef_construction: TODO
        :return: A Vector Collection
        """
        pass

    def __verify_collection(
            self,
            name: str,
            dimensions: int,
            m: int,
            ef_construction: int
    ) -> bool:
        """
        Verify a Vector Collection with given options.
        :param name: Name of the Vector Collection
        :param dimensions: The dimensions of the Vector Collection
        :param m: TODO
        :param ef_construction: TODO
        :return: Whether the Vector Collection's options are matched with given options.
        """
        pass
