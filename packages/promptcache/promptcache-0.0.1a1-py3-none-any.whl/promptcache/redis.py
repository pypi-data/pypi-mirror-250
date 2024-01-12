import contextlib
from typing import Iterable, List, Optional, Tuple, Union
from config import REDIS_PARAMS
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_community.vectorstores.redis import Redis
from promptcache.embedding import get_fast_embedding, load_embedding
from typing import Any, Dict, Optional, Awaitable
import xxhash
from redis.exceptions import ResponseError


class RedisCache(object):
    PROMPT = 'prompt'
    COMPLETION = 'completion'
    DISTANCE = 'distance'
    DOC = 'doc'
    MODEL_NAME = 'embedding_name'

    def __init__(self,
                 url: str = REDIS_PARAMS.URL,
                 embedding: Optional[Embeddings] = None,
                 index: str = REDIS_PARAMS.INDEX,
                 vector_schema: dict = REDIS_PARAMS.VECTOR_SCHEMA,
                 **kwargs):
        if embedding is None:
            embedding = get_fast_embedding()
        elif isinstance(embedding, str):
            embedding = load_embedding(embedding)
        self.index = index
        self.vectorstore: Redis = Redis.from_texts(
            texts=[''],
            metadatas=[{RedisCache.COMPLETION: ''}],
            redis_url=url,
            embedding=embedding,
            index_name=index,
            vector_schema=vector_schema, **kwargs)
        temp_id = self.search('', return_id=True).get('id', '')
        self.vectorstore.delete([temp_id], redis_url=url)
        if self.db_embedding_name and self.db_embedding_name != self.embedding_name:
            raise RuntimeError(
                f"""embedding name mismatch\n
                Current data is embedded with {self.db_embedding_name} but a new embedding model {self.embedding_name} provided"
                Consider using the same embedding model or flush the db with `RedisCache.flushdb(url)`
                """)
        self.client.set(RedisCache.MODEL_NAME, self.embedding_name)

    @property
    def db_embedding_name(self) -> Optional[str]:
        """embedding name which is persistant in db"""
        result = self.client.get(RedisCache.MODEL_NAME)
        if result:
            return result.decode('utf-8')  # type: ignore

    @property
    def embedding_name(self):
        """embedding name which is provided by user"""
        return self.vectorstore.embeddings.model_name  # type: ignore

    @property
    def client(self):
        return self.vectorstore.client

    @classmethod
    def flushdb(cls, url: str):
        import redis
        return redis.from_url(url).flushdb()

    @property
    def embedding(self) -> Embeddings:
        return self.vectorstore.embedding  # type: ignore

    @staticmethod
    def _hash_doc(content: str) -> str:
        return xxhash.xxh64(str(content).strip()).hexdigest()

    def to_texts(self, documents=List[Union[str, dict]]) -> tuple[List[str], List[str], List[dict]]:
        """Converts a list of documents to a list of prompts and a list of metadata"""
        # TODO handle long texts
        keys, docs, metadatas = [], [], []
        for document in documents:  # type: ignore
            text = document if isinstance(
                document, str) else document[RedisCache.PROMPT]
            keys.append(self._hash_doc(text))
            docs.append(text)
            metadatas.append(document if isinstance(document, dict) else {})
        return keys, docs, metadatas

    def topk(self, query: str, topk: Optional[int] = None, **kwargs) -> Optional[List[dict]]:
        """Query the cache"""
        topk = topk or self.topk
        with contextlib.suppress(ResponseError):
            return self._parse_document(self.vectorstore.similarity_search_with_score(query=query, k=topk, **kwargs))
        return []

    def search(self, query: str, return_id: bool = False) -> Optional[dict]:
        """Query the cache for exact or similar prompt"""
        result = self.get(prompt=query)
        if result is not None:
            return {RedisCache.COMPLETION: result, RedisCache.DISTANCE: 0, RedisCache.PROMPT: query}
        with contextlib.suppress(ResponseError):
            results = self._parse_document(
                self.vectorstore.similarity_search_with_score(query=query, k=1))
            if results:
                result = results[0]
                if not return_id:
                    result.pop('id')
                return result

    @staticmethod
    def _parse_document(documents: List[Tuple[Document, float]]) -> Optional[List[dict]]:
        results = []
        for document in documents:
            doc = document[0].metadata
            doc[RedisCache.PROMPT] = document[0].page_content
            doc[RedisCache.DISTANCE] = document[1]
            # metadata
            results.append(doc)
        return results

    def set(self, prompt: str, compleation: str) -> bool:
        """Add a prompt to cache. Returns True if added"""
        if not prompt:
            return False
        self.vectorstore.add_texts(
            [prompt], [{RedisCache.COMPLETION: compleation}], keys=[self._hash_doc(prompt)])
        return True

    def _to_key(self, prompt: str) -> str:
        return f"{RedisCache.DOC}:{self.index}:{self._hash_doc(prompt)}"

    def get(self, prompt:  str, default=None) -> Union[Awaitable[Optional[str]], Optional[str]]:
        """Return the compleation if exists"""
        result = self.vectorstore.client.hget(
            self._to_key(prompt), RedisCache.COMPLETION)
        if isinstance(result, bytes):
            return result.decode('utf-8')
        return default

    def delete(self, prompt: str) -> bool:
        """Delete a prompt from cache. Returns True if deleted"""
        return self.vectorstore.client.delete(self._to_key(prompt)) == 1

    def keys(self) -> Iterable[str]:
        for key in self.vectorstore.client.scan_iter(f"{RedisCache.DOC}:{self.index}:*"):
            yield key.decode('utf-8').split(':')[-1]
