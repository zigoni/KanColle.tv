import os
from django.conf import settings


KC_DOUJIN_UPLOAD_DIR = os.path.join(settings.BASE_DIR, '_rar')
KC_DOUJIN_IMAGE_EXT = ('jpg', 'png')
KC_DOUJIN_IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'doujin')
KC_DOUJIN_ITEM_PER_PAGE = 50
KC_PRIVILEGE_GROUPS = (
    {'doujin_publisher'},
    {'doujin_uploader'},
)