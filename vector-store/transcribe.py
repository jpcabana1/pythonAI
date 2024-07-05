import os
import re
import requests
import boto3
import datetime
from asyncio import sleep
from helper_file import HelperTempFile

class TranscribeService:
    
    def __init__(self) -> None:
        self.__helper_file = HelperTempFile()
        self.__client = boto3.client(
        'transcribe',
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
    
    def get_transcription_job_name(self, video_uri:str) -> str:
        formated_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        pattern = re.compile(r'[^0-9a-zA-Z._-]')
        job_name = re.sub(pattern=pattern, repl="", string=f"job-{formated_time}{video_uri}")
        return job_name[:200]

    def get_transcription_job(self, job_name, client):
        return client.get_transcription_job(TranscriptionJobName=job_name)
    
    async def transcribe_video(self, video_uri:str, language_code:str="pt-BR", media_format:str="mp4"):
        job_name=self.get_transcription_job_name(video_uri=video_uri)
        print(job_name)
        # Create TranscriptionJob
        try:         
            self.__client.start_transcription_job(
                TranscriptionJobName=job_name,
                LanguageCode=language_code,
                MediaFormat=media_format,  # Adjust based on your audio file format
                Media={
                    'MediaFileUri': video_uri
                }
            )
            print(f"job_name: {job_name}")
        except Exception as e:
            print(f"Error when creating transcription Job")
            print(e)
            return
        
        # Get TranscriptionJob
        response = self.get_transcription_job(job_name=job_name, client=self.__client)
        
        # Await TranscriptionJob result
        while response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED" and response["TranscriptionJob"]["TranscriptionJobStatus"] != "FAILED":
            response = self.get_transcription_job(job_name=job_name, client=self.__client)
            status = str(response["TranscriptionJob"]["TranscriptionJobStatus"])
            print(f"Current TranscriptionJobStatus: {status}")
            await sleep(2)
        
        url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcription_job_response = requests.request("GET", url, headers={}, data={})
        response = self.__client.delete_transcription_job(TranscriptionJobName=job_name)
        
        return transcription_job_response.json()["results"]["transcripts"][0]["transcript"]