import os
from xu_ly_db_3g import read_line
from rnoc.models import Mll, Tram
from rnoc.forms import MllForm
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
'''
form = MllForm()
#print form.fields
print form.fields['nguyen_nhan'].label
print form['subject']

def get_model_fields(model):
    fields = {}
    options = model._meta
    for field in sorted(options.concrete_fields + options.many_to_many + options.virtual_fields):
        fields[field.name] = field
    return fields
fs = get_model_fields(Mll)
print fs['nguyen_nhan'].verbose_name
'''
'''
a = Mll(subject="abcd2",gio_mat = datetime.now(),ung_cuu=None)
a.save()
'''
ist= Tram(Site_Name_1='abcd1',TG='12a')
ist.save()
