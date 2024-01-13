from cria_index.core import VectorStore

class QdrantVectorStore(VectorStore):
    @classmethod
    def class_name(cls):
        return "QdrantVectorStore"