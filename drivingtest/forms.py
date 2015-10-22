# -*- coding: utf-8 -*-
from django import forms
from drivingtest.models import Category, Linhkien,OwnContact, Table3g, Ulnew,\
    Mll, Command3g, SearchHistory, CommentForMLL, Doitac, Nguyennhan, Catruc
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget
from crispy_forms.layout import Submit, Field
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings #or from my_project import settings
from django.forms.fields import DateTimeField
from time import strftime
#from LearnDriving.settings import FORMAT_TIME
from datetime import timedelta
from django.forms.models import ModelChoiceField
D4_DATETIME_FORMAT = '%H:%M %d/%m/%Y'
print 'D4_DATETIME_FORMAT',D4_DATETIME_FORMAT
TABLE_DATETIME_FORMAT = "H:i d/m/Y "
class PersonTable(tables.Table):
    #name = tables.Column(order_by=("title", "id"))
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
class TramTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    #site_id_3g = tables.Column(attrs={"th": {"class": "foo"},"td": {"class": "foo"}})
    #site_name_1 = tables.Column(attrs={"th": {"class": "foo"},"td": {"class": "foo"}})
    class Meta:
        exclude = ("License_60W_Power", )
        model = Table3g
        sequence = ("site_id_3g","site_name_1","selection","id",)
        attrs = {"class": "tram-table table-bordered"}
class SearchHistoryTable(tables.Table):
    jquery_url= '/omckv2/search_history/'
    exclude = ('thanh_vien')
    edit_comlumn =  tables.Column(accessor="pk",)
    class Meta:
        model = SearchHistory
        attrs = {"class": "table history-table table-bordered","table-action":"/omckv2/edit_history_search/"}
    def render_edit_comlumn(self,value):
        return mark_safe('''<img src='media/images/pencil.png' class='btnEdit'/><img src='media/images/delete.png' class='btnDelete'/>''' )
class DoitacTable(tables.Table):

    #selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    edit_comlumn = tables.Column(accessor="pk", orderable=False)
    jquery_url= '/omckv2/doitac_table_sort/'
    #pagination_bottom = True
    class Meta:
        model = Doitac
        #sequence = ("selection",)
        order_by = ('-id',)
        exclude = ('Full_name_khong_dau','First_name')
        attrs = {"class": "table doi_tac-table table-bordered","table-action":"/omckv2/edit_doi_tac_table_save"}
        template = "drivingtest/custom_table_template_top_pagination.html"
    def render_edit_comlumn(self,value):
        return mark_safe('''<img src='media/images/pencil.png' class='btnEdit' id="edit-%s"/>'''%value )
from django.utils import timezone
def doitac_showing (dt,is_show_donvi = False,prefix =''):
    if  dt:
        donvi = ('-' + dt.Don_vi ) if (dt.Don_vi and is_show_donvi) else ''
        sdt = ('-' + dt.So_dien_thoai) if dt.So_dien_thoai else ''
        htmlrender =  '<a href="#" class="edit-contact" id="%s">'%dt.id + prefix + dt.Full_name + donvi + sdt +'</a>'
        return mark_safe(htmlrender)
    else:
        return ''
   
