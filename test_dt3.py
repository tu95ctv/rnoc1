import os
from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from drivingtest.forms import Mllform
from drivingtest.models import Mll
#import django.forms.forms.BoundField
#import django.forms.models.ModelChoiceField
formi = Mllform(instance=Mll.objects.latest('id'))
data = {'subject':'abc'}
#print form
#form2 = Mllform(data)
#print form2.is_valid()
#print form2.cleaned_data
print formi['subject']==formi.fields['subject']
print formi.__dict__
print type(formi.fields['nguyen_nhan']),formi.fields['nguyen_nhan']
print type(formi['nguyen_nhan']),formi['nguyen_nhan'].value()

print formi.instance
#print formi.initial
print dir(formi['nguyen_nhan'])
print dir(formi.fields['nguyen_nhan'])
#print formi.fields['nguyen_nhan'].value
print formi['nguyen_nhan'].value()
print formi.fields
print dir(Mllform)
print dir(formi)
#a = [fname for fname, f in Mllform.fields.iteritems() if isinstance(f, ModelChoiceField)]
#print a
#print Mllform.fields
print formi.fields
print issubclass(Mllform, ModelForm)