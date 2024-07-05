import os
import datetime
import re
from io import BytesIO
from requests import Response

class HelperTempFile:
    
    def __init__(self) -> None:
        pass
    
    def get_file_extension(self, filepath:str) -> str:
        pattern = r'\.html|\.html|\.mp4|\.txt|\.pdf'
        res = re.search(pattern, string=filepath)
        return res.group()
    
    def get_file_extension_from_content_type(self, content_type:str) -> str:
        extensions ={
            "text/plain":".txt",
            "video/mp4":".mp4",
            "text/html; charset=utf-8":".html",
            "application/pdf":".pdf",
        }
        return extensions.get(content_type)
    
    def save_response_as_temp_file(self, file_path:str, response:Response) -> None:
        byte_io = BytesIO()
        byte_io.write(response.content)
        
        byte_io.seek(0)
        with open(file_path, 'wb') as file:
            file.write(byte_io.read())
            
    def delete_file_if_exists(self, output_path:str):
        if os.path.exists(output_path):
            os.remove(output_path)
            
    def convert_file_name(self, url: str, size:int) -> str:
        pattern = re.compile(r":|\/|\.|\-")
        formated_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        name = formated_time + re.sub(pattern=pattern, repl="", string=url)
        return name[:size]
           
    
    def get_output_file_name(self, converted_filename:str, content_type:str) -> str:
        return f"dumps/{converted_filename}{self.get_file_extension_from_content_type(content_type)}"