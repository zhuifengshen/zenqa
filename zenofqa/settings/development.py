from .common import *

SECRET_KEY = 'development-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
CACHE = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMenCache',
  }
}
