import os
import re
import requests
import boto3
import datetime
from dotenv import load_dotenv
from asyncio import sleep
from asyncio import run
import concurrent.futures
import time

class TranscribeService:
    
    def __init__(self) -> None:
        self.__client = boto3.client(
        'transcribe',
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=os.getenv("region_name")
        )
        
    def __init__(self, region_name:str) -> None:
        self.__client = boto3.client(
        'transcribe',
            aws_access_key_id=os.getenv("aws_access_key_id"),
            aws_secret_access_key=os.getenv("aws_secret_access_key"),
            region_name=region_name
        )
    
    def get_transcription_job_name(self, video_uri:str) -> str:
        formated_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        pattern = re.compile(r":|\/|\.")
        job_name = re.sub(pattern=pattern, repl="", string=f"job-{formated_time}{video_uri}")
        return job_name[:200]

    def get_transcription_job(self, job_name, client):
        result = None
        try:
            result = client.get_transcription_job(TranscriptionJobName=job_name)
        except:
            result = client.get_transcription_job(TranscriptionJobName=job_name)
        
        return result
    
    def await_transcription_job(self, job_name):
        response = self.get_transcription_job(job_name=job_name, client=self.__client)
    
        print("Awaiting TranscriptionJob to complete...")
        while response["TranscriptionJob"]["TranscriptionJobStatus"] == "IN_PROGRESS":
            response = self.get_transcription_job(job_name=job_name, client=self.__client)
                
        return response
    
    def print_job_details(self, response):
       return f"""Job Name: {response["TranscriptionJob"]["TranscriptionJobName"]}
Job Status: {response["TranscriptionJob"]["TranscriptionJobStatus"]}
Job CreationTime: {response["TranscriptionJob"]["CreationTime"]}
Job CompletionTime: {response["TranscriptionJob"]["CompletionTime"]}
Job ElapsedTime: {self.get_elapsed_time(response=response)}
Job LanguageCode: {response["TranscriptionJob"]["LanguageCode"]}
Job MediaFormat: {response["TranscriptionJob"]["MediaFormat"]}
        """
    
    def get_elapsed_time(self, response):
        creation_time_str = str(response["TranscriptionJob"]["CreationTime"])
        completion_time_str = str(response["TranscriptionJob"]["CompletionTime"])

        from datetime import datetime as dt
        creation_time = dt.fromisoformat(creation_time_str)
        completion_time = dt.fromisoformat(completion_time_str)

        return completion_time - creation_time
        
    def validate_url(self, url:str) -> str:
        pattern = r'\.mp3|\.mp4|\.wav|\.flac|\.ogg|\.amr|\.webm|\.m4a'
        res = re.search(pattern, string=url)
        return re.sub(pattern=r'\.', repl="", string=res.group())
    
    def start_job(self, video_uri:str):
        job_name=self.get_transcription_job_name(video_uri=video_uri)
        media_format = self.validate_url(video_uri)

        #return job_name
        
        try:
            print(f"job_name: {job_name}\nmedia_format: {media_format}")      
            self.__client.start_transcription_job(
                TranscriptionJobName=job_name,
                IdentifyLanguage=True,
                MediaFormat=media_format,
                Media={
                    'MediaFileUri': video_uri
                }
            )
            
            return job_name
        except Exception as e:
            print(f"Error when creating transcription Job\n{e}")
            return ""
    
    def complete_job(self, job_name:str):
        error_message = f"Job: {job_name}\nFailed to complete.\n"
        try:
            response = self.await_transcription_job(job_name=job_name)
            print(self.print_job_details(response))
            
            if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
                url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
                transcription_job_response = requests.request("GET", url, headers={}, data={})
                #response = self.__client.delete_transcription_job(TranscriptionJobName=job_name)
                return transcription_job_response.json()["results"]["transcripts"][0]["transcript"]
            else:
                return error_message
        except Exception as e:
            print(e)
            return error_message
            
    async def start_transcription_job(self, video_uri:str):
        job_name=self.get_transcription_job_name(video_uri=video_uri)
        media_format = self.validate_url(video_uri)
    
        try:      
            self.__client.start_transcription_job(
                TranscriptionJobName=job_name,
                IdentifyLanguage=True,
                MediaFormat=media_format,
                Media={
                    'MediaFileUri': video_uri
                }
            )
            
            print(f"job_name: {job_name}\nmedia_format: {media_format}")
        except Exception as e:
            print(f"Error when creating transcription Job\n{e}")
            return ""
        
        response = self.await_transcription_job(job_name=job_name)
        print(self.print_job_details(response))
        
        if response["TranscriptionJob"]["TranscriptionJobStatus"] == "COMPLETED":
            url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            transcription_job_response = requests.request("GET", url, headers={}, data={})
            #response = self.__client.delete_transcription_job(TranscriptionJobName=job_name)
            return transcription_job_response.json()["results"]["transcripts"][0]["transcript"]
        else:
            return ""
      
async def main():
    

    #video_uri="s3://ionica-sso-stress-content/01a6fb00-28ca-11ef-a87b-913cb7053954/3f80ee70-2367-11eb-a3ad-9f132a537bed_S20-2-PLA61-9-01-OAU-003.mp4"
    #video_uri="https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/000cb430-56ea-11ea-9845-5919a5c1a6d2/S20-1-ESP80-5-audio-006.mp3"
    #video_uri="https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/00491d40-3ad8-11ea-ac4d-1961fa465f4c/S20-SE-EI-4anos-audio012.mp3"
    #region_name="sa-east-1" #sa-east-1, us-east-2
    urls = [
    "s3://ionica-sso-stress-content/01a6fb00-28ca-11ef-a87b-913cb7053954/3f80ee70-2367-11eb-a3ad-9f132a537bed_S20-2-PLA61-9-01-OAU-003.mp4",
	"https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/000cb430-56ea-11ea-9845-5919a5c1a6d2/S20-1-ESP80-5-audio-006.mp3",
	"https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/0029ece0-4807-11ea-a8c4-17da6df2d724/S20-1-ING80-1-audio-008.mp3",
	"https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/00491d40-3ad8-11ea-ac4d-1961fa465f4c/S20-SE-EI-4anos-audio012.mp3",
	"https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/00b158a0-56ea-11ea-a430-f7b9fc7ca91d/S20-1-ESP80-5-audio-007.mp3",
	"https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/00c96130-4807-11ea-9cec-799c673ae7a4/S20-1-ING80-1-audio-009.mp3",
	"https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/00d11e60-1059-11ea-8a4e-bb3ab3bd7da7/M14-2-CIE01-7-00-WAU-32-Aids.mp3",
    "https://ftdi2cv2-prod-content.s3-sa-east-1.amazonaws.com/00d5a5d0-3ad8-11ea-9403-e3bfa8d9db23/S20-SE-EI-4anos-audio013.mp3"
    ]
    
    try:
        service = TranscribeService("sa-east-1")
        #transcription = await service.start_transcription_job(video_uri=video_uri)
        jobs = []
        [jobs.append(service.start_job(url)) for url in urls]
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(service.complete_job, job_name) for job_name in jobs]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                print(f"{result}\n")
                
        #print(transcription)
    except Exception as e:
        print(e)
    


if __name__ == "__main__":
    load_dotenv()
    run(main())