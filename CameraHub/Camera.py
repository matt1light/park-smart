from picamera import PiCamera
from time import sleep

class Camera:
    """
    Camera captures a photo using the PiCamera module
    
    Attributes:
        camID: Index of the camera within the list of cameras for the hub
    """
    
    #Camera is initialized with and ID 
    def __init__(self, camID):
        self.camID = camID
     
    #Capture image and store it in path    
    def capture(self, path):
        self = PiCamera() 
        self.resolution(1024, 768)  #Set resolution      
        self.start_preview()        #Open preview and allow time to adjust light conditions
        sleep(3)                    #Camera warm up time
        self.capture(path)          #Capture image and store in path
        self.stop_preview()         
        self.close()
        return


class CameraStub:
    """
    Stub the Camera for testing and debugging
    """
    def __init__(self, camID):
        self.camID = camID
    
    def capture(self, path):
        return 