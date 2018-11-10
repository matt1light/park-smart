import requests
import datetime
import json

# The IP address of the server is 10.0.0.41, port 80
serverAddress = "http://10.0.0.41:80"

# Defining endpoints
imageEndpoint = serverAddress + "/Images"

# Create an empty list to store images in
hubImages = list()

"""
Compiles all of the Images currently held in hubImages into a JSON blob.
Specifically, the format of the JSON is an array of objects, each object
representing an Image.
"""
def buildRequest(hubImages):
    imgData = list()

    # Create a JSON object out of each image in hubImages
    for img in hubImages:
        # Expected order of JSON elements: camera ID, photo object, timestamp
        obj = {"camID": img.camID, "photo": img.photo, "time": img.time}
        imgData.append(obj)

    return json.dumps(imgData)


"""
Send a JSON array containing Image objects to the proper endpoint of the server.
"""
def sendRequest(builtRequest):
    r = requests.post(imageEndpoint, builtRequest)
    print("Status code: " + r.status_code)
    if r.status_code == requests.codes.ok:
        print("Status code OK")


"""
Capture an image from the Pi Camera and transform it into an image object.
"""
def captureImage(camID:int):
    # From what I've read, the picam saves images directly to a file? -- JF
    path = "somepath"
    return Image(loadImage(path), camID, datetime.datetime.now().strftime("%c"))


"""
Load a .JPG file as bytes.
"""
def loadImage(path):
    img = open(path, 'r')
    return img.read()


class Image:
    def __init__(self, photo, camID, time):
        self.photo = photo
        self.camID = camID
        self.time = time


testImage = Image("THISPHOTO", 3, datetime.datetime.now().strftime("%c"))
testImage2 = Image("THATPHOTO", 3, datetime.datetime.now().strftime("%c"))
images = [testImage, testImage2]
builtRequest = buildRequest(images)
print(builtRequest)
# sendRequest(builtRequest)
