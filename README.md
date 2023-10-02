## Introduction

**s3-uploader is an extension for [AUTOMATIC1111's Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).**

It allows to store pictures in Amazon S3 and generate pre-signed URLs for those images and QR codes for users to download them directly.

This was based off a DB Example provided [here](https://github.com/takoyaro/db-storage1111)

## Features

- **Upload images in Amazon S3**
- **Generate Amazon S3 Pre-signed URLs**
- **Generate QR Codes for the URLs**

## Installation


1. Visit the **Extensions** tab of Automatic's WebUI.
2. Visit the **Install from URL** subtab.
3. Paste this repo's URL into the first field: `https://github.com/tomellis/s3-uploader
4. Click **Install**.
5. Add IAM role to your ec2 instance to allow it to use S3
6. Install additional python modules: boto3, qrcode

## Usage
Set environment variables if needed before starting the app:

```
export S3_BUCKET=bucket_name
```
Then, simply check the `Save to S3` checkbox and generate!

