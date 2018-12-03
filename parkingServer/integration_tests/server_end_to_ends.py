from mainModels.models import ParkingLot, LotState, Sector, Image, Row, Spot, ArduinoOutput, SectorSpot
from imageProcessor.models import ImageProcessor
from django.utils import timezone
import json
from imageProcessor.ImageProcessorServer import ImageProcessorServerImageAI

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

class ImageInDisplayOut(TestCase):

    @classmethod
    def setUpTestData(cls):
        # add ParkingLot
        cls.parking_lot = ParkingLot.objects.create(description = "", name= "")
        # add LotState
        cls.lot_state = LotState.objects.create(parking_lot=cls.parking_lot, active=True)
        # add 2 Sectors
        cls.sector1 = Sector.objects.create(lot_state=cls.lot_state, x_index=0, y_index=0, cameraID= "1.1")
        cls.sector2 = Sector.objects.create(lot_state=cls.lot_state, x_index=1, y_index=0, cameraID="1.2")
        # add 2 Rows
        cls.top_row = Row.objects.create(lot_state=cls.lot_state, active=True)
        cls.bottom_row = Row.objects.create(lot_state=cls.lot_state, active=True)
        # use calibrate to add spots
        # dump this json
        cls.output = ArduinoOutput.objects.create(parking_lot=cls.parking_lot, ip_address="192.1.1.1")
        # calibrate
        server = ImageProcessorServerImageAI()
        cls.processor = ImageProcessor(server)
        cls.processor.calibrate_sector("../test_resources/test_pics/e2esituations/e2e3.jpg", cls.sector1)
        # add spots to the two rows
        Spot.objects.filter(pk__range=(1,4)).update(row=cls.top_row)
        Spot.objects.filter(pk__range=(5,8)).update(row=cls.bottom_row)

    def setUp(self):
        self.client = APIClient()


    def test_save_image_triggers_signal(self):

        p = open('../test_resources/test_pics/e2esituations/e2e3.jpg', 'rb')

        file = SimpleUploadedFile(name=p.name, content=p.read())

        Image.objects.create(sector=self.sector1, time_taken=timezone.now(), photo=file)
        sector = Sector.objects.filter(pk=self.sector1.pk)

        self.sector1.refresh_from_db()
        for sector_spot in self.sector1.sector_spots.all():
            self.assertEqual(sector_spot.spot.full, True)


    # def test_full_back_row(self):
    #     # simulate the pi sending the image
    #
    #     input_response = self.send_image("../test_resources/test_pics/e2esituations/e2e1.jpg", self.sector1)
    #
    #
    #     # force image processor to update sector
    #     self.processor.update_sector_with_latest(self.sector1)
    #
    #     response = self.client.get(
    #         '/displayState/',
    #         {'output': 1})
    #
    #     dict_content = json.loads(response.content.decode('utf-8'))
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(dict_content["lightState"], [3, 1])
    #     self.assertEqual(dict_content["signState"]["num_active_spots"], 8)
    #     self.assertEqual(dict_content["signState"]["num_full_spots"], 4)
    #
    # def test_full_front_row(self):
    #     # simulate the pi sending the image
    #
    #     input_response = self.send_image("../test_resources/test_pics/e2esituations/e2e4.jpg", self.sector1)
    #
    #     # force image processor to update sector
    #     self.processor.update_sector_with_latest(self.sector1)
    #
    #     response = self.client.get(
    #         '/displayState/',
    #         {'output': 1})
    #
    #     dict_content = json.loads(response.content.decode('utf-8'))
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(dict_content["lightState"], [1, 3])
    #     self.assertEqual(dict_content["signState"]["num_active_spots"], 8)
    #     self.assertEqual(dict_content["signState"]["num_full_spots"], 4)
    #
    # def test_empty(self):
    #     # simulate the pi sending the image
    #
    #     input_response = self.send_image("../test_resources/test_pics/e2esituations/empty.jpg", self.sector1)
    #
    #     # force image processor to update sector
    #     self.processor.update_sector_with_latest(self.sector1)
    #
    #     response = self.client.get(
    #         '/displayState/',
    #         {'output': 1})
    #
    #     dict_content = json.loads(response.content.decode('utf-8'))
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(dict_content["lightState"], [1, 1])
    #     self.assertEqual(dict_content["signState"]["num_active_spots"], 8)
    #     self.assertEqual(dict_content["signState"]["num_full_spots"], 0)
    #
    # def test_full(self):
    #     # simulate the pi sending the image
    #
    #     input_response = self.send_image("../test_resources/test_pics/e2esituations/e2e3.jpg", self.sector1)
    #
    #     # force image processor to update sector
    #     self.processor.update_sector_with_latest(self.sector1)
    #
    #     response = self.client.get(
    #         '/displayState/',
    #         {'output': 1})
    #
    #     dict_content = json.loads(response.content.decode('utf-8'))
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(dict_content["lightState"], [3, 3])
    #     self.assertEqual(dict_content["signState"]["num_active_spots"], 8)
    #     self.assertEqual(dict_content["signState"]["num_full_spots"], 8)
    #
    #
    # def send_image(self, photo_path, sector):
    #     time_now = timezone.now()
    #     p = open(photo_path, 'rb')
    #
    #     data = {
    #         "images": [
    #             {
    #                 "cameraID": sector.pk,
    #                 "photo": photo_path,
    #                 "time_taken": str(time_now)
    #             }
    #         ],
    #         photo_path: p,
    #     }
    #
    #     return self.client.post(
    #         "/image-collection/", data=data, format="multipart"
    #     )
