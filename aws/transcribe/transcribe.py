import os
import requests
import boto3
from dotenv import load_dotenv
from asyncio import sleep
from asyncio import run

load_dotenv()

'''
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name=os.getenv("region_name")
)
try:
    response: list = s3.list_buckets()
    bucket_name = ""
    for obj in response['Buckets']:
        if obj["Name"] == "ftd-test-bucket":
            bucket_name = obj["Name"]
    
    print(bucket_name)
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Print the object names
    for obj in response.get('Contents', []):
        print(obj['Key'])
        
except Exception as ex:
    print(ex)
'''

def create_boto3_client():
    return boto3.client(
    'transcribe',
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name=os.getenv("region_name")
    )

def create_transcription_job(job_name, client, video_file_name):
    return client.start_transcription_job(
    TranscriptionJobName=job_name,
    LanguageCode='en-US',
    MediaFormat='mp4',  # Adjust based on your audio file format
    Media={
        'MediaFileUri': f"s3://ftd-test-bucket/{video_file_name}"
    }
) 

def get_transcription_job(job_name, client):
    return client.get_transcription_job(TranscriptionJobName=job_name)
   
async def main():
    client = create_boto3_client()
    job_name='test-job-transcription'
    # video_file_name = "Dune The Emperor Has Spoken Warner Bros. Entertainment.mp4"
    # video_file_name = "Generative AI explained in 2 minutes.mp4"
    video_file_name = "What is Object-Oriented Programming (OOP).mp4"
    try:
        create_transcription_job(job_name=job_name, client=client, video_file_name=video_file_name)
    except Exception as e:
        print(f"Error when creating transcription Job")
        print(e)
    
    response = get_transcription_job(job_name=job_name, client=client)
    
    while response["TranscriptionJob"]["TranscriptionJobStatus"] != "COMPLETED":
        response = get_transcription_job(job_name=job_name, client=client)
        status = str(response["TranscriptionJob"]["TranscriptionJobStatus"])
        print(f"Current TranscriptionJobStatus: {status}")
        await sleep(2)
    
    url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    transcription_job_response = requests.request("GET", url, headers={}, data={})

    print(transcription_job_response.json()["results"]["transcripts"][0]["transcript"])
    response = client.delete_transcription_job(TranscriptionJobName=job_name)

if __name__ == "__main__":
    run(main())