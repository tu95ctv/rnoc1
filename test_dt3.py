# -*- coding: utf-8 -*- 
import os
import re
import sys
from django.utils.translation import ungettext







#from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')

from drivingtest.forms import CommentForMLLForm, NTPform
from drivingtest.models import Table3g, Duan

form = CommentForMLLForm()
print form.as_ul()
ttfi = form['trang_thai']
print '------'
print 'field',ttfi
print ttfi.label_tag()
