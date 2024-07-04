import os
import re
import requests
import boto3
from dotenv import load_dotenv
from asyncio import sleep
from asyncio import run
import datetime

class TranscribeService:
    
    def __init__(self) -> None:
        self.__client = boto3.client(
        'transcribe',
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
    
    def get_transcription_job_name(self, video_uri:str) -> str:
        formated_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        pattern = re.compile(r":|\/|\.")
        job_name = re.sub(pattern=pattern, repl="", string=f"job-{formated_time}{video_uri}")
        return job_name[:200]

    def get_transcription_job(self, job_name, client):
        return client.get_transcription_job(TranscriptionJobName=job_name)
    
    async def transcribe_video(self, video_uri:str, language_code:str, media_format:str):
        job_name=self.get_transcription_job_name(video_uri=video_uri)
        
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
        
        # Get TranscriptionJob
        response = self.get_transcription_job(job_name=job_name, client=self.__client)
        
        # Await TranscriptionJob result
        while response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED":
            response = self.get_transcription_job(job_name=job_name, client=self.__client)
            status = str(response["TranscriptionJob"]["TranscriptionJobStatus"])
            print(f"Current TranscriptionJobStatus: {status}")
            await sleep(2)
        
        url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcription_job_response = requests.request("GET", url, headers={}, data={})
        response = self.__client.delete_transcription_job(TranscriptionJobName=job_name)
        
        return transcription_job_response.json()["results"]["transcripts"][0]["transcript"]
    
async def main():
    video_uri = "s3://test-bucket-plataforma/3f80ee70-2367-11eb-a3ad-9f132a537bed_S20-2-PLA61-9-01-OAU-003.mp4"
    language_code="pt-BR"
    media_format="mp4"
    transcription = await TranscribeService().transcribe_video(video_uri=video_uri, language_code=language_code, media_format=media_format)
    print(transcription)

if __name__ == "__main__":
    load_dotenv()
    run(main())