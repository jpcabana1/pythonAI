import os
import json
import requests
import base64
import re

from langchain_community.vectorstores import OpenSearchVectorSearch, VectorStore
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from typing import List
from dotenv import load_dotenv
from loader_service import LoaderService
from asyncio import run


load_dotenv()

def basic_auth(username, password):

    original_string = f"{username}:{password}"

    # Encode the string to bytes
    original_bytes = original_string.encode('utf-8')

    # Encode the bytes to base64
    base64_bytes = base64.b64encode(original_bytes)

    # Convert the base64 bytes back to a string
    base64_string = base64_bytes.decode('utf-8')
    return  f"Basic {base64_string}"
    
def load_embeddings_model() -> Embeddings:
    return AzureOpenAIEmbeddings(
        deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        model=os.getenv("AZURE_OPENAI_MODEL"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        openai_api_type=os.getenv("OPENAI_API_TYPE"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"))
    
def load_opensearch_vectorstore(url: str, index_name: str, embeddings: Embeddings) -> VectorStore:
    return OpenSearchVectorSearch(
        opensearch_url=url, 
        index_name=index_name, 
        embedding_function=embeddings,
        http_auth=(os.getenv("OPENSEARCH_USERNAME"), os.getenv("OPENSEARCH_PASSWORD")),
        use_ssl = False,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False)

def load_vectorstore_opensearch_poc(docs: List[Document], embeddings: Embeddings) -> OpenSearchVectorSearch:
    #If using the default Docker installation, use this instantiation instead:
    return OpenSearchVectorSearch.from_documents(
        documents=docs,
        embedding=embeddings,
        opensearch_url=os.getenv("OPENSEARCH_URL"),
        http_auth=(os.getenv("OPENSEARCH_USERNAME"), os.getenv("OPENSEARCH_PASSWORD")),
        use_ssl = False,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )

def split_document(loader) -> List[Document]:
    documents :List[Document] = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=int(os.getenv("chunk_size")), chunk_overlap=int(os.getenv("chunk_overlap")))
    return text_splitter.split_documents(documents)

def get_index_body():
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

def create_index_if_not_exists(client:VectorStore, index_name:str):
    if not client.index_exists(index_name):
        #client.delete_index(index_name=index_name)
        client.create_index(dimension=1536, index_name=index_name, body=get_index_body())

def convert_text(result_text) -> str:
    # Remove half non-ascii character from start/end of doc content (langchain TokenTextSplitter may split a non-ascii character in half)
    # do not remove \x0a (\n) nor \x0d (\r)
    pattern = re.compile(
            r'[\x00-\x09\x0b\x0c\x0e-\x1f\x7f\u0080-\u00a0\u2000-\u3000\ufff0-\uffff]')
    converted_text = re.sub(pattern, '', "\n".join(result_text))
    return converted_text

def remove_non_ascii(docs:List[Document]):
    for doc in docs:
        doc.page_content = convert_text(doc.page_content)
        if doc.page_content == '':
            docs.remove(doc)

async def aingest_document(client:VectorStore, url:str):
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
    client.add_documents(documents=splitted_docs)

def search_documents(query:str, client:VectorStore):
    docs = client.similarity_search(query, k=10)
    return docs[0].page_content

def highlight_search(query:str):
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
    'Authorization': basic_auth(os.getenv("OPENSEARCH_USERNAME"), os.getenv("OPENSEARCH_PASSWORD"))
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    try:
        print(json.dumps(response.json()["hits"]["hits"][0], indent=2))
    except Exception:
        print(json.dumps(response.json()["hits"], indent=2))

async def aingest_document_url(url:str):
    index_name = os.getenv("OPENSEARCH_INDEX_NAME")
    client = load_opensearch_vectorstore(url=os.getenv("OPENSEARCH_URL"), embeddings=load_embeddings_model(), index_name=index_name)
    create_index_if_not_exists(client=client, index_name=index_name)
    await aingest_document(client=client, url=url)

async def main():
    urls = [
    ]
      
    #await aingest_document_url(url=urls[2])
      
    #Indexing
    # for url in urls:
    #     try:
    #         await aingest_document_url(url=url)
    #     except Exception as e:
    #         print(f"failed to load url: {url}")
    #         print(e)
    
    #similarity_search
    # print(search_documents(query=query, client=client))
    
    #highlight search
    query = input("Enter a text query: ")
    while query != "exit":
        highlight_search(query=query)
        query = input("Enter a text query: ")
    

if __name__ == "__main__":
    run(main())

