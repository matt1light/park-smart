from abc import abstractmethod
from .ImageAI import getCoordsFromImageResnet
from .visionAPI import localize_objects

class ImageProcessorServer():

    @abstractmethod
    def get_car_coordinates(image_path):
        print("implement this method")

class ImageProcessorServerVisionAPI(ImageProcessorServer):

    @staticmethod
    def get_car_coordinates(image_path):
        return localize_objects(image_path)

class ImageProcessorServerImageAI(ImageProcessorServer):

    @staticmethod
    def get_car_coordinates(image_path):
        return getCoordsFromImageResnet(image_path)
