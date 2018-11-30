from mainModels.models import Image
from imageProcessor.models import ImageProcessor
from imageProcessor.ImageProcessorServer import ImageProcessorServerImageAI
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Image)
def update_sector_on_image_save(sender, instance, **kwargs):
    server = ImageProcessorServerImageAI()
    processor = ImageProcessor(server)
    processor.update_sector_from_image(instance)
