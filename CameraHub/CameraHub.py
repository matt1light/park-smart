import requests
import datetime
import json
import Camera
from base64 import b64encode

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
hubCameras = []

#built request
builtRequest = json.dumps({})

# Create list of camera objects store in hubCameras
for x in range(numCams):
    camID = str(camHubID) + str(x)
    int(camID)
    hubCameras.append(Camera.Camera(camID))
    

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
        obj = {"camID": img.camID, "photo": img.photo, "time": img.time}
        imgData.append(obj)

    builtRequest = json.dumps(imgData)
    return


"""
Send a JSON array containing Image objects to the proper endpoint of the server.
"""
def sendRequest(builtRequest):
    r = requests.post(imageEndpoint, builtRequest)
    print("Status code: " + r.status_code)
    if r.status_code == "200":
        print("Status code OK")


"""
Capture an image from the Pi Camera and transform it into an image object.
"""
def captureImage(camID):
    global hubImages
    currTime = datetime.datetime.now()
    # From what I've read, the picam saves images directly to a file?
    # So, I'm thinking, the method captures an image and saves it as a JPG,
    # then loads that file and builds the Image? -- JF
    path = "/home/pi/Desktop/image1.jpg"
    
    #Create a camera object to capture the image
    cam = Camera.Camera(camID)
    cam.capture(path)
    
    # strftime converts a datetime into a string. The parameter is a formatting
    # option. "string from time".    
    hubImages.append(Image(loadImage(path), camID, currTime.strftime("%c")))
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
        
    
    #img = open(path, 'r')
    #return img.read()


class Image:
    def __init__(self, photo, camID, time):
        self.photo = photo
        self.camID = camID
        self.time = time


captureImage(10)
buildRequest(hubImages)
#testImage = Image("THISPHOTO", 3, datetime.datetime.now().strftime("%c"))
#testImage2 = Image("THATPHOTO", 3, datetime.datetime.now().strftime("%c"))
#images = [testImage, testImage2]
#builtRequest = buildRequest(images)
print(builtRequest)
# sendRequest(builtRequest)

