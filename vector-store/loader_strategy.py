import os
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader, TextLoader

class LoaderStrategy:
    def __init__(self) -> None:
        pass
    
    def __get_file_extension(self, filepath):
        _, file_extension = os.path.splitext(filepath)
        return file_extension.lstrip('.')

    def get_loader(self, file_path: str) -> BaseLoader:
        
        #Identify file extension
        file_extension = self.__get_file_extension(file_path)
        
        #Select Loader
        if file_extension == "html" or file_extension == "htm":
            return UnstructuredHTMLLoader(file_path=file_path)
        elif  file_extension == "txt":
            return TextLoader(file_path=file_path, encoding='utf-8')
        elif  file_extension == "pdf":
            return PyPDFLoader(file_path=file_path)
        else:
            return None
        