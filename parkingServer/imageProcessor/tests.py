# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import ImageProcessor
from mainModels.models import Spot, Sector, SectorSpot, LotState
import numpy as np

# Create your tests here.

# Test that the imageprocessor can process an image based on a sector
class ImageProcessorUnitTests(TestCase):
    fixtures=['data']

    def setUp(self):
        # add image to database
        # add spots to database
        # add data to database
        # FIXME this is a hardcoded value generate dynamically?
        self.FULL_SPOTS = [
            {
                'id': 1,
                'full': True
            },
            {
                'id': 2,
                'full': True
            },
            {
                'id': 3,
                'full': True
            },
            {
                'id': 4,
                'full': True
            },
            {
                'id': 5,
                'full': True
            },
            {
                'id': 6,
                'full': True
            },
        ]
        return

    def test_calibrate(self):
        # create new sector object
        sector = Sector.objects.create(lot_state=LotState.objects.get(pk=1), x_index=0, y_index=0)
        # test2 has a picture with 5 cars thus should add 4 sector spots
        expected_number_of_spots = 5
        image_name = "../test_resources/test_pics/test2"
        ImageProcessor.addSpotsToSector(image_name, sector)
        new_sector_spots = SectorSpot.objects.all()

        # assert that there have been spots added to the database table
        self.assertEqual(len(new_sector_spots), expected_number_of_spots)
        # assert that each of those spots has been added to correct sector
        # assert that each of those spots has a ImageCoordinate and a Spot
        self.assertTrue(all([(ss.sector == sector and ss.spot is not None and ss.image_coordinates is not None) for ss in new_sector_spots]))


    # def test_get_coords_from_image(self):
    #     image_location = 'test_pics/test1'
    #     coordinates = [[570, 103, 593, 114],
    #         [614, 107, 639, 121],
    #         [446, 114, 497, 132],
    #         [460, 119, 498, 133],
    #         [320, 123, 361, 141],
    #         [480, 129, 544, 154],
    #         [189, 146, 209, 157],
    #         [98, 152, 144, 186],
    #         [178, 155, 225, 186],
    #         [303, 164, 337, 189],
    #         [345, 160, 375, 186],
    #         [386, 160, 418, 189],
    #         [421, 159, 460, 189],
    #         [467, 134, 524, 172],
    #         [467, 140, 513, 191],
    #         [5, 152, 65, 189],
    #         [225, 158, 260, 185],
    #         [548, 159, 594, 208],
    #         [240, 207, 295, 244],
    #         [26, 209, 108, 272],
    #         [96, 199, 165, 267],
    #         [295, 206, 347, 266],
    #         [407, 204, 478, 275],
    #         [530, 207, 614, 271],
    #         [232, 210, 294, 272],
    #         [467, 220, 541, 270],
    #         [287, 262, 348, 352],
    #         [114, 255, 195, 337],
    #         [71, 205, 145,270]]
    #
    #     test_data = [{
    #         'name': 'Test 1',
    #         'image_location': image_location,
    #         'coordinates': coordinates,
    #         'result': 'pass'
    #     }]
    #
    #     for row in test_data:
    #         # FIXME this test might have to be updated to round coordinates to be close but not quite what they are as this may not be a deterministic operation
    #
    #         processed_coordinates = ImageProcessor.getCoordsFromImage(row['image_location'])
    #         flattened_processed_coordinates = [val for sublist in processed_coordinates for val in sublist]
    #         flattened_expected_coordinates = [val for sublist in row['coordinates'] for val in sublist]
    #         self.assertCountEqual(flattened_expected_coordinates, flattened_processed_coordinates)

    # def test_update_sector_by_image(self):
    #     image_location =
    #     sector =
    #
    #     test_data = [{
    #         'name': 'Full',
    #         'image_location': image_location,
    #         'sector': sector,
    #         'expected_spots': self.FULL_SPOTS,
    #         'result': 'pass'
    #     }]
    #
    #     for row in test_data:
    #         ImageProcessor.updateSectorByImage(row['image_location'], row['sector'])
    #         # check to see if the appropriate spots are updated
    #         for expected_spot in row['spots']:
    #             spot = Spot.objects.get(expected_spot['id'])
    #             self.assertEquals(spot.full, expected_spot['full'])
    #
    # def test_update_sector(self):
    #     sector =
    #
    #     test_data = [{
    #         'name': 'Full',
    #         'sector': sector,
    #         'expected_spots': self.FULL_SPOTS,
    #         'result': 'pass'
    #     }]
    #
    #     for row in test_data:
    #         ImageProcessor.updateSector(row['sector'])
    #
    #         for expected_spot in row['expected_spots']:
    #             spot = Spot.objects.get(expected_spot['id'])
    #             self.
    # assertEquals(spot.full, expected_spot['full'])
