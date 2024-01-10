# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Index stores for uploading and deleting documents."""
import base64
import time
import json

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional
from pymongo import UpdateOne, DeleteOne
from pymongo.collection import Collection

from azure.core import CaseInsensitiveEnumMeta
from azureml.rag.utils.logging import get_logger


INDEX_DELETE_FAILURE_MESSAGE_PREFIX = "Failed to delete"
INDEX_UPLOAD_FAILURE_MESSAGE_PREFIX = "Failed to upload"


class IndexStoreType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """IndexStoreType."""

    ACS = "ACS"
    PINECONE = "Pinecone"
    MILVUS = "Milvus"
    AZURE_COSMOS_MONGO_VCORE = "AzureCosmosMongoVcore"


logger = get_logger(__name__)


class IndexStore(ABC):
    """An index store used for uploading and deleting documents.

    This class should not be instantiated directly. Instead, use one of its subclasses.
    """

    def __init__(self, type: IndexStoreType):
        """Initialize the IndexStore."""
        self._type = type

    @property
    def type(self) -> IndexStoreType:
        """The type of the index."""
        return self._type

    @abstractmethod
    def delete_documents(self, documents: List[Any]):
        """Delete documents from the index.

        Raises:
            `RuntimeError` if all documents are not deleted from the index.
        """
        pass

    @abstractmethod
    def upload_documents(self, documents: List[Any]):
        """Upload documents to the index.

        Raises:
            `RuntimeError` if all documents are not uploaded to the index.
        """
        pass

    @abstractmethod
    def create_delete_payload_from_document_id(self, document_id: str) -> Any:
        """
        Given a document ID, construct a payload used to delete the corresponding
        document from the index.
        """
        pass

    @abstractmethod
    def create_upload_payload_from_embedded_document(
        self,
        field_mappings: dict,
        document_id: str,
        document_source_info: dict = {},
        document_data: Optional[str] = None,
        document_embeddings: Optional[List[float]] = None,
        document_metadata: Optional[dict] = None
    ) -> Any:
        """
        Given info about an EmbeddedDocument, construct a payload used to upload the document
        to the index.
        """
        pass


class AzureCosmosMongoVcoreStore(IndexStore):
    """An Azure Cosmos Mongo vCore index store used for uploading and deleting documents."""

    def __init__(self, mongo_collection: Collection):
        """Initialize the AzureCosmosMongoVcoreStore."""
        super().__init__(IndexStoreType.AZURE_COSMOS_MONGO_VCORE)
        self._mongo_collection = mongo_collection

    def delete_documents(self, documents: List[Any]):
        """Delete documents from the index.

        Raises:
            `RuntimeError` if all documents are not deleted from the index.
        """
        start_time = time.time()
        results = self._mongo_collection.bulk_write(documents)

        encountered_write_errors = (len(results.bulk_api_result.get("writeErrors", [])) + len(results.bulk_api_result.get("writeConcernErrors", []))) > 0
        deleted_count = results.deleted_count
        total_count = len(documents)
        failed_deleted_count = total_count - deleted_count
        if not encountered_write_errors and failed_deleted_count > 0:
            logger.info(
                f"Failed to delete {failed_deleted_count} documents but there were no write errors, assuming these documents were duplicates and treating "
                f"as if though all {total_count} documents were successfully deleted."
            )
            deleted_count = total_count
            failed_deleted_count = 0

        duration = time.time() - start_time
        logger.info(
            f'[{self.__class__.__name__}][{self.delete_documents.__name__}] Deleted {deleted_count} documents in {duration:.4f} seconds.')
        logger.info(
            f'[{self.__class__.__name__}][{self.delete_documents.__name__}] Full bulk write result: {results.bulk_api_result}')

        if failed_deleted_count > 0:
            raise RuntimeError(f"{INDEX_DELETE_FAILURE_MESSAGE_PREFIX} {failed_deleted_count} documents")

    def upload_documents(self, documents: List[Any]):
        """Upload documents to the index.

        Raises:
            `RuntimeError` if all documents are not uploaded to the index.
        """
        start_time = time.time()
        results = self._mongo_collection.bulk_write(documents)

        encountered_write_errors = (len(results.bulk_api_result.get("writeErrors", [])) + len(results.bulk_api_result.get("writeConcernErrors", []))) > 0
        uploaded_count = results.upserted_count + results.modified_count
        total_count = len(documents)
        failed_uploaded_count = total_count - uploaded_count
        matched_count = results.matched_count

        # This means all documents were already in the collection AND did not need to be modified
        if not encountered_write_errors and uploaded_count == 0 and matched_count == total_count:
            logger.info(
                f"No documents were upserted or modified and there were no write errors, assuming this means they were already in the collection "
                f"and did not need to be modified (ie, no new updates), treating as if though all {total_count} documents were successfully uploaded."
            )
            uploaded_count = total_count
            failed_uploaded_count = 0

        duration = time.time() - start_time
        logger.info(
            f'[{self.__class__.__name__}][{self.upload_documents.__name__}] Uploaded {uploaded_count} documents in {duration:.4f} seconds.')
        logger.info(
            f'[{self.__class__.__name__}][{self.upload_documents.__name__}] Full bulk write result: {results.bulk_api_result}')

        if failed_uploaded_count > 0:
            raise RuntimeError(f"{INDEX_UPLOAD_FAILURE_MESSAGE_PREFIX} {failed_uploaded_count} documents")

    def create_delete_payload_from_document_id(self, document_id: str) -> Any:
        """
        Given a document ID, construct a payload used to delete the corresponding
        document from the index.
        """
        return DeleteOne({"_id": base64.urlsafe_b64encode(document_id.encode("utf-8")).decode("utf-8")})

    def create_upload_payload_from_embedded_document(
        self,
        field_mappings: dict,
        document_id: str,
        document_source_info: dict = {},
        document_data: Optional[str] = None,
        document_embeddings: Optional[List[float]] = None,
        document_metadata: Optional[dict] = None
    ) -> Any:
        """
        Given info about an EmbeddedDocument, construct a payload used to upload the document
        to the index.
        """
        if document_data is None or document_embeddings is None or document_metadata is None:
            raise ValueError("One or more of document data, embeddings, metadata is missing")

        doc_source = document_source_info

        doc_id_encoded = base64.urlsafe_b64encode(document_id.encode("utf-8")).decode("utf-8")
        azure_cosmos_mongo_vcore_doc = {
            "_id": doc_id_encoded,
            field_mappings["embedding"]: document_embeddings,
            field_mappings["content"]: document_data,
        }
        if "url" in field_mappings:
            azure_cosmos_mongo_vcore_doc[field_mappings["url"]] = doc_source.get("url", "")
        if "filename" in field_mappings:
            azure_cosmos_mongo_vcore_doc[field_mappings["filename"]] = doc_source.get("filename", "")
        if "title" in field_mappings:
            azure_cosmos_mongo_vcore_doc[field_mappings["title"]] = doc_source.get("title", document_metadata.get("title", ""))
        if "metadata" in field_mappings:
            azure_cosmos_mongo_vcore_doc[field_mappings["metadata"]] = json.dumps(document_metadata)

        return UpdateOne({"_id": doc_id_encoded}, {"$set": azure_cosmos_mongo_vcore_doc}, upsert=True)