class MllTable(tables.Table):
    edit_comlumn = tables.Column(accessor="pk", orderable=False,)
    gio_mat = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    gio_tot = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    doi_tac = tables.Column(accessor="doi_tac.Full_name",verbose_name="Doi tac")
    ca_truc = tables.Column(accessor="Catruc.Name",verbose_name="Ca Trực")
    cac_buoc_xu_ly = tables.Column(accessor="pk")
    nguyen_nhan = tables.Column(accessor='nguyen_nhan.Name',verbose_name="nguyên nhân")
    jquery_url = '/omckv2/mll_filter/'
    class Meta:
        model = Mll
        attrs = {"class": "table tablemll table-bordered paleblue"}#paleblue
        exclude=('gio_nhap','gio nhap')
    '''
    def render_doi_tac1(self,value,record):
        mll = Mll.objects.get(id=value)
        dt = mll.doi_tac
        return doitac_showing (dt,is_show_donvi=True)
    '''
    def render_doi_tac(self,value,record):
        mll = Mll.objects.get(id=record.id)
        dt = mll.doi_tac
        return doitac_showing (dt,is_show_donvi=True)
    def render_edit_comlumn(self,value):
        return mark_safe('''
        <div><button class="btn d4btn btn-default edit-mll-bnt" id= "%s" type="button">Edit</button></div></br>
        <div class="dropdown">
  <button class="btn btn-primary d4btn dropdown-toggle dropdown-class" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
    Function<span class="caret"></span>
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
    <li class="delete"><a href="#">Delele </a></li>
    <li><a href="#">Bao ung cuu</a></li>
    <li><a href="#">Nhap ung cuu tot</a></li>
    <li><a href="#">nhan tin ung cuu</a></li>
    <li><a href="#">nhan tin ung cuu tot</a></li>
    <li id="add-comment"><a href="#">Add Comment</a></li>
  </ul>
</div>''' %value)
        
        
    '''   
    def render_nguyen_nhan(self,value):
        return value
    '''
    def render_cac_buoc_xu_ly(self,value):
        mll = Mll.objects.get(id=value)
        cms = '<ul class="comment-ul">' + '<li>' + (timezone.localtime(mll.gio_mat)).strftime(D4_DATETIME_FORMAT)+ ' ' + mll.cac_buoc_xu_ly + '</li>'
        querysetcm = mll.comments.all().order_by("id")
        for comment in querysetcm:
            doi_tac_showing = doitac_showing (comment.doi_tac,prefix = " PH:",is_show_donvi=True)
            cms = cms + '<li><a href="#" class="edit-commnent" comment_id="'+ str(comment.id) + '"><span class="comment-time">'  +(timezone.localtime(comment.datetime)).strftime(D4_DATETIME_FORMAT)+ '</span>' + ' <span class="thanh-vien-comment">(' +  comment.thanh_vien + ")</span>: " +'<span class="comment">' + comment.comment + '</span>' + doi_tac_showing+ '</a></li>'
        cms = cms + '</ul>'
        return mark_safe(('%s' %cms ).replace('\n','</br>')) 
    #def render_gio_mat(self,value):
        #return value
class DoitacFormFull(forms.ModelForm):
    class Meta:
        
        model = Doitac
        exclude = ('Full_name_khong_dau','First_name',)
class DoitacForm(forms.ModelForm):
    class Meta:
        model = Doitac
        exclude = ('Full_name_khong_dau','First_name')
class CommentForMLLForm(forms.ModelForm):
    #comment = forms.CharField(help_text="add comment here1",widget=forms.Textarea(attrs={'autocomplete': 'off'}))
    datetime= forms.DateTimeField(input_formats =[D4_DATETIME_FORMAT], widget =forms.DateTimeInput(format='%H:%M %Y-%m-%d',attrs={'class': 'form-control'}),help_text="leave blank if now",required=False)
    #gio_mat= forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M',required=False
    doi_tac = forms.ModelChoiceField(queryset=Doitac.objects.all(),to_field_name="Full_name")
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
    class Meta:
        model = CommentForMLL
        exclude = ('mll','thanh_vien')
        
        widgets = {
            'comment': forms.Textarea(attrs={'autocomplete': 'off'}),
        }
        error_messages={
                        'comment':{'required': 'Please enter your name'}
                        } 
    '''def __init__(self, exp = None, *args, **kwargs):
        super(CommentForMLLForm, self).__init__(*args, **kwargs)
        self.fields['comment'].initial = "hello"  
        ''' 
class CommandTable(tables.Table):
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









##############FORM


        
        #############################################333
CHOICES=[('Moto','Moto'),('Huawei','Huawei'),('ALu','ALu'),('HCM','HCM')]# truoc la lable , sau la value tren hien thi
class  ConfigCaForm1(forms.Form):  
    ca_truc = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(),initial= 'Huawei')
class  ConfigCaForm(forms.Form):  
    ca_truc = forms.ModelChoiceField(queryset=Catruc.objects.all(),)   
