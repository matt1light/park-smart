import requests
import datetime
import json

# The IP address of the server is 10.0.0.41, port 80
serverAddress = "http://10.0.0.41:80"

# Defining endpoints
imageEndpoint = serverAddress + "/Images"


def buildRequest(hubImages):
    imgData = list()
    # Create a JSON object out of each image in hubImages
    for img in hubImages:
        # Expected order of JSON elements: camera ID, photo object, timestamp
        obj = {"camID":img.camID, "photo":img.photo, "time":img.time}
        imgData.append(obj)
    # builtRequest = json.dumps(imgData)
    return json.dumps(imgData)


def sendRequest(builtRequest):
    r = requests.post(imageEndpoint, builtRequest)
    print("Status code: " + r.status_code)
    if r.status_code == requests.codes.ok:
        print("Status code OK")


def captureImage(camID:int):
    return


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
