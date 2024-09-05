from .base import *


DEBUG = True
ALLOWED_HOSTS = ['localhost','127.0.0.1', 'recipe-api-4ytq.onrender.com',]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
