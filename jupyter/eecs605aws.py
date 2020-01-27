import boto3
import time

def run(s3BucketName, inputImageFileName, resultsDataFileName, progressRefreshRate):

    client = boto3.client('s3')
    
    # Upload digit.png to S3.
    client.upload_file(inputImageFileName, s3BucketName, inputImageFileName)
    
    # Checking to see if the results.txt has been produced in S3 from Lambda.
    while True:
        try:
            client.download_file(s3BucketName, resultsDataFileName, resultsDataFileName)
            print("Downloading")
            break
        except:
            print("Waiting for result")
            time.sleep(progressRefreshRate)
            
    # Removing input digit.png and output results.txt from S3.
    client.delete_object(Bucket=s3BucketName,Key=inputImageFileName)
    client.delete_object(Bucket=s3BucketName,Key=resultsDataFileName)
