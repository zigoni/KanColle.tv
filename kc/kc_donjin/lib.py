import os
import rarfile
from django.conf import settings


def handle_uploaded_file(f):
    path = os.path.join(settings.BASE_DIR, 'tmp', f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if rarfile.is_rarfile(path):
        return path
    else:
        os.unlink(path)
        return False