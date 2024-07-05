import os
import json
import requests
import base64
from typing import List
from langchain_community.vectorstores import OpenSearchVectorSearch, VectorStore
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from loader_service import LoaderService

class OpenSearchService:
    def __init__(self) -> None:
        self.__opensearch_url = os.getenv("OPENSEARCH_URL")
        self.__opensearch_index_name = os.getenv("OPENSEARCH_INDEX_NAME")
        self.__client :VectorStore = self.load_opensearch_vectorstore(
            url=self.__opensearch_url, 
            embeddings=self.load_embeddings_model(),
            index_name=self.__opensearch_index_name)
        pass
    
    def basic_auth(self, username, password):

        original_string = f"{username}:{password}"

        # Encode the string to bytes
        original_bytes = original_string.encode('utf-8')

        # Encode the bytes to base64
        base64_bytes = base64.b64encode(original_bytes)

        # Convert the base64 bytes back to a string
        base64_string = base64_bytes.decode('utf-8')
        return  f"Basic {base64_string}"
        
    def load_embeddings_model(self) -> Embeddings:
        return AzureOpenAIEmbeddings(
            deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            model=os.getenv("AZURE_OPENAI_MODEL"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_type=os.getenv("OPENAI_API_TYPE"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"))
        
    def load_opensearch_vectorstore(self, url: str, index_name: str, embeddings: Embeddings) -> VectorStore:
        return OpenSearchVectorSearch(
            opensearch_url=url, 
            index_name=index_name, 
            embedding_function=embeddings,
            http_auth=(os.getenv("OPENSEARCH_USERNAME"), os.getenv("OPENSEARCH_PASSWORD")),
            use_ssl = False,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False)

    def get_index_body(self):
        return {
            "mappings": {
                "properties": {
                "id": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text"
                },
                "content": {
                    "type": "text"
                },
                "content_vector": {
                    "type": "nested",
                    "properties": {
                    "knn": {
                        "type": "knn_vector",
                        "dimension": 1536
                    }
                    }
                },
                "tag": {
                    "type": "text"
                },
                "metadata": {
                    "type": "text"
                }
                }
            }
            }

    def create_index_if_not_exists(self, index_name:str):
        if not self.__client.index_exists(index_name):
            self.__client.create_index(dimension=1536, index_name=index_name, body=self.get_index_body())

    async def aingest_document(self, url:str):
        documents :List[Document] = []
        loader_service = LoaderService()
        
        if loader_service.is_video(url=url):
            print("transcribing video...")
            documents = await loader_service.load_transcription(s3_url=url)
        else:
            print("dowloading file...")
            response = requests.get(url, timeout=240)
            documents = await loader_service.load(url=url, response=response)
            
        text_splitter = CharacterTextSplitter(chunk_size=int(os.getenv("chunk_size")), chunk_overlap=int(os.getenv("chunk_overlap")))
        splitted_docs :List[Document] = text_splitter.split_documents(documents)
        self.__client.add_documents(documents=splitted_docs)

    async def aingest_document_url(self, url:str):
        index_name = os.getenv("OPENSEARCH_INDEX_NAME")
        self.create_index_if_not_exists(client=self.__client, index_name=index_name)
        await self.aingest_document(client=self.__client, url=url)

    def similarity_search(self, query:str):
        docs = self.__client.similarity_search(query, k=10)
        return docs[0].page_content
            
    def highlight_search(self, query:str):
        base=os.getenv("OPENSEARCH_URL")
        index=os.getenv("OPENSEARCH_INDEX_NAME")
        url = f"{base}/{index}/_search"
        print(url)
        payload = json.dumps({
        "_source": {
            "excludes": [
            "text",
            "vector_field"
            ]
        },
        "query": {
            "match": {
            "text": f"{query}"
            }
        },
        "size": 3,
        "highlight": {
            "fields": {
            "text": {}
            }
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': self.basic_auth(os.getenv("OPENSEARCH_USERNAME"), os.getenv("OPENSEARCH_PASSWORD"))
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        try:
            print(json.dumps(response.json()["hits"]["hits"][0], indent=2))
        except Exception:
            print(json.dumps(response.json()["hits"], indent=2))
