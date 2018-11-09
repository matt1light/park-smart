import requests
import datetime
import json

# The IP address of the server is 10.0.0.41, port 80
ipAddress = "http://10.0.0.41:80"


def buildRequest(hubImages):
    imgData = list()
    for img in hubImages:
        imgData.append([img.photo, img.camID, img.time])
    builtRequest = json.dumps(imgData)
    print(builtRequest)

def sendRequest(builtRequest):
    return

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
buildRequest(images)