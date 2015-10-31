import os






#from django.forms.models import ModelChoiceField, ModelForm

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from drivingtest.models import Table3g
from drivingtest.formstest import Nform
instance = Table3g.objects.latest('id')
print instance

