from azure_embeddings import generate_embeddings
import os
import openai
import PyPDF2

#from langchain_text_splitters import CharacterTextSplitter



# Function to read the PDF
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# # Function to get embeddings from Azure OpenAI
# def get_embedding(text):
#     response = openai.Embedding.create(
#         input=text,
#         engine="text-embedding-ada-002"  # Ensure this matches your deployed model
#     )
#     return response['data'][0]['embedding']

# # Set up your Azure OpenAI credentials
# os.environ["OPENAI_API_KEY"] = "your-azure-openai-api-key"
# os.environ["OPENAI_API_BASE"] = "your-azure-openai-endpoint"


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
# Example usage
def main():
    filename = "data/João_Pedro_De_Melo_CabanaOWASP.pdf"
    loader = PyPDFLoader(filename)
    pages = loader.load()
    
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False)
    
    docs = text_splitter.split_documents(pages)
    payload = []
    for chunk in docs:
        #print(chunk.page_content)
        document = {
            "filename": filename,
            "text": chunk.page_content,
            # "embeddings": generate_embeddings(chunk)
        }
        #print(generate_embeddings(chunk.page_content).data[0].embedding)
        payload.append(document)
    print(payload)
    
    
    
    # # Read the PDF
    # pdf_text = read_pdf("data/9140604000554-ftd-se-em-cnt-biologia-vol13-18-miolo-prof-001-33.pdf")  #Replace with your PDF file path
    
    # # Create chunks
    # text_splitter = CharacterTextSplitter(
    # separator="\n\n",
    # chunk_size=100,
    # chunk_overlap=20,
    # length_function=len,
    # is_separator_regex=False)
    
    # chunks = text_splitter.split_text(pdf_text)

    # print(len(chunks))
    # # Generate embeddings for the chunks
    # embeddings = [generate_embeddings(chunk)['data'][0]['embedding'] for chunk in chunks]
    
    # print("Chunks:")
    # for chunk in chunks:
    #     print(chunk)
    
    # print("\nEmbeddings:")
    # for embedding in embeddings:
    #     print(embedding)

if __name__ == "__main__":
    main()


#print(generate_embeddings("Hello world!").model_dump_json(indent=2))