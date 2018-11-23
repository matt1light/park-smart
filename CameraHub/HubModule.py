from CameraHub import CameraHub

hub1 = CameraHub() 
    #Capture an Image for all cameras in the hub
for camera in hub1.hubCameras:
    x = hub1.hubCameras.index(camera)
    hub1.captureImage(x)
     
    #Build a request after all images have been captured 
hub1.buildRequest()
    
    #Send request
print(hub1.builtRequest.data)

    #Delay
#time.sleep(delay)