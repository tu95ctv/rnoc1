# -*- coding: utf-8 -*- 
import os
from xu_ly_db_3g import read_line, DATE_FORMAT_FOR_BCN
from rnoc.models import Mll, Tram, DuAn, BCNOSS
from rnoc.forms import MllForm
from django.contrib.auth.models import User
import datetime
from django.db.models.aggregates import Sum
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from django.db.models.aggregates import Sum
from django.db.models import Avg
if __name__ == '__main__':
    print type(MllForm.su_co).__name__