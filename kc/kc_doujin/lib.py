import os
import rarfile
import natsort
from PIL import Image
from kc_doujin.config import KC_DOUJIN_UPLOAD_DIR, KC_DOUJIN_IMAGE_EXT, KC_DOUJIN_IMAGE_DIR
from kc_doujin.exceptions import *


def handle_uploaded_file(f):
    fn = f.name
    if fn.find('.') == -1:
        fn += '.rar'
    path = os.path.join(KC_DOUJIN_UPLOAD_DIR, fn)
    if os.path.exists(path):
        raise UploadedFileExists

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if rarfile.is_rarfile(path):
        rf = rarfile.RarFile(path)
        cnt = 0
        for f in rf.infolist():
            if not f.isdir():
                ext = f.filename.split('.')[-1].lower()
                if ext in KC_DOUJIN_IMAGE_EXT:
                    cnt += 1
        if cnt >= 2:
            return path
        else:
            os.unlink(path)
            raise UploadedFileContentError

    os.unlink(path)
    raise UploadedFileFormatError


def extract_rar_file(file):
    extract_dir = os.path.join(KC_DOUJIN_IMAGE_DIR, file.get_extract_dir())
    path = os.path.join(KC_DOUJIN_UPLOAD_DIR, file.file_name)
    rf = rarfile.RarFile(path)

    img_list = []
    for f in rf.infolist():
        if not f.isdir():
            ext = f.filename.split('.')[-1].lower()
            if ext in KC_DOUJIN_IMAGE_EXT:
                img_list.append(f.filename)
    img_list = natsort.natsorted(img_list)
    pages = len(img_list)

    if not os.path.exists(extract_dir):
        os.mkdir(extract_dir)

    for f in rf.infolist():
        fn = f.filename
        if fn in img_list:
            p = img_list.index(fn)
            ext = img_list[p].split('.')[-1].lower()
            extract_path = os.path.join(extract_dir, '%d.%s' % (p+1, ext))
            data = rf.read(f)
            open(extract_path, 'wb').write(data)

    cover = Image.open(os.path.join(extract_dir, '1.%s' % img_list[0].split('.')[-1].lower()))
    w, h = cover.size
    new_h = int(float(h) / float(w) * 165)
    cover.thumbnail((165, new_h), Image.ANTIALIAS)
    cover.save(os.path.join(extract_dir, 'cover_thumbnail.jpg'))

    return pages