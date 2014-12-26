import os
from django.conf import settings


KC_DOUJIN_UPLOADER = 'donjin_uploader'
KC_DOUJIN_PUBLISHER = 'donjin_publisher'
KC_DOUJIN_UPLOAD_DIR = os.path.join(settings.BASE_DIR, '_rar')
KC_DOUJIN_IMAGE_EXT = ('jpg', 'png')
KC_DOUJIN_IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'doujin')

KC_DOUJIN_ITEM_PER_PAGE = 50