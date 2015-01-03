from kc_base.exceptions import GeneralViewException


class UploadedFileExists(Exception):
    pass


class UploadedFileFormatError(Exception):
    pass


class UploadedFileContentError(Exception):
    pass


class DoujinMgtException(GeneralViewException):
    template = 'kc_doujin/mgt_error.html'
    views = ()
    picture = ''


class DoujinMgtUploadError(DoujinMgtException):
    views = (
        {'url': 'kc-doujin-list-comic', 'name': '返回漫画管理'},
    )
    picture = 'img/doujin_upload.png'


class DoujinMgtComicError(DoujinMgtException):
    views = (
        {'url': 'kc-doujin-list-comic', 'name': '返回漫画管理'},
    )
    picture = 'img/doujin_manage.png'