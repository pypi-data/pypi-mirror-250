
from typing import Dict, List
from fastembed.embedding import FlagEmbedding
from langchain_community.embeddings import HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings
from langchain_community.embeddings.huggingface import DEFAULT_QUERY_INSTRUCTION, DEFAULT_EMBED_INSTRUCTION
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.embeddings import Embeddings as LangChainEmbedding
from config import EMBEDDING_CONSTANTS
from langchain_core.embeddings import Embeddings
import cloudpickle
import json
from dataclasses import dataclass
import os
from tempfile import TemporaryDirectory

EMBEDDING = 'embeddding'
HF = 'hf'
FASTEMBED = 'fastembed'
TYPE = 'type'


@dataclass
class EmbeddingFile():
    payload: Dict[str, bytes]
    embedding_type: str

    @classmethod
    def from_embedding(cls, embedding):
        if isinstance(embedding, FastEmbedEmbeddings):
            payload = cls.get_fastembed_payload(embedding)
            embedding_type = FASTEMBED
        else:
            payload = {EMBEDDING: embedding}
            embedding_type = HF

        return EmbeddingFile(payload, embedding_type)

    def save(self, path: str):
        with open(path, 'wb') as f:
            cloudpickle.dump(self, f)
        return path

    @classmethod
    def load_embedding(cls, path, **kwargs) -> LangChainEmbedding:
        with open(path, 'rb') as f:
            embedding_file: EmbeddingFile = cloudpickle.load(f)

        if embedding_file.embedding_type == HF:
            if EMBEDDING not in embedding_file.payload:
                raise ValueError(
                    f"File is not ExtractedFile - this might not be a huggingface model")
            return embedding_file.payload[EMBEDDING]  # type: ignore
        elif embedding_file.embedding_type == FASTEMBED:
            return cls.load_fast_embedding(embedding_file.payload, **kwargs)
        raise ValueError(
            f"Unknown embedding type {embedding_file.embedding_type}")

    @classmethod
    def get_fastembed_payload(cls, embedding) -> dict:
        cache_dir = os.path.join(
            str(embedding._model._cache_dir), f"fast-{embedding.model_name.split('/')[1]}")
        assert os.path.isdir(cache_dir)
        return cls.load_fastembed_cache(cache_dir)

    @classmethod
    def load_fastembed_cache(cls, folder_path: str):
        """Convert a folder of files to a single cloudpickled file"""
        data = {}
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                with open(os.path.join(root, file), 'rb') as f:
                    data[file] = f.read()  # type: ignore
        return data

    @classmethod
    def load_fast_embedding(cls, data, **kwargs):
        cache_dir = TemporaryDirectory().name
        model_name = cls.dict_to_cache(data, cache_dir)
        return FastEmbedEmbeddings(model_name=model_name, cache_dir=cache_dir, **kwargs)

    @staticmethod
    def dict_to_cache(data: dict, folder_path: str):
        """save files from data as fastembed cache to a cache folder"""
        if not isinstance(data, dict):
            raise ValueError(
                "File is not extracted file - this might not be a fastembed cache")
        if not isinstance(data, dict) or 'config.json' not in data:
            raise ValueError(
                "'config.json' not found in file after loading - this might not be a fastembed cache")
        config = json.loads(data['config.json'])
        folder_path = os.path.join(
            folder_path, f"fast-{config.get('_name_or_path').split('/')[-1]}")
        for file_path, content in data.items():
            file_dir = os.path.dirname(file_path)
            os.makedirs(os.path.join(folder_path, file_dir), exist_ok=True)
            with open(os.path.join(folder_path, file_path), 'wb') as f:
                f.write(content)
        return config.get('_name_or_path')


def load_embedding(path: str, **kwargs) -> Embeddings:
    return EmbeddingFile.load_embedding(path, **kwargs)


def save_embedding(path: str, embedding: Embeddings) -> str:
    return EmbeddingFile.from_embedding(embedding).save(path)


def get_fast_embedding(model_name: str = EMBEDDING_CONSTANTS.FLAGMODEL_DEFAULT, **kwargs) -> Embeddings:
    """
    Get a fastembed embedding model by name

    Args:
        model_name (str): The name of the model to use.
        max_length (int, optional): The maximum number of tokens. Defaults to 512. Unknown behavior for values > 512.
        cache_dir (str, optional): The path to the cache directory.
                                    Can be set using the `FASTEMBED_CACHE_PATH` env variable.
                                    Defaults to `fastembed_cache` in the system's temp directory.
        threads (int, optional): The number of threads single onnxruntime session can use. Defaults to None.

    Raises:
        ValueError: If the model_name is not in the format <org>/<model> e.g. BAAI/bge-base-en.
    """
    return FastEmbedEmbeddings(model_name=model_name, **kwargs)


def list_fast_models() -> List[dict]:
    """List all fastembed models"""
    return FlagEmbedding.list_supported_models()


def list_instruct_models() -> List[str]:
    """List all instruct models"""
    return EMBEDDING_CONSTANTS.INSTRUCTOR_MODELS


def get_huggingface_embedding(model_name: str = EMBEDDING_CONSTANTS.HUGGINGFACE_DEFAULT, **kwargs) -> Embeddings:
    """Get a huggingface embedding model by name"""
    return HuggingFaceEmbeddings(model_name=model_name, **kwargs)


def get_instruct_embedding(model_name: str = EMBEDDING_CONSTANTS.INSTRUCTOR_DEFAULT,
                           embed_instruction: str = DEFAULT_EMBED_INSTRUCTION,
                           query_instruction: str = DEFAULT_QUERY_INSTRUCTION,
                           **kwargs) -> Embeddings:
    """Get a huggingface embedding model by name"""
    return HuggingFaceInstructEmbeddings(model_name=model_name, embed_instruction=embed_instruction, query_instruction=query_instruction, **kwargs)
