# -*- coding: utf-8 -*- 
import os
import re






#from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from drivingtest.models import Table3g
from drivingtest.formstest import Nform
instance = Table3g.objects.latest('id')
print instance

d = { u'T\xean BSC': 0,}
print d.pop(u'T\xean BSC')
print d
if u'Tên BSC' in d:
    print d[u'Tên BSC']
a = "abcdfdfd"
print a.startswith('abc')
t ="3G_adfd3G_fdfd"
cp_s=re.compile( r"(3(G))")

#kq = cp_s.sub('',t)
kq = cp_s.search(t)
kq_match= cp_s.match(t)
print kq.span()
print'kq_match',kq_match.span()

p = re.compile("x*")
kq = p.sub('-','abxd')
print kq

