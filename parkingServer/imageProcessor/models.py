# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from mainModels.models import Spot, SectorSpot, ParkingLot, Sector, ImageCoordinates, Image, ParkingEvent
from .ImageProcessorServer import ImageProcessorServer

# Non persistant static class
# processor is not an object
class ImageProcessor(models.Model):
    MIN_OVERLAP = 0.4

    class Meta:
        managed = False

    # constructs a new image processor with a specified server to handle the ObjectRecognition
    def __init__(self, server:ImageProcessorServer):
        self.server = server

    # Creates spots based on the identified cars in an image and adds them to a specified sector
    # Input: name of image to be processed, sector for spots to be added to
    def calibrate_sector(self, image_name, sector):
        print("\nCalibrating sector: #" + str(sector.pk))
        # get coordinates for new spots
        new_coords = self.server.get_car_coordinates(image_name)
        # for each spot create a SectorSpot and add the coordinates
        for new_spot_coords in new_coords:
            print("\n.")
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
    def update_sector_with_latest(self, sector):
        # get the latest image for this sector
        images = Image.objects.filter(sector=sector).order_by('-id')
        latest_image = images[0]
        image_path = latest_image.photo.url[1:]
        # update the sector with the latest image
        self.update_sector_by_image_name(image_path, sector)

    def update_sector_from_image(self, image):
        image_name = image.photo.url[1:]
        sector = image.sector

        self.update_sector_by_image_name(image_name, sector)

    # Updates a sector's spot statuses with a picture input
    def update_sector_by_image_name(self, image_name:str, sector):
        # use object recognition to find coordinates
        detected_coords = self.server.get_car_coordinates(image_name)
        # for each coordinate in the detected coordinates
        for sector_spot in sector.sector_spots.all():
            # compare to the possible coordinates
            spot_full = False
            spot = sector_spot.spot
            for coord in detected_coords:
                # if the coordinates intersect by more than the MIN_OVERLAP
                if self.__calculate_overlap_percentage(sector_spot.image_coordinates, coord) >= self.MIN_OVERLAP and spot.full==False:
                    # update the spot to full and save it
                    print("New car found in \n\tsector: " + str(sector.pk) + "\n\tspot: " + str(spot.pk))
                    spot.full = True
                    spot.last_park = timezone.now()
                    spot.save(update_fields=["last_park", "full"])
                    new_car_in_spot = True
            # if the spot is empty in the picture but not in the database update the database entry
            if not new_car_in_spot and spot.full:
                print("Car left spot in \n\tsector:" + str(sector.pk) + "\n\tspot: " + str(spot.pk))
                ParkingEvent.objects.create(spot=spot,
                                            parking_start=spot.last_park,
                                            parking_end=timezone.now())

                spot.full = False
                spot.last_park = None
                spot.save(update_fields=["last_park", "full"])


    # helper method
    # Takes the input of the coordinates of two rectangles and determinest the percentage that they overlap
    def __calculate_overlap_percentage(self, spot_coords, detected_coords):
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
