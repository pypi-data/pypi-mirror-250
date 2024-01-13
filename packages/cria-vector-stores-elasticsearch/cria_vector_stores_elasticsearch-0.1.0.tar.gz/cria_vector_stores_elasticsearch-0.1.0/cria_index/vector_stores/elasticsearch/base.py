from cria_index.core import VectorStore

class ElasticSearchVectorStore(VectorStore):
    @classmethod
    def class_name(cls):
        return "ElasticSearchVectorStore"