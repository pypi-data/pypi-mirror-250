from html2image import Html2Image
from PIL import Image
from aia_utils.logs_cfg import config_logger
import logging
config_logger()
logger = logging.getLogger(__name__)

class ImageUtils:

    def __init__(self, output_path='target'):
        logger.info('ImageUtils Initialized')
        self.output_path = output_path
        self.hti = Html2Image(output_path=self.output_path)

    
    def html2img(self, name, html, css, size: tuple=(1100, 1400)):
        logger.info('html2img')
        self.hti.screenshot(html_str=html, css_str=css, save_as=name, size=size)
        im = Image.open(f"{self.output_path}/{name}")
        return im
    
