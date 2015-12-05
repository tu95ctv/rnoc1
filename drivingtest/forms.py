# -*- coding: utf-8 -*-
'print in form 4'
from django import forms
from drivingtest.models import Category, Linhkien,OwnContact, Table3g, Ulnew,\
    Mll, Command3g, SearchHistory, CommentForMLL, Doitac, Nguyennhan, Catruc,\
    TrangThaiCuaTram, UserProfile, Duan, SpecificProblem, FaultLibrary
from crispy_forms.layout import Submit, Field, Fieldset, MultiField
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import  format_html
from django.conf import settings #or from my_project import settings
from django.forms.fields import DateTimeField
from datetime import datetime
from django.core.exceptions import ValidationError
from toold4 import luu_doi_tac_toold4
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.utils.encoding import force_text
from django.forms.util import flatatt
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab
from django.template.context import Context
from django.template.loader import get_template
from django.forms.models import ModelMultipleChoiceField
import re
D4_DATETIME_FORMAT = '%H:%M %d/%m/%Y'
TABLE_DATETIME_FORMAT = "H:i d/m/Y "
######CONSTANT
CHOICES=[('Excel_3G','Ericsson 3G'),('Excel_to_2g','Database 2G'),\
         ('Excel_to_2g_config_SRAN','2G SRAN HCM Config'),\
         ('Excel_to_3g_location','3G Site Location'),('ALL','ALL'),\
         ('Excel_ALU','Excel_ALU'),('Excel_NSM','Excel_NSM'),
         ]
NTP_Field = ['ntpServerIpAddressPrimary','ntpServerIpAddress1','ntpServerIpAddress1','ntpServerIpAddress2']       
W_VErsion = [('W12','W12'),('W11','W11')]
#Function for omckv2
from django.utils import timezone
def doitac_showing (dt,is_show_donvi = False,prefix =''):
    if  dt:
        donvi = ('-' + dt.Don_vi ) if (dt.Don_vi and is_show_donvi) else ''
        sdt = ('-' + dt.So_dien_thoai) if dt.So_dien_thoai else ''
        htmlrender =  '<a href="#" class="edit-contact" id="%s">'%dt.id + prefix + dt.Full_name + donvi + sdt +'</a>'
        return mark_safe(htmlrender)
    else:
        return ''
#FIELD For OMCKV2
class DateTimeFieldWithBlankImplyNow(DateTimeField):
    def to_python(self, value):
        if value in self.empty_values:
            return datetime.now()
        else:
            rs = super(DateTimeFieldWithBlankImplyNow,self).to_python(value)
            return rs
