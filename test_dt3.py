# -*- coding: utf-8 -*- 
import os
import re







#from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from drivingtest.forms import CommentForMLLForm
from drivingtest.models import Table3g, Duan
'''
f = CommentForMLLForm (data={'comment':'ilove you','datetime':'21:14 02/11/2015'})
print f.is_valid()
print type(f.cleaned_data['datetime'])
'''
du_an_instance = Duan.objects.get(Name = 's')
print du_an_instance

