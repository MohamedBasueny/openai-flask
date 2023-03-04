import openai
import requests
import boto3
import time
import zipfile
from flask import jsonify
import os
# Set up the OpenAI API credentials
openai.api_key = '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'
Access_key = 'AKIAZ2ATZLIJIMU3LGAH'
Secret_access_key = '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'
Bucket_name = 'lablab-r589abgqi3sghbtjf6yb4nkig1azruse1a-s3alias'
# A function to open a file
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Generating a function of generating HTML
def generate_HTML(command):
    format_html = "<!-- <<COMMAND>>; it should link the .css file namely 'styles.css'-->\n<!DOCTYPE html>\n"
    command = command
    prompt = format_html.replace("<<COMMAND>>",command)
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=3818,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    with open("index.html","w") as file:
        file.write(response.choices[0].text)
        file.close()

# Generating a function of generating CSS
def generate_CSS():
    format_css = "<<HTML>>\n/* <<COMMAND>> */\n"
    command = "Make a  CSS style file  from HTML above"
    prompt = format_css.replace("<<HTML>>",open_file("index.html")).replace("<<COMMAND>>",command)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=.3,
        max_tokens=3000)
     
    with open("styles.css","w") as file:
        file.write(response.choices[0].text)
        file.close()

# Define the endpoint for generating HTML and CSS based on user prompt
def generate_HTML_and_CSS(command):
    # Get the command prompt from the request
    # Generate HTML file
    generate_HTML(command)
    # Generate CSS file
    generate_CSS()

    # Create a ZipFile object
    file_name = '{}_HTML_CSS.zip'.format(time.time())
    zip_file = zipfile.ZipFile(file_name, 'w')
    # Add files to the zip file
    zip_file.write("index.html")
    zip_file.write("styles.css")
    # Close the ZipFile object
    zip_file.close()

    # Send to S3 Bucket AWS
    s3 = boto3.client('s3', aws_access_key_id=Access_key, 
    aws_secret_access_key=Secret_access_key)
    bucket_name = Bucket_name
    # Send Zip file
    # Upload the zip file to the S3 bucket
    file_path = f"/home/runner/openai-flask/{file_name}"
    s3.upload_file(file_path, bucket_name, file_name)

    # Retrieve the URL

    # url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    url = s3.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': bucket_name,
        'Key': file_name,
    },
    ExpiresIn=3600,  # URL expires after 1 hour
)

    # Notify
    print("HTML and CSS files have been sent to AWS bucket")
    return jsonify({'generated_HTML_and_CSS_URL': url})
