from dotenv import load_dotenv
from asyncio import run
from opensearch.opensearch_service import OpenSearchService

async def main():
    service = OpenSearchService()
    
    #highlight search
    query = input("Enter a text query: ")
    while query != "exit":
        if query == "ingest":
            url = input("file url: ")
            try:
                await service.aingest_document_url(url=url)
                print("Ingestion completed.")
                query=""
            except Exception as e:
                print(f"failed to load url: {url}")
                print(e)
                query=""
        else:
            service.highlight_search(query=query)
            query = input("Enter a text query: ")
    

if __name__ == "__main__":
    load_dotenv()
    run(main())

