# -*-  coding: utf-8 -*-
"""project settings"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
__author__ = 'Evren Esat Ozkan'
from zengine.settings import *
import os.path

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_LANG = 'tr'

# path of the activity modules which will be invoked by workflow tasks
ACTIVITY_MODULES_IMPORT_PATHS.extend(['ulakbus.views', 'ulakbus.tasks'])
# absolute path to the workflow packages
WORKFLOW_PACKAGES_PATHS.append(os.path.join(BASE_DIR, 'diagrams'))

AUTH_BACKEND = 'ulakbus.models.auth.AuthBackend'

PERMISSION_MODEL = 'ulakbus.models.auth.Permission'
USER_MODEL = 'ulakbus.models.auth.User'
ROLE_MODEL = 'ulakbus.models.auth.Role'
# # left blank to use StreamHandler aka stderr
# LOG_HANDLER = os.environ.get('LOG_HANDLER', 'file')
#
# # logging dir for file handler
# LOG_DIR = os.environ.get('LOG_DIR', '/tmp/')

# DEFAULT_CACHE_EXPIRE_TIME = 99999999  # seconds

# diagrams that does not require logged in user
ANONYMOUS_WORKFLOWS = ['login', 'logout']

# #PYOKO SETTINGS
DEFAULT_BUCKET_TYPE = os.environ.get('DEFAULT_BUCKET_TYPE', 'models')

DATE_DEFAULT_FORMAT = "%d.%m.%Y"
DATETIME_DEFAULT_FORMAT = "%d.%m.%Y %H:%s"

DEFAULT_WF_CATEGORY_NAME = 'Genel'
DEFAULT_OBJECT_CATEGORY_NAME = 'Seçime Uygun Görevler'

OBJECT_MENU = {
    # 'personel|ogrenci|personeller|ogrenciler': [{'name':'ModelName',
    #                                             'field':'field_name',
    #                                             'verbose_name': 'verbose_name',
    #                                             'category': 'Genel'
    #                                             'wf':'crud'}]
    # 'field' defaults to 'personel' or 'ogrenci'
    # verbose_name can be specified to override the model's verbose_name_plural
    'other': [
        {'name': 'Personel', 'category': 'Genel'},
        {'name': 'Ogrenci', 'category': 'Genel'},
        {'name': 'Okutman', 'category': 'Genel'},
        {'name': 'HariciOkutman', 'category': 'Genel'},
        {'name': 'Donem', 'category': 'Genel'},
        {'name': 'Program', 'category': 'Genel'},
        {'name': 'Ders', 'category': 'Genel'},
        {'name': 'Campus', 'category': 'Genel'},
        {'name': 'Building', 'category': 'Genel'},
        {'name': 'Room', 'category': 'Genel'},
        {'name': 'AkademikTakvim', 'category': 'Genel'},
        {'name': 'OgrenciProgram', 'category': 'Genel'},
    ],
    'personel': [
        {'name': 'Personel', 'field': 'object_id', 'wf': 'kimlik_ve_iletisim_bilgileri',
         'verbose_name': 'Kimlik ve Iletisim Bilgileri', 'field': 'personel_id'},
        {'name': 'HizmetKayitlari', 'verbose_name': 'Hizmet Cetveli', 'field': 'personel_id'},
        {'name': 'Izin', 'wf': 'izin', 'verbose_name': 'İzin İşlemleri', 'field': 'personel_id'},
        {'name': 'UcretsizIzin', 'wf': 'ucretsiz_izin', 'verbose_name': 'Ücretsiz İzin İşlemleri',
         'field': 'personel_id'},
        {'name': 'KurumDisiGorevlendirmeBilgileri', 'field': 'personel_id'},
        {'name': 'KurumIciGorevlendirmeBilgileri', 'field': 'personel_id'},
        {'name': 'AdresBilgileri', 'verbose_name': 'Adres Bilgileri', 'field': 'personel_id'},
        {'name': 'HizmetKurs', 'field': 'personel_id'},
        {'name': 'HizmetOkul', 'field': 'personel_id'},
        {'name': 'HizmetMahkeme', 'field': 'personel_id'},
        {'name': 'HizmetBirlestirme', 'verbose_name': 'Hizmet Birleştirme',
         'field': 'personel_id'},
        {'name': 'HizmetTazminat', 'verbose_name': 'Tazminat Bilgileri', 'field': 'personel_id'},
        {'name': 'HizmetUnvan', 'verbose_name': 'Ünvan', 'field': 'personel_id'},
        {'name': 'HizmetAcikSure', 'verbose_name': 'Açık Süre Bilgileri', 'field': 'personel_id'},
        {'name': 'HizmetBorclanma', 'verbose_name': 'Borçlanma Bilgileri', 'field': 'personel_id'},
        {'name': 'HizmetIHS', 'field': 'personel_id'},
        {'name': 'HizmetIstisnaiIlgi', 'field': 'personel_id'},
        {'name': 'AskerlikKayitlari', 'verbose_name': 'Askerlik Kayıtları',
         'field': 'personel_id'},
        {'name': 'Atama', 'field': 'personel_id'},
        # {'name': 'Kadro'        , 'field': 'personel_id'},
    ],
    'ogrenci': [
        {'name': 'DersKatilimi', 'verbose_name': 'Devam Durumu', 'field': 'ogrenci_id'},
        {'name': 'Borc', 'verbose_name': 'Harç Bilgileri', 'field': 'ogrenci_id'},
        {'name': 'DegerlendirmeNot', 'field': 'ogrenci_id'},
        {'name': 'OgrenciDersi', 'field': 'ogrenci_id'},
        {'name': 'Ogrenci', 'field': 'object_id', 'wf': 'ogrenci_kimlik_bilgileri',
         'verbose_name': 'Kimlik Bilgileri'},
        {'name': 'Ogrenci', 'field': 'object_id', 'wf': 'ogrenci_iletisim_bilgileri',
         'verbose_name': 'İletişim Bilgileri'},
        {'name': 'OncekiEgitimBilgisi', 'verbose_name': 'Önceki Eğitim Bilgileri',
         'field': 'ogrenci_id'},
        {'name': 'OgrenciProgram', 'field': 'ogrenci_id', 'wf': 'danisman_atama',
         'verbose_name': 'Danışman Atama'},
    ],
}

VIEW_URLS = [
    # ('falcon URI template', 'python path to view method/class')
    ('/ara/ogrenci/{query}', 'ulakbus.views.system.SearchStudent'),
    ('/ara/personel/{query}', 'ulakbus.views.system.SearchPerson'),
    ('/notify/', 'ulakbus.views.system.Notification'),
    ('/get_current_user/', 'ulakbus.views.system.GetCurrentUser'),
    ('/menu', 'ulakbus.views.system.UlakbusMenu'),
]

ZATO_SERVER = os.environ.get('ZATO_SERVER', 'http://localhost:11223')

ENABLE_SIMPLE_CRUD_MENU = False

ALLOWED_ORIGINS += [
    'http://ulakbus.net',
    'http://www.ulakbus.net',
    'http://dev.zetaops.io',
    'http://nightly.zetaops.io',
]

UID = 173500

FILE_MANAGER = 'ulakbus.lib.s3_file_manager.S3FileManager'
ALLOWED_FILE_TYPES = {
    'png': ('image/png', 'png'),
    'txt': ('text/plain', 'txt'),
    'jpg': ('image/jpeg', 'jpg'),
    'jpeg': ('image/jpeg', 'jpg'),
    'pdf': ('application/pdf', 'pdf'),
    'doc': ('application/msword', 'doc'),
    'xls': ('application/vnd.ms-excel', 'xls'),
    'ppt': ('application/vnd.ms-powerpoint', 'ppt'),
    'pptx': ('application/vnd.openxmlformats-officedocument.presentationml.presentation', 'pptx'),
    'xlsx': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xlsx'),
    'docx': ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx'),
}

S3_PROXY_URL = os.environ.get('S3_PROXY_URL')
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY')
S3_PUBLIC_URL = os.environ.get('S3_PUBLIC_URL')
S3_PROXY_PORT = os.environ.get('S3_PROXY_PORT', '8080')
S3_BUCKET_NAME = 'ulakbus'

QUICK_MENU = [
    'kadro_islemleri',
    # 'izin',
    'akademik_takvim',
    'ders_hoca_sube_atama',
    'ders_ekle',
    'Birim',
    'Ders',
    'Program'
]

MAX_NUM_DROPDOWN_LINKED_MODELS = 20

PERMISSION_PROVIDER = 'ulakbus.models.auth.ulakbus_permissions'


ERROR_MESSAGE_500 = "DEMO Sisteminde güncelleme nedeniyle kesinti ve hata olabilir." \
                    "Şimdi bunlardan birini görüyorsunuz. Lütfen daha sonra tekrar deneyiniz"
