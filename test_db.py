import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')

from drivingtest.forms import Mllform

from django.db.models import CharField
from drivingtest.models import Ulnew , ForumTable, PostLog, Table3g,CommentForMLL,Mll
#print dict([(f.name,f.name) for f in Table3g._meta.fields if isinstance(f, CharField)])
'''
mll = Mll.objects.latest('id')
print mll.thiet_bi
c = CommentForMLL.objects.get_or_create(comment = "oktao noi nelen srosi")[0]
print c.comment
mll.comments.add(c)
mll = Mll.objects.get(id=1)
cms = ''
querysetcm = mll.comments.all()
for cm in querysetcm:
    cms = cms + cm.comment + '\n'
print cms
'''
mllform = Mllform()
print mllform.as_table
for field in mllform:
    print field.label