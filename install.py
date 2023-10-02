import launch

if not launch.is_installed("boto3"):
    launch.run_pip("install boto", "requirements for s3-uploader")

if not launch.is_installed("qrcode"):
    launch.run_pip("install qrcode", "requirements for s3-uploader")
