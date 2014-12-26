import os
import patoolib
import hashlib
import shutil
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
    try:
        patoolib.test_archive(path)
    except patoolib.util.PatoolError:
        os.unlink(path)
        raise UploadedFileFormatError

    tmp_dir = os.path.join(KC_DOUJIN_UPLOAD_DIR, hashlib.md5(path.encode()).hexdigest())
    os.mkdir(tmp_dir)
    patoolib.extract_archive(path, outdir=tmp_dir)

    cnt = 0
    for root, dirs, files in os.walk(tmp_dir):
        for file in files:
            if file.index('.') >= 0:
                ext = file.split('.')[-1].lower()
                if ext in KC_DOUJIN_IMAGE_EXT:
                    cnt += 1
    shutil.rmtree(tmp_dir)
    if cnt >= 2:
        return path
    else:
        os.unlink(path)
        raise UploadedFileContentError


def extract_rar_file(file):
    extract_dir = os.path.join(KC_DOUJIN_IMAGE_DIR, file.get_extract_dir())
    path = os.path.join(KC_DOUJIN_UPLOAD_DIR, file.file_name)

    tmp_dir = os.path.join(KC_DOUJIN_UPLOAD_DIR, hashlib.md5(path.encode()).hexdigest())
    os.mkdir(tmp_dir)
    patoolib.extract_archive(path, outdir=tmp_dir)

    img_list = []
    for root, dirs, files in os.walk(tmp_dir):
        for f in files:
            if f.index('.') >= 0:
                ext = f.split('.')[-1].lower()
                if ext in KC_DOUJIN_IMAGE_EXT:
                    img_list.append(os.path.join(root, f))
                    print(os.path.join(root, f))

    img_list = natsort.natsorted(img_list)
    pages = len(img_list)

    if not os.path.exists(extract_dir):
        os.mkdir(extract_dir)

    for p in range(pages):
        img = Image.open(img_list[p])
        w, h = img.size
        if h > 1080:
            new_w = int(float(w) / float(h) * 1080 + 0.5)
            img.thumbnail((new_w, 1080), Image.ANTIALIAS)
        save_path = os.path.join(extract_dir, '%d.jpg' % (p+1))
        img.save(save_path)

    cover = Image.open(img_list[0])
    w, h = cover.size
    new_h = int(float(h) / float(w) * 165 + 0.5)
    cover.thumbnail((165, new_h), Image.ANTIALIAS)
    cover.save(os.path.join(extract_dir, 'cover_thumbnail.jpg'))

    shutil.rmtree(tmp_dir)
    return pages