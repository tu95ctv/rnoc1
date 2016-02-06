# -*- coding: utf-8 -*- 
import os
import re
import sys
from django.utils.translation import ungettext







#from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')

from drivingtest.models import Table3g, Duan,SpecificProblem, ThietBi,Doitac
print len(Doitac.objects.all())