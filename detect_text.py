import boto3
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve AWS credentials from .env file
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")

# Set up AWS Textract client
client = boto3.client(
    'textract', 
    aws_access_key_id=aws_access_key, 
    aws_secret_access_key=aws_secret_key, 
    region_name=aws_region
)

def detect_text(image_path):
    
    client = boto3.client('textract')
    with open(image_path,'rb') as image:
        response = client.detect_document_text(Document={'Bytes': image.read()}
    )

    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text += " " + item["Text"] 

    return text