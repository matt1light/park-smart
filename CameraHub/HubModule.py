import CameraHub

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