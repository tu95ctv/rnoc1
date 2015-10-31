# -*- coding: utf-8 -*-
from drivingtest.modelstest import CommentForMLLt
from django import forms
D4_DATETIME_FORMAT = '%H:%M %d/%m/%Y'
class Nform(forms.Form):
    a = forms.CharField()
class CommentForMLLFormt(forms.ModelForm):
    print 'outside','CommentForMLLForm(forms.ModelForm):'
    #comment = forms.CharField(help_text="add comment here1",widget=forms.Textarea(attrs={'autocomplete': 'off'}))
    datetime= forms.DateTimeField(input_formats =[D4_DATETIME_FORMAT], widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),help_text="leave blank if now",required=False)
    trang_thai = forms.CharField(label ="Trạng thái",widget=forms.TextInput(attrs={'class':'form-control autocomplete'}),required=False)
    doi_tac_fr = forms.CharField(label = "Đối Tác",widget=forms.TextInput(attrs={'class':'form-control autocomplete','style':'width:600px'}),required=False)
    is_delete = forms.BooleanField(required=False,label= "Xóa comment này")
    #gio_mat= forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M',required=False
    #doi_tac = forms.ModelChoiceField(queryset=Doitac.objects.all(),to_field_name="Full_name")
    #doi_tac = forms.ModelChoiceField(queryset=Doitac.objects.all(),initial = Doitac.objects.get(pk = 3).id)
    #https://docs.djangoproject.com/en/dev/ref/forms/widgets/#datetimeinput
    
    '''
    def clean(self):
        somefield = self.cleaned_data.get('comment')
        if not somefield:
            if not self._errors.has_key('comment'):
                from django.forms.util import ErrorList
                self._errors['somefield'] = ErrorList()
            self._errors['somefield'].append('Some field is blank')
    '''
    def __init__(self, *args, **kw):
        super(CommentForMLLFormt, self).__init__(*args, **kw)
        if 'instance' not in kw:
            
            self.fields.keyOrder = [
                'trang_thai',
                'doi_tac_fr',
                'comment',
                'datetime',
                
                ]
        else:
            self.fields.keyOrder = [
                'trang_thai',
                'doi_tac_fr',
                'comment',
                'datetime',
                'is_delete',
                ]
    class Meta:
        model = CommentForMLLt
        exclude = ('mll','thanh_vien','doi_tac','su_kien')
        
        widgets = {
            'comment': forms.Textarea(attrs={'autocomplete': 'off'}),
        }
        error_messages={
                        'comment':{'required': 'Please enter your name'}
                        } 