import requests
import datetime
import time
import json
from Camera import CameraStub
from base64 import b64encode

class CameraHub: 
    """
    Each camera hub is an instance of this class which contains all pertinent attributes 
    and operations of the camera hub
    """
    
    def __init__(self, numCams, hubID):

        # The IP address of the server is 10.0.0.41, port 80
        self.serverAddress = "http://172.17.130.14:7000"

        # Defining endpoints
        self.imageEndpoint = self.serverAddress + "/image/"

        # Create an empty list to store images in
        self.hubImages = list()

        # Number of Cameras
        self.numCams = numCams

        # Camera Hub ID
        self.camHubID = hubID

        # List of Cameras
        self.hubCameras = list()
        
        # Stores POST request response for the last set of requests
        self.responseCodes = list()

        # Create list of camera objects stored in hubCameras

        # Instantiate Camera objects as same PiCamera for now
        for x in range(self.numCams):
            self.hubCameras.append(CameraStub(x))

        # Built request is a list of RequestData objects
        self.builtRequest = list()

    

    """
    Compiles all of the Images currently held in hubImages into an array of RequestData objects, stored in builtRequest
    """
    def buildRequest(self):
        imgFields = []

        # Go through all hub images. Check if Image is a none object. If it is ignore it
        for img in self.hubImages:
            if img == None:
                pass
            else: # If it not a none object then read the image object data into builtRequest
                hubID = int(img.cameraID.split('.')[0])
                camID = int(img.cameraID.split('.')[1])
                
                # Check if the cameraID is invalid, if it is raise error
                if (hubID != self.camHubID or camID < 0 or camID > len(self.hubCameras) - 1):
                    raise ValueError("cameraID is invalid")
                    
                # Parse the image data into the data attribute of RequestData
                data = {"cameraID": img.cameraID, "time_taken": img.time}
                
                # Read the image file bytes into the files attribute of RequestData
                files = {"image" + img.cameraID: img.photo}
                
                # Add the parsed data into the builtRequest list
                self.builtRequest.append(RequestData(data, files))
            
        return


    """
    Send http POST request for each RequestData object in the builtRequest
    """
    def sendRequest(self):
        for postRequest in self.builtRequest:
            r = requests.post(self.imageEndpoint, data = postRequest.data, files = postRequest.files)
            self.responseCodes.append(r.status_code)
        
        return


    """
    Capture an image from the Pi Camera and transform it into an image object.
    """
    def captureImage(self, camID):
        
        # Get the current time 
        currTime = datetime.datetime.now()
        
        path = "/home/pi/Desktop/image" + str(camID) + ".jpg"
        #path = "C:/Users/mrolu/OneDrive/Desktop/randomImage.jpg"
        
        # Call camera object to capture the image
        if (camID < 0 or camID > len(self.hubCameras) - 1): #If camID passed is invalid
            self.hubImages.append(None)
        else:
            self.hubCameras[camID].capture(path)
            
            # Create a photo ID for the Image: first digit is the camHubID followed by a period and then the camera's index within the hub
            cameraID = str(self.camHubID) + "." + str(camID)
            
            # Create a new Image object for the photo and store it in hubImages
            self.hubImages.append(Image(open(path, "rb"), cameraID, currTime))
        return
 

class Image:
    """
    Image class represents a photo taken. Attributes store the bytes of 
    
    Attributes:
        photo: Stores bytes of the photo file
        cameraID: String of the camera ID. 
        time_taken: Datetime object of the time the photo was taken
    """
    
    def __init__(self, photo, cameraID, time):
        self.photo = photo
        self.cameraID = cameraID
        self.time_taken = time

    # This method was overwritten to ensure that two photo objects with the same attributes are considered equal
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.photo == other.photo and self.cameraID == other.cameraID and self.time == other.time 
        else:
            return False

class RequestData:
    """
    Request data contains the 2 required pieces of data to post a HTTP request for a single image
    
    Attributes:
        data: Python dict containing time_taken and cameraID
        files: dict containing bytes for the image
    """
    def __init__(self, data, files):
        self.data = data
        self.files = files