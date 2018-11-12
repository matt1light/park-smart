# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from imageai.Detection import ObjectDetection
import os

from mainModels.models import Spot, SectorSpot, ParkingLot, Sector, ImageCoordinates, Image

# Non persistant static class
# processor is not an object
class ImageProcessor(models.Model):
    MIN_OVERLAP = 0.7
    class Meta:
        managed = False

    @staticmethod
    def addSpotsToSector(image_name, sector):
        # get coordinates for new spots
        new_coords = ImageProcessor.getCoordsFromImage(image_name)
        # for each spot create a SectorSpot and add the coordinates
        for new_spot_coords in new_coords:
            # create a spot with sectorspot id
            s = Spot.objects.create(active=True, full=False)
            # create an ImageCoord from new_spot_coords with sectorspot id
            i = ImageCoordinates.objects.create(x=new_spot_coords[0],y=new_spot_coords[1],w=new_spot_coords[2],h=new_spot_coords[3])
            # create a sectorspot with the sector id
            SectorSpot.objects.create(sector=sector, spot=s, image_coordinates=i)

    @staticmethod
    def updateSector(sector):
        # get the latest image for this sector
        latest_image = Image.objects.filter(sector=sector.pk).latest('image')
        ImageProcessor.updateSectorByImage(latest_image.photo, sector)

    @staticmethod
    def updateSectorByImage(image_name, sector):
        # use object recognition to find coordinates
        detected_coords = ImageProcessor.getCoordsFromImage(image_name)
        # for each coordinate in the detected coordinates
        for coord in detected_coords:
            # compare to the possible coordinates
            for sector_spot in sector.sector_spots:
                # if the coordinates intersect by more than the MIN_OVERLAP
                if ImageProcessor.calculateOverlapPercentage(sector_spot.image_coordinates, detected_coords) >= ImageProcessor.MIN_OVERLAP:
                    # update the spot to full and save it
                    spot = sector_spot.spot
                    spot.full = True
                    spot.save(['full'])

    @staticmethod
    def getCoordsFromImage(image_name):
        execution_path = os.getcwd()

        #FIXME adjust image path
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
        # detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()

        custom_objects = detector.CustomObjects(car=True, motorcycle=True)
        detections = detector.detectCustomObjectsFromImage(custom_objects=custom_objects, input_image=os.path.join(execution_path ,image_name + ".jpg"), output_image_path=os.path.join(execution_path , image_name+"_processed.jpg"), minimum_percentage_probability=40)

        coords = []

        for eachObject in detections:
            coords.append(eachObject['box_points'].tolist())

        return coords

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
