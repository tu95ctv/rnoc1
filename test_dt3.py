# -*- coding: utf-8 -*- 
import os
import re
import sys
from django.utils.translation import ungettext







#from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')

from drivingtest.forms import CommentForMLLForm, NTPform
from drivingtest.models import Table3g, Duan,SpecificProblem
a= SpecificProblem(fault_name='DTRUfalt3',object_name='sector2')
a.save()
a= SpecificProblem(fault_name='DTRUfalt4',object_name='sector3')
a.save()
