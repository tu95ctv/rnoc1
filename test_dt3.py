import os
#from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
#from drivingtest.forms import Mllform
#from drivingtest.forms import CommentForMLLForm
#from drivingtest.models import Mll,CommentForMLL
'''
#mllinstance = Mll.objects.latest('id')
#print mllinstance
CommentForMLL_instance = CommentForMLL.objects.latest('id')
CommentForm = CommentForMLLForm(instance = CommentForMLL_instance)
print CommentForm.fields
print CommentForm['trang_thai']
print dir(CommentForm)
for f in CommentForm:
    print f
    '''