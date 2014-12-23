import os
from django.conf import settings


KC_DONJIN_UPLOADER = 'donjin_uploader'
KC_DONJIN_PUBLISHER = 'donjin_publisher'
KC_DONJIN_UPLOAD_DIR = os.path.join(settings.BASE_DIR, '_rar')
KC_DONJIN_IMAGE_EXT = ('jpg', 'png')
KC_DONJIN_IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'donjin')