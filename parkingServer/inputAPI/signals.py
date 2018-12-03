from django.db.models.signals import post_save
from django.dispatch import receiver
from mainModels.models import Image
from imageProcessor.ImageProcessorServer import ImageProcessorServerImageAI, ImageProcessorServerExternalImageAI
from imageProcessor.models import ImageProcessor
from parkingServer.settings import IMAGE_PROCESSING_SERVER_IP
import pdb

@receiver(post_save, sender=Image)
def update_spots_on_image_save(sender, instance, **kwargs):
    if not IMAGE_PROCESSING_SERVER_IP:
        server = ImageProcessorServerImageAI()
    else:
        server = ImageProcessorServerExternalImageAI()
    processor = ImageProcessor(server)
    processor.update_sector_from_image(instance)
