import re
import os
import datetime

SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from rnoc.models import Nguyennhan
if __name__ == '__main__':
    print datetime.datetime.now()
    
