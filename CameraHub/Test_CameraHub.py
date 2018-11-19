import unittest
import datetime
import json
from CameraHub import CameraHub
from CameraHub import Image
from MockServerTest import MockServerRequestHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

"""
Unit Test for CameraHub class.
Tests public methods
"""
class CameraHubTestCase(unittest.TestCase):
    
    def setUp(self):   
        self.date = datetime.datetime.now().date()
        self.c = CameraHub()
        
    def tearDown(self):
        del self.c
        del self.date

    """
    Test 1a: tests that captureImage() correctly creates a valid Image object when passed valid camID
    """
    def testCaptureImageValidID(self):
        #Call method to capture photo
        self.c.captureImage(0)
        
        #Create expected Image object manually with photo captured by method above
        image1 = Image(self.c.loadImage("/home/pi/Desktop/image0.jpg"), "1.0", self.date.strftime("%c"))
        
        #Assert both objects are equal.
        #__eq__ method for image class has been overwritten to compare attributes of instances for equality
        self.assertEqual(self.c.hubImages[0], image1)
       
    """
    Test 1b: Test that method appends None object to hubImages array when called with invalid camID
    """
    def testCaptureImageInvalidID(self):
        #call method with invalid camID
        self.c.captureImage(-1)
        
        #Assert returned Image is a None object
        self.assertEqual(self.c.hubImages[0], None)
    
    """
    Test 2a: Test that method creates a valid JSON object store in builtRequest of all Image objects in
    hubImages when called
    """
    def testBuildRequestValid(self):
        #Call captureImage to populate hubImages
        self.c.captureImage(0)
        self.c.captureImage(1)
        
        #Call method to create JSON
        self.c.buildRequest()
        
        #Manually create JSON object of all images in hubImages
        imgData = []
        for img in self.c.hubImages:
            obj = {"photoID": img.photoID, "photo": img.photo, "time": img.time}
            imgData.append(obj)
        request = json.dumps(imgData)
        
        self.assertEqual(self.c.builtRequest, request)
      
    """
    Test 2b: Tests that the method removes None objects added to hubImages before
    creating JSON object
    """
    def testBuildRequestNoneObjects(self):
        #Call captureImage to populate hubImages includind and invalid call to add None object
        self.c.captureImage(0)
        self.c.captureImage(-1)
        self.c.captureImage(1)
        
        #Call method to build JSON object
        self.c.buildRequest()
        
        #Manually build JSON object without JSON object
        imgData = []
        for img in self.c.hubImages:
            if img == None:
                pass
            else:
                obj = {"photoID": img.photoID, "photo": img.photo, "time": img.time}
                imgData.append(obj)
        request = json.dumps(imgData)
        
        self.assertEqual(self.c.builtRequest, request)
        
    """
    Test 2c: Tests that be method raises a value error when hubImages contains an Image object
    has an invalid photoID
    """
    def testBuildRequestInvalidImageObject(self):
        #Capture images to populate hubImages
        self.c.captureImage(0)
        self.c.captureImage(1)
        self.c.captureImage(2)
        
        #Overwrite photoID attribute with invalid value
        self.c.hubImages[1].photoID = "1.a"
        
        #Check that Value Error is raised
        with self.assertRaises(ValueError):
            self.c.buildRequest()
        
    """
    Test 3a: Tests that method returns valid response code with POST request is sent
    """
    def testSendRequest(self):
        #Create a mock server on a separate thread
        mock_server = HTTPServer(('localhost', 8080), MockServerRequestHandler)
        mock_server_thread = Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()
        
        #Input valid request url
        self.c.imageEndpoint = "http://localhost:8080/Images"
        
        #Call method and check that response is ok
        self.c.sendRequest()
        self.assertEqual(self.c.responseCode, 200)
        
        
    def testSendRequestInvalidImageEndPoint(self):
        #Create a mock server on a separate thread
        mock_server = HTTPServer(('localhost', 8081), MockServerRequestHandler)
        mock_server_thread = Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()
        
        #Input invalid request url
        self.c.imageEndpoint = "http://localhost:8081/invalid"
        
        #call method and check response
        self.c.sendRequest()
        self.assertEqual(self.c.responseCode, 404)
        
      
#Run tests
suite = unittest.TestLoader().loadTestsFromTestCase(CameraHubTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
        
        
