import base64
from io import BytesIO
import os
import re
import modules.scripts as scripts
import gradio as gr
import shlex

import boto3
import qrcode
import uuid
from datetime import datetime

s3 = boto3.client('s3')

s3_bucket = os.environ.get('S3_BUCKET')

class Scripts(scripts.Script):
    def title(self):
        return "S3 Uploader"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        checkbox_save_to_s3 = gr.inputs.Checkbox(label="S3 Uploader: Save to S3", default=False)
        return [checkbox_save_to_s3]

    def postprocess(self, p, processed, checkbox_save_to_s3):
        for i in range(len(processed.images)):
            # Extract image information
            prompt = processed.prompt
            image = processed.images[i]
            buffer = BytesIO()
            image.save(buffer, "png")
            image_bytes = buffer.getvalue()

            # Generate UUID for image
            uuid_str = str(uuid.uuid4())
            # Get current date and time
            now = datetime.now()
            date_time = now.strftime("%Y%m%d-%H%M%S")
            # Create file name with suffix
            file_name = f"{uuid_str}-{date_time}.png" 

            # Save buffer out to png file
            with open(file_name, "wb") as outfile:
                outfile.write(buffer.getbuffer())
            
            try:
              # Upload file to S3
              s3.upload_file(file_name, s3_bucket, file_name)

              # Generate presigned URL to access uploaded file
              url = s3.generate_presigned_url(
                      ClientMethod='get_object',
                      Params={
                          'Bucket': s3_bucket,
                          'Key': file_name
                      })

              # Generate QR code from presigned URL & upload to S3
              img = qrcode.make(url)
              qrcode_filename = 'qrcode-' + file_name
              img.save(qrcode_filename)
              s3.upload_file(qrcode_filename, s3_bucket, qrcode_filename)
              qrcode_url = s3.generate_presigned_url(
                      ClientMethod='get_object',
                      Params={
                          'Bucket': s3_bucket,
                          'Key': qrcode_filename
                      })

            except Exception as e:
              print(f"Error uploading to S3: {e}")
              traceback.print_exc()
              return False

            # Print out the details
            print(f"""
               File Name: {file_name}
               Prompt: {prompt}
               URL: {url}
               QRCode Image: {qrcode_url}
               """)

        return True
