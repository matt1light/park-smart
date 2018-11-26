# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from .ImageProcessorServer import ImageProcessorServerImageAI, ImageProcessorServerVisionAPI

from mainModels.models import Spot, SectorSpot, ParkingLot, Sector, ImageCoordinates, Image, ParkingEvent

# Non persistant static class
# processor is not an object
class ImageProcessor(models.Model):
    MIN_OVERLAP = 0.4
    class Meta:
        managed = False

    def __init__(self, server):
        self.server = server

    # Creates spots based on the identified cars in an image and adds them to a specified sector
    # Input: name of image to be processed, sector for spots to be added to
    def addSpotsToSector(self, image_name, sector):
        # get coordinates for new spots
        new_coords = self.server.get_car_coordinates(image_name)
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
    def updateSector(self, sector):
        # get the latest image for this sector
        images = Image.objects.filter(sector=sector).order_by('-id')
        latest_image = images[0]
        image_path = latest_image.photo.url[1:]
        # update the sector with the latest image
        self.updateSectorByImage(image_path, sector)

    # Updates a sector's spot statuses with a picture input
    def updateSectorByImage(self, image_name, sector):
        # use object recognition to find coordinates
        detected_coords = self.server.get_car_coordinates(image_name)
        # for each coordinate in the detected coordinates
        for sector_spot in sector.sector_spots.all():
            # compare to the possible coordinates
            spot_full = False
            spot = sector_spot.spot
            for coord in detected_coords:
                # if the coordinates intersect by more than the MIN_OVERLAP
                if self.calculateOverlapPercentage(sector_spot.image_coordinates, coord) >= self.MIN_OVERLAP and spot.full==False:
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


    # Takes the input of the coordinates of two rectangles and determinest the percentage that they overlap
    def calculateOverlapPercentage(self, spot_coords, detected_coords):
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
