# GUI Packages.
import matplotlib.pyplot as plt
import ipywidgets as widgets
import time

# AWS Packages.
import boto3

# AWS Variables.
s3BucketName = "handwriting-recog-aws-bucket"
inputImageFileName = "digit.png"
resultsDataFileName = "results.txt"

def parseAndShowResults(resultsDataFileName):

    with open(resultsDataFileName, "r") as results:
        # Extracting prediction results.
        vals = {}
        for result in results:
            # class=1 ; probability=0.573457
            values = result.split(";")
            classValue = values[0].strip(" ").replace("class=", "")
            predictionValue= values[1].strip(" ").replace("probability=", "").replace("\n", "")
            vals[predictionValue] = classValue
        
        # Finding the prediction value with the highest prediction value.
        predictedValue = vals[str(max(vals.keys()))]
        predictionProbabilityValue = str(max(vals.keys()))
        
        # Displaying values and the input image.
        img = plt.imread(inputImageFileName)
        plt.imshow(img)
        title = plt.title("Predicted: \"%s\", Probability: %s" % (predictedValue, predictionProbabilityValue))

## AWS Image Upload callback function and button ##

# Upload digit.png to S3 to produce the results.txt using lambda.
def awsImageUpload(buttonObject):

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
            time.sleep(awsProgressRefreshRateSlider.value)
            
    # Removing input digit.png and output results.txt from S3.
    client.delete_object(Bucket=s3BucketName,Key=inputImageFileName)
    client.delete_object(Bucket=s3BucketName,Key=resultsDataFileName)

    # Display Results
    parseAndShowResults(resultsDataFileName)

## Image upload callback function and button ##
def selectimage2upload(imageData):
    # Due to the file structure, image file name needs to be
    # extracted to access the bytes data of the image.
    imageFileName = list(imageData["new"].keys())[0]
    
    # Image bytes data.
    imageBytesData = imageData["new"][imageFileName]["content"]
    
    # Writing image file to current directory with "inputImageFileName".
    with open(inputImageFileName, "wb") as imageFile:
        imageFile.write(imageBytesData)
    
    # Displaying uploaded image in GUI.
    display(widgets.Image(value=imageBytesData))
    
    # Showing AWS GUI Components after image is uploaded.
    display(awsProgressRefreshRateSlider)
    display(awsUploadButton)


def createDashBoard():
    # Allows the buttons to be accessed globally: Necessary
    # since some callback functions are dependent on these
    # widgets.
    global awsUploadButton
    global awsProgressRefreshRateSlider
    
    # AWS Image Upload Button.
    awsUploadButton = widgets.Button(description="Upload to AWS")
    awsUploadButton.on_click(awsImageUpload)
    
    # AWS Progress Refresh Rate Selector.
    awsProgressRefreshRateSlider = widgets.FloatSlider(min=0, max=1.0)
    
    # Display GUI.
    # Note: If new image is being uploaded, this block needs to be
    # run again.
    selectimage2uploadButton = widgets.FileUpload(multiple=False)
    # Specifying which function to run whenever an image is uploaded.
    selectimage2uploadButton.observe(selectimage2upload, names='value')
    display(selectimage2uploadButton)
