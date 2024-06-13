import os
import json
import datetime
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from dotenv import load_dotenv

load_dotenv()

def get_dump_file_name() -> str:
    # Get the current date and time
    current_datetime = datetime.datetime.now()
    
    # Format the date and time as a string in the desired format
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M%S")
    
    return f"dumps/unstructured-dump-{formatted_datetime}.json"

# Update here with your api key and server url
client = UnstructuredClient(
    api_key_auth=os.getenv("UNSTRUCTURED_API_KEY_AUTH"),
    server_url=os.getenv("UNSTRUCTURED_SERVER_URL"),
)

# Update here with your filename
filename = "data/9140604000554-ftd-se-em-cnt-biologia-vol13-18-miolo-prof-001-33.pdf"

with open(filename, "rb") as f:
    files=shared.Files(
        content=f.read(),
        file_name=filename,
    )

# You can choose fast, hi_res or ocr_only for strategy, learn more in the docs at step 4
req = shared.PartitionParameters(files=files, strategy="auto")

try:
    resp = client.general.partition(req)
    json_string = json.dumps(resp.elements, indent=2)
    print(json_string)
    
    with open(get_dump_file_name(), "w", encoding="utf-8") as file:
        file.write(json_string)
except SDKError as e:
    print(e)
