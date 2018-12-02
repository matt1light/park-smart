from mainModels.models import Image
from imageProcessor.models import ImageProcessor
from imageProcessor.ImageProcessorServer import ImageProcessorServerImageAI, ImageProcessorServerExternalImageAI
from django.db.models.signals import post_save
from django.dispatch import receiver

from parkingServer.parkingServer.settings import IMAGE_PROCESSING_SERVER_IP

@receiver(post_save, sender=Image)
def update_sector_on_image_save(sender, instance, **kwargs):
    if not IMAGE_PROCESSING_SERVER_IP:
        server = ImageProcessorServerImageAI()
    else:
        server = ImageProcessorServerExternalImageAI()
    processor = ImageProcessor(server)
    processor.update_sector_from_image(instance)