class NTPform(forms.Form):
    ntpServerIpAddressPrimary= forms.CharField(required=False,initial = '10.213.227.98')
    ntpServerIpAddressSecondary= forms.CharField(required=False,initial = '10.213.227.98')
    ntpServerIpAddress1= forms.CharField(required=False,initial = '10.213.227.98')
    ntpServerIpAddress2= forms.CharField(required=False,initial = '10.213.227.98')
            
     
class Mllform(forms.ModelForm):
    gio_mat= forms.DateTimeField(input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format='%H:%M %Y-%m-%d',attrs={'class': 'form-control'}),help_text="leave blank if now",required=False)
    gio_bao_uc= forms.DateTimeField(input_formats = [D4_DATETIME_FORMAT],required=False)
    gio_tot= forms.DateTimeField(input_formats = [D4_DATETIME_FORMAT],required=False)
    #nguyen_nhan = forms.ModelChoiceField(queryset=Nguyennhan.objects.all())
    #def get_nguyen_nhan_name(self):
        #return Nguyennhan.objects.get(id=self.initial['nguyen_nhan']).Name
    '''
    def __init__(self, *args, **kwargs):
        super(Mllform, self).__init__(*args, **kwargs)
    '''
    class Meta:
        model = Mll
        exclude = ('comments','gio nhap')
        
class Commandform(forms.ModelForm):
    command = forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'off'}))
    ten_lenh = forms.CharField(required=False, widget=forms.Textarea(attrs={'autocomplete':'off'}))
    mo_ta = forms.CharField(required=False,widget=forms.Textarea(attrs={'autocomplete':'off'}))
    def __init__(self,*args, **kwargs):
        #extra = kwargs.pop('extra')
        super(Commandform, self).__init__(*args, **kwargs)
        #self.fields['nguyen_nhan'].label = u"Nguyên nhân"
        #self.helper = FormHelper()
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = settings.TEMPLATE_PATH +'/layout/inline_field.html'
        #submit = kwargs.pop('submit')
        '''
        self.helper.layout = Layout(
        'thiet_bi',
        'gio_mat',
        'gio_tot',
        'nguyen_nhan',
        'cac_buoc_xu_ly',                         
        StrictButton('Luu Lai', css_class='btn-default'),
        )
        '''
        
        self.helper.form_id = 'command-form'
        #self.helper.form_class = 'blueForms'
        #self.helper.form_method = 'post'
        #self.helper.form_action = 'luu_mll_form/'
        #if submit=='tao':
        self.helper.add_input(Submit('mll', 'Add Command'))
        self.helper.add_input(Submit('command-cancel', 'cc'))
        #elif submit=='sua':
            #self.helper.add_input(Submit('mll', 'sua'))
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Command3g
       
      
NTP_Field = ['ntpServerIpAddressPrimary','ntpServerIpAddress1','ntpServerIpAddress1','ntpServerIpAddress2']       

from django.db import models
class UpcappedModelField(models.Field):
    '''
    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        """
        Returns a django.forms.Field instance for this database Field.
        """
        defaults = {'required': not self.blank,
                    'label': self.verbose_name,
                    'help_text': self.help_text}
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()
        if self.choices:
            # Fields with choices get special treatment.
            include_blank = (self.blank or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)
            defaults['coerce'] = self.to_python
            if self.null:
                defaults['empty_value'] = None
            if choices_form_class is not None:
                form_class = choices_form_class
            else:
                form_class = forms.TypedChoiceField
            # Many of the subclass-specific formfield arguments (min_value,
            # max_value) don't apply for choice fields, so be sure to only pass
            # the values that TypedChoiceField will understand.
            for k in list(kwargs):
                if k not in ('coerce', 'empty_value', 'choices', 'required',
                             'widget', 'label', 'initial', 'help_text',
                             'error_messages', 'show_hidden_initial'):
                    del kwargs[k]
        defaults.update(kwargs)
        if form_class is None:
            form_class = forms.CharField
        return form_class(**defaults)
        '''
    def formfield(self, form_class=forms.CharField, **kwargs):
        return super(UpcappedModelField, self).formfield(form_class=forms.CharField, 
                         label=self.verbose_name, **kwargs)
