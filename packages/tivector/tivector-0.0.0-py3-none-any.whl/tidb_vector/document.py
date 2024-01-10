class VectorDocument:
    """
    Represents a document of a Vector Collection
    """

    id: str
    """
    Identifier of the document
    """

    vector: [float]
    """
    The vector value of the document.
    """

    content: str
    """
    The raw content of the document.
    """

    meta: dict
    """
    
    """
