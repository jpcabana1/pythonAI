from dotenv import load_dotenv
from asyncio import run
from opensearch_service import OpenSearchService

async def main():
    ursls = [
    ]
    
    service = OpenSearchService()
    #await service.aingest_document_url(url=urls[2])
      
    #Indexing
    # for url in urls:
    #     try:
    #         await service.aingest_document_url(url=url)
    #     except Exception as e:
    #         print(f"failed to load url: {url}")
    #         print(e)
    
    #similarity_search
    # print(service.search_documents(query=query, client=client))
    
    
    
    #highlight search
    query = input("Enter a text query: ")
    while query != "exit":
        # response = service.similarity_search(query=query)
        # print(response)
        service.highlight_search(query=query)
        query = input("Enter a text query: ")
    

if __name__ == "__main__":
    load_dotenv()
    run(main())