class ChoiceFieldConvertBlank(forms.ModelChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            value = self.queryset.get(id = 1)
            return value
        else:
            value = super(ChoiceFieldConvertBlank,self).to_python(value)
        return value
       
class ChoiceFielddButWidgetTextInput(forms.CharField):
    default_error_messages = {
        'invalid_choice': _('Select a valid choice. %(value)s is not one of the available choices.'),
    }
    def __init__(self,queryset=None,to_python_if_leave_blank=None, *args, **kwargs):
        super(ChoiceFielddButWidgetTextInput,self).__init__( *args, **kwargs)
        self.queryset = queryset
        self.to_python_if_leave_blank = to_python_if_leave_blank
    def to_python(self, value):
        if value in self.empty_values:
            if self.to_python_if_leave_blank:
                value = self.queryset.get(**self.to_python_if_leave_blank)
                return value
            else:
                return None
        try:
            value = self.queryset.get(**{'Name': value})
            return value
        except (ValueError, self.queryset.model.DoesNotExist):
            raise ValidationError(self.error_messages['invalid_choice']%{'value':value})
    def prepare_value(self, value): # co chuc nang value cua widget
        if isinstance(value, int):
            value = self.queryset.get(id=value).Name
            return value
        else:
            return value
class TrangThaiField(ChoiceFielddButWidgetTextInput):
    default_error_messages = {
        'invalid_choice': _('khong co trang thai nao la "%(value)s" ca'),
        #'Select a valid choice. %(value)s is not one of the available choices.'
    }
class NguyenNhanField(ChoiceFielddButWidgetTextInput):
    default_error_messages = {
        'invalid_choice': _('Không có nguyên nhân nào là %(value)s  cả.'),
        #'Select a valid choice. %(value)s is not one of the available choices.'
    }     
class DuanField(ChoiceFielddButWidgetTextInput):
    pass
class DoiTacField(forms.CharField):
    def __init__(self,queryset=None, *args, **kwargs):
        super(DoiTacField,self).__init__( *args, **kwargs)
        self.queryset = queryset
    def prepare_value(self, value):# value for render as_widget
        if not value:
            return ''
        if isinstance(value, int):
            pass
        else:
            return value
        doi_tac = self.queryset.get(id=value)
        if doi_tac:
            doi_tac_return_to_form = doi_tac.Full_name  + (('-' + doi_tac.Don_vi ) if doi_tac.Don_vi else '') + (('-' + doi_tac.So_dien_thoai ) if doi_tac.So_dien_thoai else '')
        else:
            doi_tac_return_to_form=''
        return doi_tac_return_to_form
    def to_python(self, doi_tac_inputext):
        doi_tac_obj = luu_doi_tac_toold4(self.queryset,doi_tac_inputext)
        return doi_tac_obj
        #raise ValidationError(self.error_messages['invalid_choiced4'], code='invalid_choice')

#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFOOOOOOOOOOOOOOOOOOORMFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF       
class Commandform(forms.ModelForm):
    command = forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'off'}))
    ten_lenh = forms.CharField(required=False, widget=forms.Textarea(attrs={'autocomplete':'off'}))
    mo_ta = forms.CharField(required=False,widget=forms.Textarea(attrs={'autocomplete':'off'}))
    def __init__(self,*args, **kwargs):
        super(Commandform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = settings.TEMPLATE_PATH +'/layout/inline_field.html'
        self.helper.form_id = 'command-form'
        self.helper.add_input(Submit('mll', 'Add Command'))
        self.helper.add_input(Submit('command-cancel', 'cc'))
    class Meta:
        model = Command3g
class UploadFileForm(forms.Form):
    sheetchoice = forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple,label="Which Sheet you want import?",required=False)
    file = forms.FileField(label="Chon file database_3g excel",required=False)
    is_available_file = forms.BooleanField (required=False,label = "if available in media/document folder")
class DoitacFormFull(forms.ModelForm):
    class Meta:
        model = Doitac
        exclude = ('Full_name_khong_dau','First_name',)
class DoitacForm(forms.ModelForm):
    class Meta:
        model = Doitac
        exclude = ('Full_name_khong_dau','First_name')
class FaultLibraryForm(forms.ModelForm):
    def __init__(self,*args, **kw):
        super(FaultLibraryForm, self).__init__(*args, **kw)
        self.helper = FormHelper(form=self)
        self.helper.add_input(Submit('cf', 'EDIT Fault Code'))
    class Meta:
        model = FaultLibrary
        #exclude = ('mll',)
