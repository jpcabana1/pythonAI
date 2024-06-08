import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

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
s3 = boto3.client(
    'transcribe',
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name=os.getenv("region_name")
)

# Start the transcription job
response = client.start_transcription_job(
    TranscriptionJobName='test-job-transcription',
    LanguageCode='en-US',
    MediaFormat='mp4',  # Adjust based on your audio file format
    Media={
        'MediaFileUri': "s3://ftd-test-bucket/Generative AI explained in 2 minutes.mp4"
    }
) 

response = client.get_transcription_job(TranscriptionJobName='test_job-transcription')

url = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]

transcription_job_response = requests.request("GET", url, headers={}, data={})

print(transcription_job_response.json()["status"])
print(transcription_job_response.json()["results"]["transcripts"][0]["transcript"])

response = client.delete_transcription_job(TranscriptionJobName='test_job-transcription')

'''