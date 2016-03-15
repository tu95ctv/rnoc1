import os
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from django.utils import timezone
import datetime
print timezone.now()
print datetime.datetime.now()
print timezone.localtime(timezone.now())