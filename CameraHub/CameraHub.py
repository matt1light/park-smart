import requests
import datetime
import time
import json
import Camera
from base64 import b64encode

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
        self.builtRequest = json.dumps({})

    

    """
    Compiles all of the Images currently held in hubImages into a JSON blob.
    Specifically, the format of the JSON is an array of objects, each object
    representing an Image.
    """
    def buildRequest(self):
        imgData = []

        # Create a JSON object out of each image in hubImages
        for img in self.hubImages:
            if img == None:
                pass
            else:
                hubID = int(img.photoID.split('.')[0])
                camID = int(img.photoID.split('.')[1])
                if (hubID != self.camHubID or camID < 0 or camID > len(self.hubCameras) - 1):
                    raise ValueError("photoID is invalid")
                    
                obj = {"photoID": img.photoID, "photo": img.photo, "time": img.time}
                imgData.append(obj)
            # Expected order of JSON elements: camera ID, photo object, timestamp

        self.builtRequest = json.dumps(imgData)
        return


    """
    Send a JSON array containing Image objects to the proper endpoint of the server.
    """
    def sendRequest(self):
        r = requests.post(self.imageEndpoint, self.builtRequest)
        self.responseCode = r.status_code
        return


    """
    Capture an image from the Pi Camera and transform it into an image object.
    """
    def captureImage(self, camID):
        global hubImages
        global camHubID
        
        currTime = datetime.datetime.now().date()
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
            photoID = str(self.camHubID) + "." + str(camID)
            
            # strftime converts a datetime into a string. The parameter is a formatting
            # option. "string from time".    
            self.hubImages.append(Image(self.loadImage(path), photoID, currTime.strftime("%c")))
        return


    """
    Load a .JPG file as bytes.
    """
    def loadImage(self, path):
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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.photo == other.photo and self.photoID == other.photoID and self.time == other.time 
        else:
            return False
