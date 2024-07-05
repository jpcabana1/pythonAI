
import os
from transcribe.transcribe import TranscribeService
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader, TextLoader
from typing import List
from utils.helper_file import HelperTempFile
from requests import Response

class LoaderService:
    
    def __init__(self) -> None:
        self.__helper = HelperTempFile()
        self.__trservice = TranscribeService()
    
    def is_video(self, url) -> bool:
        try:
            return self.__helper.get_file_extension(url) == ".mp4"
        except Exception:
            return False
    
    
    async def load(self, url: str, response:Response) -> List[Document]:
        
        converted_filename=self.__helper.convert_file_name(url=url, size=50)
        output_path = self.__helper.get_output_file_name(converted_filename=converted_filename, content_type=response.headers.get("Content-Type"))
        print(output_path)
        try:
            self.__helper.save_response_as_temp_file(file_path=output_path, response=response)
        except Exception as e:
            print(e)
            self.__helper.delete_file_if_exists(output_path)
        
        #Identify file extension
        file_extension = self.__helper.get_file_extension(output_path)
        
        documents : List[Document] = []
        #Select Loader
        if file_extension == ".html" or file_extension == ".htm":
            documents = UnstructuredHTMLLoader(file_path=output_path).load()
        elif  file_extension == ".txt":
            documents = TextLoader(file_path=output_path, encoding='utf-8').load()
        elif file_extension == ".pdf":
            documents = PyPDFLoader(file_path=output_path).load()
        else:
            documents = []
            
        self.__helper.delete_file_if_exists(output_path)
            
        return documents
    
    async def load_transcription(self, s3_url:str) -> List[Document]:
        transcription = await self.__trservice.transcribe_video(video_uri=s3_url)
        text_splitter = CharacterTextSplitter(chunk_size=int(os.getenv("chunk_size")), chunk_overlap=int(os.getenv("chunk_overlap")))
        texts = [transcription]
        documents : List[Document] = text_splitter.create_documents(texts=texts) 
        return documents
            