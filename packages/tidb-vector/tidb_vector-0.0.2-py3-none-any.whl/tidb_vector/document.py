from typing import List


class VectorDocument:
    """
    Represents a document of a Vector Collection
    """

    id: str
    """
    Identifier of the document.
    """

    vector: List[float]
    """
    The vector value of the document.
    """

    content: str
    """
    The raw content of the document.
    """

    metadata: dict
    """
    Metadata of the document.
    """

    def __init__(self, document_id: str, vector: List[float], content: str, metadata: dict):
        self.id = document_id
        self.vector = vector
        self.content = content
        self.metadata = metadata


class VectorDocumentSearchResult:
    id: str
    content: str
    metadata: str
    similarity: float

    def __init__(self, document_id: str, content: str, metadata: str, similarity: float):
        self.id = document_id
        self.content = content
        self.metadata = metadata
        self.similarity = similarity

    def __str__(self):
        return f"VectorDocumentSearchResult<similarity = {self.similarity}, {self.content}>"
