# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from imageai.Detection import ObjectDetection
import os
import datetime

from mainModels.models import Spot, SectorSpot, ParkingLot, Sector, ImageCoordinates, Image, ParkingEvent

# Non persistant static class
# processor is not an object
class ImageProcessor(models.Model):
    MIN_OVERLAP = 0.4
    MIN_PROBABILITY = 23
    class Meta:
        managed = False

    # Creates spots based on the identified cars in an image and adds them to a specified sector
    # Input: name of image to be processed, sector for spots to be added to
    @staticmethod
    def addSpotsToSector(image_name, sector):
        # get coordinates for new spots
        new_coords = ImageProcessor.getCoordsFromImageResnet(image_name)
        # for each spot create a SectorSpot and add the coordinates
        for new_spot_coords in new_coords:
            # create a spot with sectorspot id
            spot = Spot.objects.create(active=True, full=False)
            # create an ImageCoord from new_spot_coords with sectorspot id
            image_coordinates = ImageCoordinates.objects.create(left=new_spot_coords[0],
                                                                top=new_spot_coords[1],
                                                                right=new_spot_coords[2],
                                                                bottom=new_spot_coords[3])
            # create a sectorspot with the sector id
            SectorSpot.objects.create(sector=sector, spot=spot, image_coordinates=image_coordinates)

    # Updates a sector's spot statuses based on it's most recent image
    @staticmethod
    def updateSector(sector):
        # get the latest image for this sector
        images = Image.objects.filter(sector=sector).order_by('-id')
        latest_image = images[0]
        image_path = latest_image.photo.url[1:]
        # update the sector with the latest image
        ImageProcessor.updateSectorByImage(image_path, sector)

    # Updates a sector's spot statuses with a picture input
    @staticmethod
    def updateSectorByImage(image_name, sector):
        # use object recognition to find coordinates
        detected_coords = ImageProcessor.getCoordsFromImageResnet(image_name)
        # for each coordinate in the detected coordinates
        for sector_spot in sector.sector_spots.all():
            # compare to the possible coordinates
            spot_full = False
            spot = sector_spot.spot
            for coord in detected_coords:
                # if the coordinates intersect by more than the MIN_OVERLAP
                if ImageProcessor.calculateOverlapPercentage(sector_spot.image_coordinates, coord) >= ImageProcessor.MIN_OVERLAP and spot.full==False:
                    # update the spot to full and save it
                    spot.full = True
                    spot.last_park = datetime.datetime.now()
                    spot.save(update_fields=["last_park", "full"])
                    spot_full = True
            # if the spot is empty in the picture but not in the database update the database entry
            if not spot_full and spot.full:
                ParkingEvent.objects.create(spot=spot,
                                            parking_start=spot.last_park,
                                            parking_end=datetime.datetime.now())

                spot.full = False
                spot.last_park = None
                spot.save(update_fields=["last_park", "full"])

    # Gets the coordinates of cars in an image, using the resnet ANN model
    @staticmethod
    def getCoordsFromImageResnet(image_name):
        execution_path = os.getcwd()

        #FIXME adjust image path
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
        # detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()

        custom_objects = detector.CustomObjects(car=True, motorcycle=True)
        detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path ,image_name), output_image_path=os.path.join(execution_path , image_name.split(".")[0] + "_processed.jpg"), minimum_percentage_probability=ImageProcessor.MIN_PROBABILITY)

        coords = []

        for eachObject in detections:
            coords.append(eachObject['box_points'].tolist())

        return coords

    # Gets the coordinates of cars in an image, using google's vision API
    @staticmethod
    def getCoordsFromImageVisionAPI(image_name):
        ImageProcessor.localize_objects(image_name)

    # Takes the input of the coordinates of two rectangles and determinest the percentage that they overlap
    @staticmethod
    def calculateOverlapPercentage(spot_coords, detected_coords):
        left1 = spot_coords.left
        left2 = detected_coords[0]


        top1 = spot_coords.top
        top2 = detected_coords[1]

        right1 = spot_coords.right
        right2 = detected_coords[2]

        bottom1 = spot_coords.bottom
        bottom2 = detected_coords[3]

        intersection = max(0, min(right1, right2) - max(left1, left2)) * max(0, min(bottom1, bottom2) - max(top1, top2))

        spot_area = (right1 - left1)*(bottom1 - top1)
        detected_area = (right2 - left2)*(bottom2 - top2)

        union = spot_area + detected_area - intersection
        percentage = intersection/union
        return percentage

    # vision api method to get coordinates of cars in an image
    @staticmethod
    def localize_objects(path):
        """Localize objects in the local image.

        Args:
        path: The path to the local file.
        """
        path += ".jpg"
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        coords = []

        with open(path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)

        objects = client.object_localization(
            image=image, ).localized_object_annotations

        for object_ in objects:
            if object_.name == "Car" or object_.name == "Motorcycle":
                vertices = object_.bounding_poly.normalized_vertices
                left = vertices[0].x
                right = vertices[1].x
                top = vertices[0].y
                bottom = vertices[2].y

                coords.append([left, right, top, bottom])

        return coords
