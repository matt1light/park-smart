# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import ImageProcessor
from mainModels.models import Spot, Sector, SectorSpot, LotState
from .ImageProcessorServer import ImageProcessorServerImageAI, ImageProcessorServerVisionAPI, ImageProcessorServerExternalImageAI

# Create your tests here.

# Test that the imageprocessor can process an image based on a sector
class ImageProcessorUnitTests(TestCase):
    fixtures=['../test_resources/fixtures/data.json']

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
        server = ImageProcessorServerExternalImageAI()
        self.imageProcessor = ImageProcessor(server)
        return

    def test_calibrate(self):
        # create new sector object
        sector = Sector.objects.create(lot_state=LotState.objects.get(pk=1), x_index=0, y_index=0)
        # test2 has a picture with 5 cars thus should add 4 sector spots
        expected_number_of_spots = 5
        image_name = "../test_resources/test_pics/e2esituations/fullish.jpg"
        self.imageProcessor.calibrate_sector(image_name, sector)
        new_sector_spots = SectorSpot.objects.filter(sector=sector)

        # assert that there have been spots added to the database table
        self.assertEqual(len(new_sector_spots), expected_number_of_spots)
        # assert that each of those spots has been added to correct sector
        # assert that each of those spots has a ImageCoordinate and a Spot
        self.assertTrue(all([(ss.sector == sector and ss.spot is not None and ss.image_coordinates is not None) for ss in new_sector_spots]))


    # def test_get_coords_from_image(self):
    #     image_location = '../test_resources/test_pics/test1.jpg'
    #     coordinates = [
    #
    #     ]
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
    #         processed_coordinates = self.imageProcessor.getCoordsFromImage(row['image_location'])
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
    #         self.imageProcessor.updateSectorByImage(row['image_location'], row['sector'])
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
    #         self.imageProcessor.updateSector(row['sector'])
    #
    #         for expected_spot in row['expected_spots']:
    #             spot = Spot.objects.get(expected_spot['id'])
    #             self.
    # assertEquals(spot.full, expected_spot['full'])
