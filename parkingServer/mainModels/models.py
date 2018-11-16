from django.db import models

# Create your models here.

class ParkingLot(models.Model):
    name = models.TextField()
    description = models.TextField()

# lot state
class LotState(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, related_name='lot_state', on_delete=models.CASCADE)
    active = models.BooleanField()

# lot-state sector
class Sector(models.Model):
    lot_state = models.ForeignKey(LotState, related_name='sectors', on_delete=models.CASCADE)
    x_index = models.IntegerField()
    y_index = models.IntegerField()

class Row(models.Model):
    lot_state = models.ForeignKey(LotState, related_name='rows', on_delete=models.CASCADE)
    active = models.BooleanField()

class Spot(models.Model):
    row = models.ForeignKey(Row, related_name='spots', null= True, on_delete=models.SET_NULL)
    active = models.BooleanField()
    full = models.BooleanField()

class ImageCoordinates(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()

class SectorSpot(models.Model):
    sector = models.ForeignKey(Sector, related_name='sector_spots', on_delete=models.CASCADE)
    spot = models.OneToOneField(Spot, related_name='sector_spot', on_delete=models.SET_NULL, null=True)
    image_coordinates = models.OneToOneField(ImageCoordinates, related_name='sector_spot', on_delete=models.CASCADE)

class Image(models.Model):
    sector = models.ForeignKey(Sector, related_name='images', on_delete=models.SET_NULL, null=True)
    photo = models.ImageField()
    time_taken = models.DateTimeField()

class Input(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, related_name='inputs', on_delete=models.CASCADE)

class CameraHubInput(Input):
    ip_address = models.IntegerField()
    hubId = models.IntegerField()

class Camera(models.Model):
    camera_hub = models.ForeignKey(CameraHubInput, related_name='cameras', on_delete=models.CASCADE)
    # this might not exist later but as is we want cameras to be represented as hubID.camID
    camId = models.IntegerField()

class Output(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, related_name='outputs', on_delete=models.CASCADE)

class ArduinoOutput(Output):
    ip_address = models.TextField()
