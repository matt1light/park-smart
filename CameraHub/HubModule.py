from CameraHub import CameraHub
import time

#delay between Image captures
delay = 60

while (1):
    # Create a Camera Hub object and initialize it
    hub1 = CameraHub() 
    
    # Capture an Image for all cameras in the hub
    for camera in hub1.hubCameras:
        x = hub1.hubCameras.index(camera)
        hub1.captureImage(x)
         
    #Build a request after all images have been captured 
    hub1.buildRequest()
        
    #Send request
    hub1.sendRequest()

    #print(hub1.responseCode)

    #Delay
    time.sleep(delay)