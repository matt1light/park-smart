import requests
import datetime
import time
import json
import Camera
from base64 import b64encode
from collections import namedtuple

class CameraHub:
    def __init__(self):

        # The frequency(period) of photo updates in seconds
        self.delay = 60

        # The IP address of the server is 10.0.0.41, port 80
        self.serverAddress = "http://10.0.0.41:80"

        # Defining endpoints
        self.imageEndpoint = self.serverAddress + "/Images"

        # Create an empty list to store images in
        self.hubImages = list()

        # Number of Cameras
        self.numCams = 2

        # Camera Hub ID
        self.camHubID = 1

        # List of Cameras
        self.hubCameras = list()
        
        #Last post request response code
        self.responseCode = 0

        # Create list of camera objects stored in hubCameras

        #Instantiate Camera objects as same PiCamera for now
        for x in range(self.numCams):
            self.hubCameras.append(Camera.Camera(x))

        #built request
        self.builtRequest = RequestData(json.dumps({}), files = {})

    

    """
    Compiles all of the Images currently held in hubImages into a JSON blob.
    Specifically, the format of the JSON is an array of objects, each object
    representing an Image.
    """
    def buildRequest(self):
        imgFields = []

        # Create a JSON object out of each image in hubImages
        for img in self.hubImages:
            if img == None:
                pass
            else:
                hubID = int(img.cameraID.split('.')[0])
                camID = int(img.cameraID.split('.')[1])
                if (hubID != self.camHubID or camID < 0 or camID > len(self.hubCameras) - 1):
                    raise ValueError("cameraID is invalid")
                    
                fields = {"cameraID": img.cameraID, "photo": "image" + img.cameraID, "time": img.time}
                
                files = {"image" + img.cameraID: img.photo}
                
                imgFields.append(fields)
                
                self.builtRequest.files.update(files)
            
            self.builtRequest.data = json.dumps(imgFields)
                
            # Expected order of JSON elements: camera ID, photo object, timestamp

        #builtRequest = dict(imgFields = imgFiles)
        return


    """
    Send a JSON array containing Image objects to the proper endpoint of the server.
    """
    def sendRequest(self):
        r = requests.post(self.imageEndpoint, data = {self.builtRequest.data}, files = self.builtRequest.files)
        self.responseCode = r.status_code
        return


    """
    Capture an image from the Pi Camera and transform it into an image object.
    """
    def captureImage(self, camID):
        global hubImages
        global camHubID
        
        currTime = datetime.datetime.now()
        # From what I've read, the picam saves images directly to a file?
        # So, I'm thinking, the method captures an image and saves it as a JPG,
        # then loads that file and builds the Image? -- JF
        
        path = "/home/pi/Desktop/image" + str(camID) + ".jpg"
        
        #Call camera object to capture the image
        
        if (camID < 0 or camID > len(self.hubCameras) - 1):
            self.hubImages.append(None)
        else:
            self.hubCameras[camID].capture(path)
            
            #Create a photo ID for the Image
            cameraID = str(self.camHubID) + "." + str(camID)
            
            # strftime converts a datetime into a string. The parameter is a formatting
            # option. "string from time".    
            self.hubImages.append(Image(self.loadImage(path), cameraID, currTime.strftime("%c")))
        return


    """
    Load a .JPG file as bytes.
    """
    def loadImage(self, path):
        with open(path, "rb") as imageFile:
            bytes = imageFile.read()
            #base64_bytes = b64encode(bytes)
            #base64_string = base64_bytes.decode()
            return bytes
    

class Image:
    def __init__(self, photo, cameraID, time):
        self.photo = photo
        self.cameraID = cameraID
        self.time = time

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.photo == other.photo and self.cameraID == other.cameraID and self.time == other.time 
        else:
            return False

class RequestData:
    def __init__(self, data, files):
        self.data = data
        self.files = files