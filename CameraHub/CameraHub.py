import requests
import datetime
import time
import json
import Camera
from base64 import b64encode

# The frequency(period) of photo updates in seconds
delay = 60

# The IP address of the server is 10.0.0.41, port 80
serverAddress = "http://10.0.0.41:80"

# Defining endpoints
imageEndpoint = serverAddress + "/Images"

# Create an empty list to store images in
hubImages = list()

# Number of Cameras
numCams = 2

# Camera Hub ID
camHubID = 1

# List of Cameras
hubCameras = list()

# Create list of camera objects stored in hubCameras

#Instantiate Camera objects as same PiCamera for now
for x in range(numCams):
    hubCameras.append(Camera.Camera(x))

#built request
builtRequest = json.dumps({})

    

"""
Compiles all of the Images currently held in hubImages into a JSON blob.
Specifically, the format of the JSON is an array of objects, each object
representing an Image.
"""
def buildRequest(hubImages):
    global builtRequest
    imgData = []

    # Create a JSON object out of each image in hubImages
    for img in hubImages:
        # Expected order of JSON elements: camera ID, photo object, timestamp
        obj = {"photoID": img.photoID, "photo": img.photo, "time": img.time}
        imgData.append(obj)

    builtRequest = json.dumps(imgData)
    return


"""
Send a JSON array containing Image objects to the proper endpoint of the server.
"""
def sendRequest(builtRequest):
    r = requests.post(imageEndpoint, builtRequest)
    print("Status code: " + r.status_code)
    return


"""
Capture an image from the Pi Camera and transform it into an image object.
"""
def captureImage(camID):
    global hubImages
    global camHubID
    
    currTime = datetime.datetime.now()
    # From what I've read, the picam saves images directly to a file?
    # So, I'm thinking, the method captures an image and saves it as a JPG,
    # then loads that file and builds the Image? -- JF
    path = "/home/pi/Desktop/image" + str(camID) + ".jpg"
    
    #Call camera object to capture the image
    hubCameras[camID].capture(path)
    
    #Create a photo ID for the Image
    photoID = str(camHubID) + "." + str(camID)
    
    # strftime converts a datetime into a string. The parameter is a formatting
    # option. "string from time".    
    hubImages.append(Image(loadImage(path), photoID, currTime.strftime("%c")))
    return


"""
Load a .JPG file as bytes.
"""
def loadImage(path):
    with open(path, "rb") as imageFile:
        bytes = imageFile.read()
        base64_bytes = b64encode(bytes)
        base64_string = base64_bytes.decode()
        return base64_string


class Image:
    def __init__(self, photo, photoID, time):
        self.photo = photo
        self.photoID = photoID
        self.time = time


while 1:
    
    #Capture an Image for all cameras in the hub
    for camera in hubCameras:
        x = hubCameras.index(camera)
        captureImage(x)
     
    #Build a request after all images have been captured 
    buildRequest(hubImages)
    
    #Send request
    sendRequest(builtRequest)

    #Delay
    time.sleep(delay)