class SpecificProblemForm(forms.ModelForm):
    def __init__(self,*args, **kw):
        super(SpecificProblemForm, self).__init__(*args, **kw)
        self.helper = FormHelper(form=self)
        self.helper.add_input(Submit('cf', 'EDIT SPECIFIC PROBLEM'))
    class Meta:
        model = SpecificProblem
        exclude = ('mll',)
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        error_messages={'username':{'required': _('vui long nhap o nay!!')},}
class UserProfileForm(forms.ModelForm):
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_regex1 = RegexValidator(regex=r'\w{9,15}', message="Phone number must bat dau bang dau +")
    phone_regex2 = RegexValidator(regex=r'^\+', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    so_dien_thoai = forms.CharField(validators=[phone_regex1,phone_regex2]) # validators should be a list
    class Meta:
        model = UserProfile
        fields = ('so_dien_thoai',)
#$$$$$$$$$$$$$$$$$$MAINFORM
class CommentForMLLForm(forms.ModelForm):
    datetime= DateTimeFieldWithBlankImplyNow(input_formats =[D4_DATETIME_FORMAT], widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),help_text="leave blank if now",required=False)
    doi_tac = DoiTacField(queryset=Doitac.objects.all(),label = "Đối Tác",widget=forms.TextInput(attrs={'class':'form-control autocomplete','style':'width:600px'}),required=False)
    is_delete = forms.BooleanField(required=False,label= "Xóa comment này")
    trang_thai = ChoiceFieldConvertBlank(queryset=TrangThaiCuaTram.objects.all(),required = False,label = u'Trạng thái')
    #trang_thai = TrangThaiField(queryset=TrangThaiCuaTram.objects.all(),to_python_if_leave_blank={'id':1},label ="Trạng thái",widget=forms.TextInput(attrs={'class':'form-control autocomplete'}),required=False)
    def __init__(self,*args, **kw):
        
        #create_or_edit_form = kw.pop('create_or_edit_form')
        super(CommentForMLLForm, self).__init__(*args, **kw)
        self.helper = FormHelper(form=self)
        if 'instance' not in kw:
            self.fields.keyOrder = ['trang_thai','doi_tac','thao_tac_lien_quan','comment','datetime', ]
            self.helper.add_input(Submit('create-comment', u'Create Comment',css_class="btn btn-primary"))
        else:
            self.fields.keyOrder = ['trang_thai', 'doi_tac','thao_tac_lien_quan','comment','datetime','is_delete',]
            self.helper.add_input(Submit('create-comment', u'Edit',css_class="btn btn-warning"))
            
        
        self.helper.form_id = 'add-comment-form-id'
        self.helper.form_action = '/omckv2/add_comment/'
        self.helper.form_tag = False
        self.helper.layout = Layout(
Div(
     Div(AppendedText('datetime','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker-comment')),\
    Field('trang_thai',css_class='comboboxd4'),
    'thao_tac_lien_quan',
    'comment',
    'doi_tac',
    )
    class Meta:
        model = CommentForMLL
        exclude = ('mll','thanh_vien',)
        widgets = {
            'comment': forms.Textarea(attrs={'autocomplete': 'off'}),
        }
        '''
        labels = {
                'comment':u'Noi dung comment'
                 }
                 '''
        error_messages={
                        'comment':{'required': _('Please enter your name')}
                        } 
class  ConfigCaForm(forms.Form):  
    ca_truc = forms.ModelChoiceField(queryset=Catruc.objects.all(),)
GENDER_CHOICES = (
    ('male', _('Men')),
    ('female', _('Women')),
)
class ConfigCaFilterMLLTable(forms.ModelForm):
    #http://stackoverflow.com/questions/9993939/django-display-values-of-the-selected-multiple-choice-field-in-a-template
    #genders = forms.ModelChoiceField(queryset=Catruc.objects.all(),choices=GENDER_CHOICES,
    #ca_muon_show = forms.ModelChoiceField(queryset=Catruc.objects.all(),                                
    #widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        super(ConfigCaFilterMLLTable, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        self.helper.form_id = 'config_ca_filter_mll_table'
        self.helper.form_action = '/omckv2/config_ca_filter_mll_table/'
        self.helper.add_input(Submit('cf', 'submit'))
    class Meta:
        model = UserProfile
        fields = ('config_ca_filter_in_mll_table',)
        widgets= {'config_ca_filter_in_mll_table':forms.CheckboxSelectMultiple()}
class NTPform(forms.Form):
    ntpServerIpAddressPrimary= forms.CharField(required=False,initial = '10.213.227.98')
    ntpServerIpAddressSecondary= forms.CharField(required=False,initial = '10.213.227.98')
    ntpServerIpAddress1= forms.CharField(required=False,initial = '10.213.227.98')
    ntpServerIpAddress2= forms.CharField(required=False,initial = '10.213.227.98')
    
    
    #####                            #####
    #############            #############
                    #    #
                    #    #
                    # Mllform   #
                    #    #
class SubjecField(forms.CharField):
    def to_python(self,value):
        value = re.sub(',\s*$','',value)
        return super(SubjecField,self).to_python(value)
class Mllform(forms.ModelForm):
    subject = SubjecField(required=True)
    id =forms.CharField(required=False,widget=forms.HiddenInput(attrs={'hidden-input-name':'id-mll-entry'}))
    gio_mat= DateTimeFieldWithBlankImplyNow(input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),help_text=u"bỏ trống nếu là bây giờ",required=False)
    gio_mat_lon_hon= forms.DateTimeField(label =u'giờ mất sau thời điểm', input_formats = [D4_DATETIME_FORMAT],required=False,help_text=u"dùng để lọc lớn hơn")
    gio_tot= forms.DateTimeField(input_formats = [D4_DATETIME_FORMAT],required=False)
    datetime = DateTimeFieldWithBlankImplyNow(label = u'Giờ của trạng thái',input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),help_text=u"bỏ trống nếu là bây giờ",required=False)
    #specific_problem = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control autocomplete'}),required=False)
    #ca_truc = forms.CharField(required=False)
    #trang_thai = TrangThaiField(queryset=TrangThaiCuaTram.objects.all(),help_text=u'Bỏ trống = Raise Sự Kiện',label ="Trạng thái",widget=forms.TextInput(attrs={'class':'form-control autocomplete'}),required=False)
    trang_thai = ChoiceFieldConvertBlank(queryset=TrangThaiCuaTram.objects.all(),required = False,label = u'Trạng thái')
    #nguyen_nhan = NguyenNhanField(queryset=Nguyennhan.objects.all(),label =u'Nguyên nhân',widget=forms.TextInput(attrs={'class':'form-control autocomplete'}),required=False)
    #du_an = DuanField(queryset=Duan.objects.all(),label =u'Dự án',widget=forms.TextInput(attrs={'class':'form-control autocomplete'}),required=False)
    doi_tac = DoiTacField(queryset=Doitac.objects.all(),label = "Đối Tác",widget=forms.TextInput(attrs={'class':'form-control autocomplete'}),required=False)
    comment = forms.CharField(label = u'Comment:',widget=forms.Textarea(attrs={'class':'form-control autocomplete'}),required=False)
    specific_problem_m2m = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super(Mllform, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        self.helper.form_id = 'amll-form'
        self.helper.form_action = '/omckv2/luu_mll_form/'
        if 'instance'in kwargs:
            #is_edit = True
            #disible_karg ={'disable':'disable'}
            #self.helper.add_input(Submit('mll', 'Edit MLL initial',css_class="right-btn-first btn-warning"))
            self.helper.add_input(Submit('mll', 'Edit MLL initial',css_class="btn-warning mll-btn"))
        else:
            #is_edit = False
            #disible_karg ={'abc':'abc'}
            #self._meta.exclude =('gio_nhap','ca_truc','trang_thai')
            self.helper.add_input(Submit('mll', 'Tao MLL',css_class="mll-btn"))
            #self.helper.add_input(Submit('mll', 'Tao MLL',css_class="right-btn-first"))
        #self.helper.add_input(Submit('cancel', 'Cancle',css_class="d4btn btn btn-danger right-btn"))
        self.helper.add_input(Submit('cancel', 'Cancle',css_class="btn-danger"))
        self.helper.add_input(Submit('Filter', 'Filter',css_class="btn-info"))
        self.helper.layout = Layout(
TabHolder(
    Tab('Nhap Form MLL',Div('id',Field('subject',css_class="autocomplete_search_tram"), Field('nguyen_nhan',css_class= 'comboboxd4'),\
        Div(AppendedText('gio_mat','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'), Div(AppendedText('gio_tot','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'), css_class= 'col-sm-4'),
    Div(  'site_name',  'thiet_bi',Field('du_an',css_class= 'comboboxd4'),  'specific_problem_m2m', css_class= 'col-sm-4'),
    Div(HTML('<h4>Comment đầu tiên</h4>'),Div(AppendedText('datetime','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'),
        Field('trang_thai',css_class= 'comboboxd4'),Field('comment'),'doi_tac', css_class= 'col-sm-4 first-comment')
    ),
    Tab('Extra for filter', Div(Field('thanh_vien',css_class= 'comboboxd4'),'ca_truc',Div(AppendedText('gio_mat_lon_hon','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'),'ung_cuu','giao_ca',css_class= 'col-sm-6')),             
    Tab('Hide1',)   
            ) #Tab end
)#Layout end
    class Meta:
        model = Mll
        exclude = ('gio_nhap','specific_problem','specific_problem_m2m')
        widgets = {'specific_problem':forms.Textarea(attrs={'autocomplete':'off'}),
                  # 'trang_thai':forms.Textarea(attrs={'autocomplete':'off','class':'comboboxd4'}),
                   #'nguyen_nhan':forms.Textarea(attrs={'autocomplete':'off','class':'comboboxd4'}),
                   }
        '''
        labels = {
                'comment':u'Nội dung comment'
                 }
        '''
class Mllform_Without_first_comment(Mllform):
    class Meta:
        model = Mll
        exclude = ('gio_nhap','ca_truc','datetime','trang_thai','comment','doi_tac')
        widgets = {'specific_problem':forms.Textarea(attrs={'autocomplete':'off'}),
                  # 'trang_thai':forms.Textarea(attrs={'autocomplete':'off','class':'comboboxd4'}),
                   #'nguyen_nhan':forms.Textarea(attrs={'autocomplete':'off','class':'comboboxd4'}),
                   }
        '''
        labels = {
                'comment':u'Nội dung comment'
                 }
        '''
    
class Table3gForm_NTP_save(forms.ModelForm):
    send_mail = forms.EmailField(max_length=30,required = False)
    class Meta:
        model = Table3g
        fields = ['ntpServerIpAddressPrimary' ,'ntpServerIpAddressSecondary',\
                         'ntpServerIpAddress1','ntpServerIpAddress2']
        help_texts = {
            'ntpServerIpAddress2': _('Update will update all site have same NTPconfig'),
        }
class Table3gForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Table3gForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        self.helper.form_id = 'detail_tram'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/omckv2/edit_site/'
        #self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Edit',css_class="right-btn-first"))
        self.helper.layout = Layout(
        TabHolder(
            Tab(
                      'thong tin 3G',
                      Div('du_an_show','site_id_3g',  'site_name_1', 'site_name_2','BSC','site_ID_2G',css_class= 'col-sm-3'),
                      Div(  'ProjectE', 'Status', 'du_an', css_class= 'col-sm-3'),
                      Div( 'U900','License_60W_Power','Count_Province', 'Count_RNC','Ngay_Phat_Song_3G' , 'Port', css_class= 'col-sm-3'),
                      #Div(  'Cell_1_Site_remote', 'Cell_2_Site_remote', 'Cell_3_Site_remote','Cell_4_Site_remote', 'Cell_5_Site_remote','Cell_6_Site_remote','Cell_7_Site_remote', 'Cell_8_Site_remote', 'Cell_9_Site_remote', css_class= 'col-sm-3'),
                      Div('RNC' , 'Cabinet','UPE','GHI_CHU','BSC_2G', HTML("""<p><button class="btn btn-default download-script" type="button">Download Script</button></p>""") , css_class= 'col-sm-3')
                     
            ),
            Tab('Truyen Dan 3G',
                Div('Trans','IUB_VLAN_ID', 'IUB_SUBNET_PREFIX', 'IUB_DEFAULT_ROUTER',css_class= 'col-sm-3'),
                Div( 'IUB_HOST_IP', 'MUB_VLAN_ID',  'MUB_SUBNET_PREFIX', 'MUB_DEFAULT_ROUTER', 'MUB_HOST_IP',css_class= 'col-sm-3')
            ),             
            Tab('thong tin 2G',
              Div('BSC_2G', 'LAC_2G','site_ID_2G','Cell_ID_2G','Ngay_Phat_Song_2G',css_class= 'col-sm-3'),
              Div('cau_hinh_2G', 'nha_san_xuat_2G', 'TG', 'TRX_DEF',css_class= 'col-sm-3')
            ),
           
            Tab(
                 'thong tin tram', 'site_name_1', 'site_name_2','Ma_Tram_DHTT','Nha_Tram','dia_chi_2G', 'dia_chi_3G',
            ),
            Tab('NTP','ntpServerIpAddressPrimary','ntpServerIpAddressSecondary',\
    'ntpServerIpAddress1',\
    'ntpServerIpAddress2',css_class= 'col-sm-3'),
            Tab(
                 'hide',HTML('Hide')
            )
                
        )
    )
    class Meta:
        model = Table3g
        exclude=['License_60W_Power']
        help_texts = {'du_an':''}
######################################################################################################################################################
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                                                                                                     #
######################################################################################################################################################
#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE
from django_tables2_reports.tables import TableReport
#class SearchHistoryTable(TableReport):
class SearchHistoryTable(TableReport):
    jquery_url= '/omckv2/search_history/'
    exclude = ('thanh_vien')
    edit_comlumn =  tables.Column(accessor="pk",)
    class Meta:
        model = SearchHistory
        attrs = {"class": "table history-table table-bordered","table-action":"/omckv2/edit_history_search/"}
    def render_edit_comlumn(self,value):
        return mark_safe('''<img src='media/images/pencil.png' class='btnEdit'/><img src='media/images/delete.png' class='btnDelete'/>''' )
class DoitacTable(TableReport):
    edit_comlumn = tables.Column(accessor="pk", orderable=False)
    jquery_url= '/omckv2/doitac_table_sort/'
    class Meta:
        model = Doitac
        #sequence = ("selection",)
        order_by = ('-id',)
        exclude = ('Full_name_khong_dau','First_name')
        attrs = {"class": "table doi_tac-table table-bordered","table-action":"/omckv2/edit_doi_tac_table_save"}
        template = "drivingtest/custom_table_template_top_pagination.html"
    def render_edit_comlumn(self,value):
        return mark_safe('''<img src='media/images/pencil.png' class='btnEdit' id="edit-%s"/>'''%value )
class CommandTable(TableReport):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    edit_comlumn = tables.Column(accessor="pk", orderable=False)
    class Meta:
        model = Command3g
        sequence = ("selection",)
        attrs = {"class": "table cm-table table-bordered"}
    def render_edit_comlumn(self,value):
        return mark_safe('''
        <div><button class="btn btn-default edit-command-bnt" id= "%s" type="button">Edit Command </button></div>'''
         %value)
class TramTable(TableReport):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    jquery_url = '/omckv2/tram_table/'
    is_show_download_link = True
    class Meta:
        exclude = ("License_60W_Power", )
        model = Table3g
        sequence = ("site_id_3g","site_name_1","selection","id",)
        attrs = {"class": "tram-table table-bordered"}
'''
format_html('<option value="{0}"{1}>{2}</option>',
                           option_value,
                           selected_html,
                           force_text(option_label))
'''

class MllTable(TableReport):
    edit_comlumn = tables.Column(accessor="pk", orderable=False,)
    gio_tot = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    #last_update_time = tables.DateTimeColumn(format="H:i d-m")
    doi_tac = tables.Column(accessor="doi_tac.Full_name",verbose_name="Doi tac")
    ca_truc = tables.Column(accessor="ca_truc.Name",verbose_name="Ca Trực")
    trang_thai = tables.Column(accessor="trang_thai.Name",verbose_name="Trang Thai")
    cac_buoc_xu_ly = tables.Column(accessor="pk")
    specific_problem = tables.Column(accessor="pk")
    nguyen_nhan = tables.Column(accessor='nguyen_nhan.Name',verbose_name="nguyên nhân")
    jquery_url = '/omckv2/mll_filter/'
    gio_mat = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    class Meta:
        model = Mll
        attrs = {"class": "table tablemll table-bordered paleblue"}#paleblue
        exclude=('gio_nhap','gio_bao_uc','last_update_time','doi_tac')
        sequence = ('id','subject','site_name','thiet_bi','nguyen_nhan','du_an','ung_cuu','thanh_vien','ca_truc'\
                    ,'gio_mat','gio_tot','trang_thai','specific_problem','cac_buoc_xu_ly','edit_comlumn','giao_ca',)
    def render_specific_problem(self,value):
        mll = Mll.objects.get(id=value)
        sp_all =  mll.specific_problems.all()
        if not sp_all:
            return ''
        result = '<ul class="non-bullet-ul">'
        for x in sp_all:
            result = result + '<li>' + ( '<a  href="/omckv2/handelmodel/FaultLibraryForm/%s" class="green-color-text object-specific-problem">'%x.fault.id + ((x.fault.Name  + '</a>**' )) if x.fault else '')\
              + ( ('<a href="/omckv2/handelmodel/SpecificProblemForm/%s" class="object-specific-problem">'%x.id + x.object_name + '</a>') if x.object_name else '') + '</li>'
        result +='</ul>'
        result = mark_safe(result)
        return result
    def render_trang_thai(self,value):
        if value ==u"Báo ứng cứu":
            value = u'<span class="bao-ung-cuu">{0}</span>'.format(value)
        return mark_safe(value)
    def render_doi_tac(self,value,record):
        mll = Mll.objects.get(id=record.id)
        dt = mll.doi_tac
        return doitac_showing (dt,is_show_donvi=True)
    def render_cac_buoc_xu_ly(self,value):
        mll = Mll.objects.get(id=value)
        #cms = '<ul class="comment-ul">' + '<li>' + (timezone.localtime(mll.gio_mat)).strftime(D4_DATETIME_FORMAT)+ ' ' + mll.cac_buoc_xu_ly + '</li>'
        querysetcm = mll.comments.all().order_by("id")
        
        '''
        for count,comment in enumerate(querysetcm):
            doi_tac_showing = doitac_showing (comment.doi_tac,prefix = " PH:",is_show_donvi=True)
            cms = cms + '<li class ="comment-row-' +str(count%2)+ '"><a href="#" class="edit-commnent" comment_id="'+ str(comment.id) + '">\
            <span class="comment-time">'  +(timezone.localtime(comment.datetime)).strftime(D4_DATETIME_FORMAT)+ '</span>' \
            + ' <span class="thanh-vien-comment">(' +  comment.thanh_vien.username + "-" + \
            comment.trang_thai.Name+ " )</span>: " +'<span class="comment">' + comment.comment + '</span>' + doi_tac_showing+ '</a></li>'
        cms = cms + '</ul>'
        return mark_safe(('%s' %cms ).replace('\n','</br>')) 
        '''
        
        t = get_template('drivingtest/comment_in_mll_table_show.html')
        c = Context({ 'querysetcm': querysetcm })
        #rendered = t.render(c)
        return mark_safe(t.render(c))
        
    def render_edit_comlumn(self,value):
        return mark_safe('''
        <div><button class="btn d4btn btn-default edit-mll-bnt" id= "%s" type="button">Edit</button></div></br>
        <div class="dropdown ">
  <button class="btn btn-primary d4btn dropdown-toggle dropdown-class" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
    Function<span class="caret"></span>
  </button>
  <ul class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenu1">
    <li class="delete"><a href="#">Delele </a></li>
    <li><a href="#">Nhắn tin ứng cứu</a></li>
    <li id="add-comment" hanhdong="add-comment"><a href="#">Add Comment</a></li>
  </ul>
</div>''' %value)
        


            
            








#END TABLE###########END TABLE####################END TABLE#############END TABLE####END TABLE########END TABLE#######END TABLE#####
#UL
        
        









#TRANGPHUKIEN------------------------------------------

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    delete = forms.BooleanField(required=False,help_text="trong truong hop edit muon xoa")
    is_show_on_home_page = forms.BooleanField(initial=True,required=False)
    arrange_order_display = forms.IntegerField(required=False)
    cate_encode_url= forms.CharField(required=False)
    class Meta:
        model = Category
class OwnContactForm(forms.ModelForm):
    dia_chi= forms.CharField(widget=forms.Textarea)
    ten= forms.CharField(widget=forms.Textarea)
    email= forms.CharField(widget=forms.Textarea)
    sodienthoai= forms.CharField(widget=forms.Textarea) 
    google_map = forms.CharField(required=False,widget=forms.Textarea)
    slogan = forms.CharField(required=False,widget=forms.Textarea)
    about_us = forms.CharField(required=False,widget=forms.Textarea)
    banner_url = forms.URLField(required=False,)
    webpage= forms.CharField(required=False,)
    mainheader_color = forms.CharField(required=False,)
    mainheader_type = forms.CharField(required=False,)
    class Meta:
        model = OwnContact

class LinhkienForm(forms.ModelForm):
    delete = forms.BooleanField(required=False)
    name= forms.CharField(max_length=128,initial="abc")
    picture = forms.ImageField(help_text="Select a profile image to upload.",required=False,)
    icon_picture = forms.ImageField(help_text="upload icon picture here.",required=False)
    borrowed_icon_picture = forms.URLField(widget=forms.Textarea,required=False)
    borrowed_picture = forms.URLField(widget=forms.Textarea,required=False,initial="http://stcv4.hnammobile.com/uploads/accesories/details/4068823508_dan-cuong-luc-premium-ipad-air-2--0-25mm-.jpg")
    is_best_sale = forms.IntegerField(required=False)
    is_promote_sale = forms.IntegerField(required=False)
    arrange_order = forms.IntegerField(required=True)
    price = forms.IntegerField(initial="50")
    old_price = forms.IntegerField(initial="60",required=False)
    show_old_price = forms.BooleanField(initial=True,required=False)
    description = forms.CharField(max_length=8500,widget=forms.Textarea,initial="abc",required=False)
    pub_date = forms.DateTimeField(required=False)
    last_edited_date = forms.DateTimeField(required=False)
    class Meta:
        model = Linhkien


#ULLLLLLL---------------------------

class ForumChoiceForm(forms.Form):
    forumchoice = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Xin chon forum")
class UlnewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    description= forms.CharField(widget=forms.Textarea(attrs={'class': 'special'}))
    class Meta:
        model = Ulnew
        
#Table for UL
#PersonTable(tables.Table)
class PersonTable(TableReport):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    description = tables.Column(verbose_name="Mo ta")
    is_posted_shaanig = tables.Column(empty_values=())
    title = tables.Column()
    def render_is_posted_shaanig(self):
        return 'hk'
    def render_description(self,value):
        return value[:10]
    class Meta:
        model = Ulnew
        attrs = {"class": "paleblue"}
        sequence = ("selection", "date")
        
        
               
