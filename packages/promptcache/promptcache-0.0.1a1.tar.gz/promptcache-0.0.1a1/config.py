class EMBEDDING_CONSTANTS:
    FLAGMODEL_DEFAULT = 'BAAI/bge-small-en-v1.5'
    HUGGINGFACE_DEFAULT = 'sentence-transformers/all-MiniLM-L6-v2'
    INSTRUCTOR_DEFAULT = 'hkunlp/instructor-base'
    INSTRUCTOR_MODELS = ["hkunlp/instructor-base",
                         "hkunlp/instructor-large", "hkunlp/instructor-xl"]


class REDIS_PARAMS:
    URL = 'redis://localhost:6379'
    INDEX = 'cache'
    VECTOR_SCHEMA = {
        "algorithm": "HNSW"
    }