W_VErsion = [('W12','W12'),('W11','W11')]
from django.utils.translation import ugettext_lazy as _
class Table3gForm_NTP_save(forms.ModelForm):
    #w_version =  forms.MultipleChoiceField(choices=W_VErsion, widget=forms.CheckboxSelectMultiple(),initial= 'W12',required=False) 
    
    
    class Meta:
        model = Table3g
        fields = ['ntpServerIpAddressPrimary' ,'ntpServerIpAddressSecondary',\
                         'ntpServerIpAddress1','ntpServerIpAddress2']
        help_texts = {
            'ntpServerIpAddress2': _('Update will update all site have same NTPconfig'),
        }
class Table3gForm(forms.ModelForm):
    #site_id_3g = UpcappedModelField()
    #site_id_3g = forms.CharField(label='abd')
    def __init__(self, *args, **kwargs):

        super(Table3gForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        #self.helper.form_id = 'thong_tin_tram_form'
        #self.helper.form_class = 'blueForms'
        #self.helper.form_method = 'post'
        #self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Edit'))
        self.helper.layout = Layout(
        TabHolder(
            Tab(
                      'thong tin 3G',
                      Div('site_id_3g',  'site_name_1', 'site_name_2','BSC','site_id_2g_E','BSC_2G' ,css_class= 'col-sm-3'),
                      Div(    'Status',  'Cabinet', 'Port', 'RNC','UPE','GHI_CHU' ,css_class= 'col-sm-3'),
                      Div( 'U900','License_60W_Power','Count_Province', 'Count_RNC','Ngay_Phat_Song_3G', css_class= 'col-sm-3'),
                      #Div(  'Cell_1_Site_remote', 'Cell_2_Site_remote', 'Cell_3_Site_remote','Cell_4_Site_remote', 'Cell_5_Site_remote','Cell_6_Site_remote','Cell_7_Site_remote', 'Cell_8_Site_remote', 'Cell_9_Site_remote', css_class= 'col-sm-3'),
                      HTML("""
            <p>
    <button class="btn btn-default download-script" type="button">Download Script</button>
</p>
        """)
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
                 'hide',
            )
                
        )
    )
    class Meta:
        model = Table3g
        
        exclude=['License_60W_Power']
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
























#TRANGPHUKIEN------------------------------------------

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    delete = forms.BooleanField(required=False,help_text="trong truong hop edit muon xoa")
    is_show_on_home_page = forms.BooleanField(initial=True,required=False)
    arrange_order_display = forms.IntegerField(required=False)
    cate_encode_url= forms.CharField(required=False)
    
    #is_parent_cate = forms.NullBooleanField(initial=False,required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
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
        # Provide an association between the ModelForm and a model
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
        # Provide an association between the ModelForm and a model
        model = Linhkien
        
        
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
class UploadFileForm(forms.Form):
    file = forms.FileField()
    is_parent_category = forms.BooleanField (required=False)
    


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset,HTML, Div, MultiField
from crispy_forms.bootstrap import TabHolder, Tab, StrictButton
class ExampleForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout =  Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'like_website',
                'favorite_number',
                'favorite_color',
                'favorite_food',
                'notes'
            ),
            )
        self.helper.form_id = 'id-exampleForm'
        #self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/abc/'
        #self.helper.form_tag = False
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper[1:2].wrap_together(Fieldset, "legend of the fieldset", css_class="fieldsets")        
        #self.helper[1:3].wrap_together(Fieldset, "legend of the fieldset", css_class="fieldsets")  

#ULLLLLLL---------------------------

class ForumChoiceForm(forms.Form):
    forumchoice = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Xin chon forum")
class UlnewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'tab1',
                'category',
                'title'
            ),
            Tab(
                'Address',
                'date',
                'rg',
                'city',
                'state',
                'country'
            ),
            Tab(
                'Contact',
                'email',
                'mobile',
                'home',
                'office',
                'twitter'
            )
        )
    )
 
    description= forms.CharField(widget=forms.Textarea(attrs={'class': 'special'}))
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Ulnew
        
        
