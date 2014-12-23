import os
import rarfile
from kc_donjin.config import *


def handle_uploaded_file(f):
    fn = f.name
    if fn.find('.') == -1:
        fn += '.rar'
    path = os.path.join(KC_DONJIN_UPLOAD_DIR, fn)

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if rarfile.is_rarfile(path):
        rf = rarfile.RarFile(path)
        cnt = 0
        for f in rf.infolist():
            if not f.isdir():
                ext = f.filename.split('.')[-1].lower()
                if ext in KC_DONJIN_IMAGE_EXT:
                    cnt += 1
        if cnt >= 2:
            return path
    os.unlink(path)
    return False