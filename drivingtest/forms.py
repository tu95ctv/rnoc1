# -*- coding: utf-8 -*-
from django import forms
from drivingtest.models import Category, Linhkien,OwnContact, Table3g, Ulnew,\
    Mll, Command3g, SearchHistory, CommentForMLL
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import SplitDateTimeWidget
from crispy_forms.layout import Submit, Field
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings #or from my_project import settings
from django.forms.fields import DateTimeField
from time import strftime
from LearnDriving.settings import FORMAT_TIME
from datetime import timedelta

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
    
    
    class Meta:
        exclude = ("License_60W_Power", )
        model = Table3g
        sequence = ("selection","id","site_id_3g",)
        attrs = {"class": "tram-table table-bordered"}
class SearchHistoryTable(tables.Table):
    jquery_url= '/omckv2/search_history/'
    exclude = ('thanh_vien')
    edit_comlumn =  tables.Column(accessor="pk",)
    class Meta:
        model = SearchHistory
    def render_edit_comlumn(self,value):
        return mark_safe('''<img src='media/images/pencil.png' class='btnEdit'/>%s'''%value )   
class MllTable(tables.Table):
    edit_comlumn = tables.Column(accessor="pk", orderable=False)
    gio_mat = tables.DateTimeColumn(format="Y-m-d H:i")
    gio_tot = tables.DateTimeColumn(format="Y-m-d H:i")
    cac_buoc_xu_ly = tables.Column(accessor="pk")
    jquery_url = '/omckv2/mll_filter/'
    class Meta:
        model = Mll
        exclude=('gio_nhap','gio nhap')
        attrs = {"class": "table tablemll table-bordered"}
    def render_edit_comlumn(self,value):
        return mark_safe('''
        <div><button class="btn d4btn btn-default edit-mll-bnt" id= "%s" type="button">Edit</button></div></br>
        <div class="dropdown">
  <button class="btn btn-primary d4btn dropdown-toggle dropdown-class" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
    Function<span class="caret"></span>
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
    <li class="delete"><a href="#">Delele </a></li>
    <li><a href="#">nhan tin ung cuu</a></li>
    <li><a href="#">ung cuu tot</a></li>
    <li id="add-comment"><a href="#">Add Comment</a></li>
  </ul>
</div>''' %value)
    def render_cac_buoc_xu_ly(self,value):
        mll = Mll.objects.get(id=value)
        cms = '<ul class="comment-ul">' + '<li>' + mll.cac_buoc_xu_ly + '</li>'
        querysetcm = mll.comments.all().order_by("id")
        for comment in querysetcm:
            cms = cms + '<li><a href="#" comment-id="'+ str(comment.id) + '">'  +(comment.datetime + timedelta(hours=7, minutes=0)).strftime(FORMAT_TIME)+ '(' +  comment.thanh_vien + "): " + comment.comment + '</a></li>'
        cms = cms + '</ul>'
        return mark_safe(('%s' %cms ).replace('\n','</br>')) 
    #def render_gio_mat(self,value):
        #return value
class CommentForMLLForm(forms.ModelForm):
    class Meta:
        model = CommentForMLL   
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

class Table3gForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):

        super(Table3gForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
        TabHolder(
            Tab(
                      'thong tin 3G',
                      Div('site_id_3g',  'site_name_1', 'site_name_2','BSC','site_id_2g_E','BSC_2G' ,css_class= 'col-sm-3'),
                      Div(    'Status',  'Cabinet', 'Port', 'RNC','UPE','GHI_CHU' ,css_class= 'col-sm-3'),
                      Div( 'Count_Province', 'Count_RNC','Ngay_Phat_Song_3G', css_class= 'col-sm-3'),
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
            Tab(
                 'hide',
            )
                
        )
    )
    class Meta:
        model = Table3g
        
        
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
        
        
        
        #############################################333
        
        
class Mllform(forms.ModelForm):
    #thiet_bi = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    '''
    thiet_bi= forms.CharField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))
    site_name= forms.CharField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))
    loai_tu= forms.CharField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))
    nguyen_nhan = forms.CharField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))
    ung_cuu = forms.BooleanField()
    thanh_vien = forms.CharField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))
    ca_truc = forms.CharField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))
    #gio_nhap= forms.DateTimeField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))#3
    gio_mat= forms.DateTimeField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))#3
    gio_tot= forms.DateTimeField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))#3
    specific_problem =  forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'off',"class":'expand'}))
    
    doi_tac= forms.CharField(widget=forms.TextInput(attrs={'class':'input-filter1 expand-input1'}))
    
    cac_buoc_xu_ly =  forms.CharField(widget=forms.Textarea(attrs={'autocomplete':'off',"class":'expand'}))
    
    #gio_mat= forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M',required=False)#3
    #nguyen_nhan = forms.CharField(required=False,widget=forms.TextInput(attrs={'autocomplete':'off'}))
    '''
    '''
    def __init__(self,*args, **kwargs):
        super(Mllform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = settings.TEMPLATE_PATH +'/layout/inline_field.html'
        
        self.helper.layout = Layout(
        'thiet_bi',
        'gio_mat',
        'gio_tot',
        'nguyen_nhan',
        'cac_buoc_xu_ly',                         
        StrictButton('Luu Lai', css_class='btn-default'),
        )
        
        self.helper.form_id = 'mll-form'
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
        
        
