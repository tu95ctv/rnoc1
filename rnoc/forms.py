# -*- coding: utf-8 -*-
'#print in form 4'
from django.utils import timezone
from unidecode import unidecode
from ckeditor.widgets import CKEditorWidget
from __builtin__ import str
#from django.utils.timezone import activate
'''
import os
from LearnDriving.settings import TIME_ZONE
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
'''
from django import forms
from models import SuCo,Tram,Mll, Lenh, SearchHistory, Comment, DoiTac, TrangThai, UserProfile, DuAn, SpecificProblem, FaultLibrary,ThietBi, EditHistory
from crispy_forms.layout import Submit, Field
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.utils.html import   strip_tags
from django.forms.fields import DateTimeField, FileField
from datetime import datetime
from django.core.exceptions import ValidationError
from toold4 import luu_doi_tac_toold4, prepare_value_for_specificProblem
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,HTML, Div
from crispy_forms.bootstrap import TabHolder, Tab
from django.template.context import Context, RequestContext
from django.template.loader import get_template
import re
from django_tables2_reports.tables import TableReport
from django.template.base import Template
from exceptions import IndexError, AttributeError
from django_tables2_reports.config import RequestConfigReport
from django.http.response import HttpResponse, StreamingHttpResponse
import xlwt
import collections
from django_tables2_reports.csv_to_xls.xlwt_converter import write_row
import csv
from rnoc.models import CaTruc, ThaoTacLienQuan, NguyenNhan, Tinh, BSCRNC,\
    SiteType, BCNOSS, UPE, BTSType
import random
from django.forms.util import ErrorList

HUONG_DAN = ''' <p>Tìm kiếm 1 field nào đó có chứa bất kỳ ký tự, nhập vào field đó *</p>
<p>Tìm kiếm 1 field nào đó KHÔNG chứa bất kỳ ký tự, nhập vào field đó ! </p>
 '''
D4_DATE_ONLY_FORMAT = '%d/%m/%Y'
D4_DATETIME_FORMAT = '%H:%M %d/%m/%Y'
D4_DATE_FORMAT_TABLE = 'd/m/Y'
TABLE_DATETIME_FORMAT = "H:i d/m/Y "
VERBOSE_CLASSNAME ={'NguyenNhan':u'Nguyên Nhân','ThietBi':u'Thiết Bị','TrangThai':u'Trạng Thái',\
                    'Tram':u'Trạm','Mll':u'Even or MLL','Comment':u'Comment','BCNOSS':u'Báo cáo ngày',\
                    'Lenh':u'Lệnh','UserProfile':u'Thông tin User','FaultLibrary':u'Thư viện lỗi','SpecificProblem':u'Specific Problem',\
                    'SearchHistory':u'Lịch sử user tìm kiếm','DuAn':u'Dự Án','SuCo':u'Sự Cố','ThaoTacLienQuan':u'Thao Tác Liên Quan',\
                    'CaTruc':u'Ca Trực','Tinh':u'Tỉnh','BSCRNC':u'BSCRNC','DoiTac':u'Đối Tác','UPE':u'UPE','Tram_NTP':u'Tram_NTP'} 
######CONSTANT
CHOICES=[('Excel_3G','Ericsson 3G'),('Excel_to_2g','Database 2G'),\
         ('Excel_to_2g_config_SRAN','2G SRAN HCM Config'),\
         ('Excel_to_3g_location','3G Site Location'),('ALL','ALL'),\
         ('Excel_ALU','Excel_ALU'),('Excel_NSM','Excel_NSM'),
         ]
NTP_Field = ['ntpServerIpAddressPrimary','ntpServerIpAddressSecondary','ntpServerIpAddress1','ntpServerIpAddress2']       
W_VErsion = [('W12','W12'),('W11','W11')]
#Function for omckv2
def DoiTac_showing (dt,is_show_donvi = False,prefix =''):
    if  dt:
        donvi = ('-' + dt.Don_vi ) if (dt.Don_vi and is_show_donvi) else ''
        sdt = ('-' + dt.So_dien_thoai) if dt.So_dien_thoai else ''
        htmlrender =  '<a href="#" class="edit-contact" id="%s">'%dt.id + prefix + dt.Name + donvi + sdt +'</a>'
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
            value = self.queryset.get(Name = u'Raise sự kiện')#
            return value
        else:
            value = super(ChoiceFieldConvertBlank,self).to_python(value)
        return value


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
            doi_tac_return_to_form = doi_tac.Name  + (('-' + doi_tac.Don_vi ) if doi_tac.Don_vi else '') + (('-' + doi_tac.So_dien_thoai ) if doi_tac.So_dien_thoai else '')
        else:
            doi_tac_return_to_form=''
        return doi_tac_return_to_form
    '''
    def to_python(self, doi_tac_inputext):
        doi_tac_obj = luu_doi_tac_toold4(self.queryset,doi_tac_inputext)
        return doi_tac_obj
    '''
        #raise ValidationError(self.error_messages['invalid_choiced4'], code='invalid_choice')
'''
class DoiTacFieldForFilterMLL(DoiTacField):
    def to_python(self, doi_tac_inputext):
        doi_tac_obj = luu_doi_tac_toold4(self.queryset,doi_tac_inputext,is_save_DoiTac_if_not_exit=False)
        return doi_tac_obj
'''
#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFOOOOOOOOOOOOOOOOOOORMFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF       


class UploadFileForm(forms.Form):
    sheetchoice = forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple,label="Which Sheet you want import?",required=True)
    file = forms.FileField(label="Chon file  excel",required=False)
    is_available_file = forms.BooleanField (required=False,label = "if available in media/document folder")
class ThongKeTable(TableReport):
    thang_nam = tables.Column(orderable = False)
    so_lan_mat_lien_lac = tables.Column(orderable = False)
    tong_thoi_gian_mat = tables.Column(orderable = False)
    thoi_gian_trung_binh_1_lan_mat = tables.Column(orderable = False)
    thoi_luong_mat_trung_binh_cua_1_tram_trong_thang = tables.Column(orderable = False)
    class Meta:
        #sequence = ("selection",'id','command','Name','thiet_bi','ghi_chu_lenh','edit_comlumn')
        attrs = {"class": "table-bordered"}
class BaseTableForManager(TableReport):
    is_report_download = True
    edit_comlumn = tables.Column(accessor="pk", orderable=False,)    
    def render_edit_comlumn(self,value):
        return mark_safe('<div><button class="btn  btn-default edit-entry-btn-on-table" id= "%s" type="button">Edit</button></div></br>'%value)
    def as_row_generator(self):
        csv_header = [column.header for column in self.columns]
        yield csv_header
        for row in self.rows:
            csv_row = []
            for column, cell in row.items():
                if isinstance(cell, basestring):
                    # if cell is not a string strip_tags(cell) get an
                    # error in django 1.6
                    cell = strip_tags(cell)
                else:
                    cell = unicode(cell)
                csv_row.append(cell)
            yield csv_row
    def as_xls_d4_in_form_py_csv(self, request):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in self.as_row_generator()),
                                         content_type="text/csv")
        file_name = self.Meta.model.__name__
        response['Content-Disposition'] = 'attachment; filename="Table_%s.csv"'%file_name
        return response
    def as_xls_d4_in_form_py_xls(self,request):
        response = HttpResponse()
        file_name = self.Meta.model.__name__
        response['Content-Disposition'] = 'attachment; filename="Table_%s.xls"'%file_name
        # Styles used in the spreadsheet.  Headings are bold.
        header_font = xlwt.Font()
        header_font.bold = True
        header_style = xlwt.XFStyle()
        header_style.font = header_font
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet 1')
        # Cell width information kept for every column, indexed by column number.
        cell_widths = collections.defaultdict(lambda: 0)
        csv_header = [column.header for column in self.columns if column.header!='Edit Comlumn']
        write_row(ws, 0, csv_header, cell_widths, style=header_style, encoding='utf-8')
        for lno,row in enumerate(self.rows):
            csv_row = []
            for column, cell in row.items():
                if column.header=='Edit Comlumn':
                    continue
                if isinstance(cell, basestring):
                    # if cell is not a string strip_tags(cell) get an
                    # error in django 1.6
                    cell = strip_tags(cell)
                else:
                    cell = unicode(cell)
                csv_row.append(cell)

            write_row(ws, lno+ 1, csv_row, cell_widths, style=None, encoding='utf-8')
        # Roughly autosize output column widths based on maximum column size.
        
        #for col, width in cell_widths.items():
            #ws.col(col).width = width
        setattr(response, 'content', '')
        wb.save(response)
        return response
class BaseFormForManager(forms.ModelForm):
    modal_add_title_style = 'background-color:#337ab7'
    design_common_button = True
    modal_edit_title_style = 'background-color:#5bc0de' 
    modal_prefix_title = "Detail"
    allow_edit_modal_form = True
    is_admin_set_update_edit_history = False
    def __init__(self,*args, **kw):
        self.loai_form = kw.pop('form_table_template',None)
        self.is_loc = kw.pop('loc',False)
        self.model_fnames = self.Meta.model._meta.get_all_field_names()
        force_allow_edit = kw.pop('force_allow_edit',False)
        self.request = kw.pop('request',None)
        self.khong_show_2_nut_cancel_va_loc = kw.pop('khong_show_2_nut_cancel_va_loc',None)
        #self.instance = kw.get('instance',None)
        #instance =  kw.get('instance',None)
        super(BaseFormForManager, self).__init__(*args, **kw)
        self.is_has_instance = bool(self.instance and self.instance.pk)
        self.Form_Class_Name = self.__class__.__name__
        if self.is_admin_set_update_edit_history:
            self.update_edit_history()
        
        if self.Form_Class_Name =='MllForm':
            if self.is_has_instance and not self.is_bound :
                #initial_autocomplete_para = {}
                #print 'prepare_value_for_specificProblem.__module__',prepare_value_for_specificProblem.__module__.__file__
                specific_problem_m2m_value = '\n'.join(map(prepare_value_for_specificProblem,self.instance.specific_problems.all()))
                self.initial.update({'specific_problem_m2m':specific_problem_m2m_value})
                autocomplete_attr = ('nguyen_nhan','du_an','su_co','thiet_bi','trang_thai')
                
                for x in autocomplete_attr:
                    attr = getattr(self.instance, x)
                    if attr!=None:
                        value_showed_inputtext = attr.Name
                    else:
                        value_showed_inputtext = ''
                    self.initial.update({x:value_showed_inputtext})
                    '''
                if instance.su_co:
                    su_co = instance.su_co.Name
                else:
                    su_co = ''
                if instance.du_an:
                    du_an = instance.du_an.Name
                else:
                    du_an = ''
                    '''
                #self.initial.update(**initial_autocomplete_para)
        elif self.Form_Class_Name =='CommentForm': 
                if not self.is_bound and not self.is_has_instance:
                        initial = {'mll':self.request.GET['selected_instance_mll']}
                        self.initial.update(initial)
                if self.is_has_instance:
                    if len(self.instance.thao_tac_lien_quan.all())>0:
                        display_text = ', '.join([item.Name for item in self.instance.thao_tac_lien_quan.all()])
                    else:
                        display_text = ''
                    self.initial.update({'thao_tac_lien_quan':display_text})
                    autocomplete_attr = ('trang_thai',)
                    for x in autocomplete_attr:
                        attr = getattr(self.instance, x)
                        if attr!=None:
                            value_showed_inputtext = attr.Name
                        else:
                            value_showed_inputtext = ''
                        self.initial.update({x:value_showed_inputtext})        
        if self.is_has_instance:
            if 'nguoi_tao' in self.model_fnames and 'nguoi_tao' in self.fields and  isinstance(self.fields['nguoi_tao'].widget,forms.TextInput):
                nguoi_tao = self.instance.nguoi_tao.username
                self.initial.update({'nguoi_tao':nguoi_tao})
            if 'nguoi_sua_cuoi_cung' in self.model_fnames and 'nguoi_sua_cuoi_cung' in self.fields  and isinstance(self.fields['nguoi_sua_cuoi_cung'].widget,forms.TextInput):
                nguoi_sua_cuoi_cung = self.instance.nguoi_sua_cuoi_cung.username if self.instance.nguoi_sua_cuoi_cung else ''
                self.initial.update({'nguoi_sua_cuoi_cung':nguoi_sua_cuoi_cung})
        if self.is_loc:
            self._validate_unique = False
        else:
            self._validate_unique = True
        self.helper = FormHelper(form=self)
        if self.design_common_button:
            if self.loai_form =='form on modal' and  self.allow_edit_modal_form or force_allow_edit or self.khong_show_2_nut_cancel_va_loc:
                self.helper.add_input(Submit('add-new', 'ADD NEW',css_class="submit-btn"))
            elif self.loai_form =='form on modal' and not self.allow_edit_modal_form:
                pass
            else: #loai_form =='normal form template' or None
                self.helper.add_input(Submit('add-new', 'ADD NEW',css_class="submit-btn"))
                self.helper.add_input(Submit('cancel', 'Cancel',css_class="btn-danger cancel-btn"))
                self.helper.add_input(Submit('manager-filter', 'Lọc',css_class="btn-info loc-btn"))
        self.helper.form_id = 'model-manager'
        #else: cai nay danh cho form NTPForm se co nhung nut rieng
    def update_edit_history(self):
        if self.is_has_instance:
            querysets = EditHistory.objects.filter(modal_name=self.Meta.model.__name__,edited_object_id = self.instance.id)
            table = EditHistoryTable(querysets)
            RequestConfigReport(self.request, paginate={"per_page": 10}).configure(table)
            t = Template('{% load render_table from django_tables2 %}{% render_table table "drivingtest/custom_table_template_mll.html" %}')
            c = RequestContext(self.request,{'table':table})
            self.htmltable = '<div style="clear:both;" id="edit-history-wrapper-div" class = "form-table-wrapper"><div class="table-manager">' + t.render(c)  + '</div></div>'
            self.htmltable = HTML(self.htmltable)
        else:
            self.htmltable=HTML('cai nay dung de luu lai lich su edit')
    def update_action_and_button(self,action_url):
        is_has_instance_for_button_showing = bool(self.instance and self.instance.pk)
        #self.helper.form_action = action_url
        self.helper.form_action = '/omckv2/modelmanager/'+self.Form_Class_Name +'/' + (str(self.instance.pk) if is_has_instance_for_button_showing else 'new')  + '/'
        
        #c = re.compile('/(\w+)/$')
        #entry_id = c.search(action_url).group(1)
        if self.helper.inputs:
            #if entry_id=='new':
            if not is_has_instance_for_button_showing:# only get, chua save
                try:
                    self.helper.inputs[0].value = "ADD NEW"
                    self.helper.inputs[0].field_classes = self.helper.inputs[0].field_classes.replace('btn-warning','btn-primary')
                except IndexError:
                    pass
                if self.loai_form =='form on modal':
                    self.modal_prefix_title="ADD"
                    self.modal_title_style = self.modal_add_title_style
            else:
                try:
                    self.helper.inputs[0].value = "EDIT"
                    self.helper.inputs[0].field_classes  = self.helper.inputs[0].field_classes.replace('btn-primary','btn-warning')
                except IndexError:
                    pass
                if self.loai_form =='form on modal':
                    self.modal_prefix_title="Detail"
                    self.modal_title_style = getattr(self,'modal_edit_title_style',None)
    
    
     
    
    def _post_clean(self):
        if self.is_loc or  self._errors :
            pass
        else:
            super(BaseFormForManager,self)._post_clean()
   
    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                e_code = getattr(e,'code',None)
                if self.is_loc and e_code=='required':
                    self.cleaned_data[name] = value
                    continue
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]# co san rua roi, copy thoi
    def clean(self):
        # thieu unique_valid
        if self.is_loc or  self._errors :
            pass
        else:
            errors= None
            model_fnames = self.model_fnames
            if self.instance and self.instance.pk:#if edit
                if not self.request.user.is_superuser:# lien quan den is_duoc_tao_truoc
                    try:
                        is_duoc_tao_truoc_attr_of_instance = getattr(self.instance,'is_duoc_tao_truoc')
                    except AttributeError:# Neu self.instance khong co is_duoc_tao_truoc attr
                        is_duoc_tao_truoc_attr_of_instance =None
                    if is_duoc_tao_truoc_attr_of_instance != None:
                        if 'is_duoc_tao_truoc' in self.fields:# xem xem nguoi dung co thay doi gia tri nay o tren form khong
                            value  = self.cleaned_data.get('is_duoc_tao_truoc')
                            if  value!=self.instance.is_duoc_tao_truoc:
                                msg = u'Bạn không được thay đổi field này'
                                #self.add_error('Name',msg)
                                errors = self._errors.setdefault("is_duoc_tao_truoc",ErrorList())
                                errors.append(msg)
                        if is_duoc_tao_truoc_attr_of_instance==True:
                            name_of_instance = self.instance.Name
                            if name_of_instance != self.cleaned_data['Name']:
                                msg = u'Bạn không được thay đổi field Name'
                                errors = self._errors.setdefault("Name",ErrorList())
                                errors.append(msg)
                
                if not errors:
                    exclude = getattr(self.Meta, 'exclude',[])
                    if 'ngay_gio_sua'in model_fnames:
                        if 'ngay_gio_sua' in exclude:
                            self.instance.ngay_gio_sua = datetime.now()
                        else:
                            self.cleaned_data['ngay_gio_sua'] = datetime.now()
                    if 'nguoi_sua_cuoi_cung'in model_fnames:
                        if 'nguoi_sua_cuoi_cung' in exclude:
                            self.instance.nguoi_sua_cuoi_cung = self.request.user
                        else:
                            self.cleaned_data['nguoi_sua_cuoi_cung'] = self.request.user
                            
                            
                    if 'ngay_gio_tao'in model_fnames:# thuc ra khogn can thiet cung duoc, dinh huong lai thoi
                        if 'ngay_gio_tao'  not in exclude:
                            self.cleaned_data['ngay_gio_tao'] = self.instance.ngay_gio_tao
                    if 'nguoi_tao'in model_fnames:
                        if 'nguoi_tao'  not in exclude:# Neu nguoi tao in exclude thi tot roi, neu no khong in ma thay doi lung tung thi phai dinh huong
                            self.cleaned_data['nguoi_tao'] = self.instance.nguoi_tao
                           
                    if 'ly_do_sua' in model_fnames :
                        if 'ly_do_sua' in exclude:
                            self.instance.ly_do_sua = self.request.GET['edit_reason']
                        else:
                            self.cleaned_data['ly_do_sua'] = self.request.GET['edit_reason']
            else: # if add new
                if not self.is_loc:
                    exclude = getattr(self.Meta, 'exclude',[])
                    #danh cho nhung field khong exclude
                    if 'ngay_gio_tao'in model_fnames:
                        if 'ngay_gio_tao' in exclude:
                        #Trong truong hop bi exclude field
                            self.instance.ngay_gio_tao = datetime.now()
                        else:
                            self.cleaned_data['ngay_gio_tao'] = datetime.now()
                    if 'nguoi_tao'in model_fnames:
                        if 'nguoi_tao' in exclude:
                            self.instance.nguoi_tao = self.request.user
                        else:
                            self.cleaned_data['nguoi_tao'] = self.request.user
                    
                    
                    if 'nguoi_sua_cuoi_cung' in model_fnames:
                        if 'nguoi_sua_cuoi_cung' in exclude:
                            self.instance.nguoi_sua_cuoi_cung = None
                        else:
                            self.cleaned_data['nguoi_sua_cuoi_cung'] = None
                    # vi ly do khong co clean_nguoi sua_cuoi_cung nen  trong post_clean phai them vao
                    if 'is_duoc_tao_truoc' in model_fnames and not self.request.user.is_superuser:#Neu add New thi field is_duoc_tao_truoc nay luon False
                        if 'is_duoc_tao_truoc' in exclude:
                            self.instance.is_duoc_tao_truoc = False
                        else:
                            self.cleaned_data['is_duoc_tao_truoc'] = False
                        
                    
            if 'Name_khong_dau' in model_fnames:
                self.instance.Name_khong_dau = unidecode(self.cleaned_data['Name'])   
        return self.cleaned_data
    
    def clean_nguoi_tao(self):# dung de loc
        nguoi_tao_string = self.cleaned_data['nguoi_tao']
        print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@nguoi_tao',nguoi_tao_string
        if self.is_loc:
            if isinstance(nguoi_tao_string,str):
                try:
                    instance = User.objects.get(Name = nguoi_tao_string)
                    return instance
                except User.DoesNotExist:
                    return None
        else:
            return nguoi_tao_string#de cho clean no lo
    def clean_nguoi_sua_cuoi_cung(self):
        value = self.cleaned_data['nguoi_sua_cuoi_cung']
        if self.is_loc:
            if isinstance(value,str):
                try:
                    instance = User.objects.get(Name = value)
                    return instance
                except User.DoesNotExist:
                    return None
        else:
            return value
      
    def clean_Name(self):
        value = self.cleaned_data['Name']
        if value:
            value = value.lstrip().rstrip()
            return value
        else:
            return ''
class NguyenNhanForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    def __init__(self, *args, **kwargs):
        super(NguyenNhanForm, self).__init__(*args, **kwargs)
        #self.helper[-5:].wrap_together(Field, css_class='col-sm-6')
        #self.helper[1:3].wrap(Fieldset, "legend of the fieldset")
        #self.helper[1:3].wrap(Fieldset, "legend of the fieldset", css_class="fieldsets")
        
        #self.helper.layout.append(HTML('ILOVE U'))
    class Meta:
        exclude = ('Name_khong_dau',)
        model = NguyenNhan
        widgets = { 'ghi_chu': forms.Textarea(attrs={'autocomplete': 'off'}),\
                'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),
            } 

class ThietBiForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    #ghi_chu_2 = forms.CharField(label=u"ghi_chu_2",widget=CKEditorWidget(),required =False)
    class Meta:
        model = ThietBi
        widgets = { 'ghi_chu': CKEditorWidget(),\
                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\
            } 
class LenhForm(BaseFormForManager):

    def __init__(self, *args, **kwargs):
        super(LenhForm, self).__init__(*args, **kwargs)
        self.helper.form_action='/omckv2/modelmanager/LenhForm/new/'
        self.helper.layout = Layout(Div(\
            Div('command',css_class='col-sm-6'),Div(Div('Name',css_class='col-sm-8'),Div('thiet_bi',css_class='col-sm-4'),Div('ghi_chu_lenh',css_class='col-sm-12'),css_class="col-sm-6")\
            ,css_class='row'))
        
    class Meta:
        model = Lenh
        widgets = {'command':forms.Textarea(attrs={'style':'height:300px;resize:vertical'}),'ghi_chu_lenh':CKEditorWidget(config_name = 'lenh_ckeditor')
                   }
        #exclude = ('ngay_gio_tao','ngay_gio_sua','nguoi_sua_cuoi_cung','nguoi_tao','ly_do_sua')
        exclude = ('Name_khong_dau',)
class DoiTacForm(BaseFormForManager):
    allow_edit_modal_form = True
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = DoiTac
        exclude = ('Name_khong_dau',)
        widgets = { 'ghi_chu':CKEditorWidget,
                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\
            } 
    

class CaTrucForm(BaseFormForManager):
    #is_allow_edit_name_field  = True
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = CaTruc
        widgets = { 'ghi_chu': CKEditorWidget(),\
                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\
            }
class TinhForm(BaseFormForManager):
    #is_allow_edit_name_field  = True
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = Tinh
        widgets = { 'ghi_chu': CKEditorWidget,\
                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\
            }   
        #exclude = ('is_duoc_tao_truoc',)
class UPEForm(BaseFormForManager):
    #is_allow_edit_name_field  = True
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    #ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    #nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = UPE
         
class BSCRNCForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = BSCRNC
        widgets = { 'ghi_chu': CKEditorWidget,\
                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\
            }   
        #exclude = ('is_duoc_tao_truoc',)
class TrangThaiForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = TrangThai
        widgets = { 'ghi_chu': CKEditorWidget,\
                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\
            }  
        exclude = ('Name_khong_dau','nguoi_tao','nga_gio_tao','nguoi_sua_cuoi_cung','ngay_gio_sua')
    def clean(self):
        super(TrangThaiForm,self).clean()
        if self.cleaned_data['color_code']=='':
            self.cleaned_data['color_code'] = "#%06x" % random.randint(0, 0xFFFFFF)
        return self.cleaned_data

class DuAnForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = DuAn
        exclude = ('is_duoc_tao_truoc','Name_khong_dau')
        widgets = { 'ghi_chu': CKEditorWidget,\
                    'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\

                   #'ngay_gio_tao':forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"disabled":"disabled"}) ,\
                   #'ngay_gio_sua':forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"disabled":"disabled"}) ,\
                    #'nguoi_tao':forms.TextInput(attrs={"disabled":"disabled"}),\
                    #'nguoi_sua_cuoi_cung':forms.TextInput(attrs={"disabled":"disabled"}),\
            }
    
    
class FaultLibraryForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = FaultLibrary
        widgets = { 'ghi_chu': CKEditorWidget,\
                   'ly_do_sua':forms.TextInput(attrs={"disabled":"disabled"}),\
     
            }
        exclude = ('Name_khong_dau',)
    
    
class ThaoTacLienQuanForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = ThaoTacLienQuan
        widgets = { 'ghi_chu': CKEditorWidget,\
                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\
        
            }
        exclude = ('Name_khong_dau',)
        
class SuCoForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    class Meta:
        model = SuCo
        widgets = { 'ghi_chu': CKEditorWidget,\

                   'ly_do_sua':forms.TextInput(attrs={"readonly":"readonly"}),\

            }
        exclude = ('Name_khong_dau',)

        # Disabled widget thi khong co key trong request.GET or POST

class SpecificProblemForm(BaseFormForManager):
    allow_edit_modal_form=True
    class Meta:
        model = SpecificProblem
        exclude = ('mll',)
class BCNOSSForm(BaseFormForManager):
    gio_mat= DateTimeFieldWithBlankImplyNow(help_text = u"now if leave blank",label=u"Giờ mất",input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),required=False)
    gio_tot= forms.DateTimeField(label=u"Giờ tốt",input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),required=False)
    gio_mat_lon_hon= forms.DateTimeField(label =u'Giờ mất sau thời điểm', input_formats = [D4_DATETIME_FORMAT],required=False,help_text=u"Dùng để lọc đối tượng có thời điểm mất sau thời điểm này")
    gio_canh_bao_ac= forms.DateTimeField(label=u"gio_canh_bao_ac",input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),required=False)
    #allow_edit_modal_form=True
    def clean(self):
        self.cleaned_data['tong_thoi_gian']  = int(round((self.cleaned_data['gio_tot'] - self.cleaned_data['gio_mat']).seconds/60)) if self.cleaned_data['gio_tot']  else None
        return self.cleaned_data
    def __init__(self, *args, **kwargs):
        super(BCNOSSForm, self).__init__(*args, **kwargs)
        self.helper.form_action='/omckv2/modelmanager/BCNOSSForm/new/'
        self.helper.layout = Layout(Div(\
            Div('object','code_loi','vnp_comment',Div(AppendedText('gio_canh_bao_ac','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker')\
                ,Div(AppendedText('gio_tot','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'),css_class='col-sm-3')\
            ,Div(Div(AppendedText('gio_mat','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker')\
                 ,Div(AppendedText('gio_mat_lon_hon','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'),Field('BSC_or_RNC',css_class= 'mySelect2'),Field('BTS_Type',css_class= 'mySelect2'),Field('BTS_thiet_bi',css_class= 'mySelect2'),css_class='col-sm-3'),css_class='row'))
    class Meta:
        model = BCNOSS
        #exclude = ('mll',)
        widgets = {'vnp_comment':forms.Textarea}
class  UserProfileForm(BaseFormForManager):  
    class Meta:
        model = UserProfile
CHOICES={'/omckv2/modelmanager/DoiTacForm/new/':u'Đối tác','/omckv2/modelmanager/ThietBiForm/new/':u'Thiết bị',\
             '/omckv2/modelmanager/DuAnForm/new/':u'Dự án',\
             '/omckv2/modelmanager/SuCoForm/new/':u'Sự cố',\
             '/omckv2/modelmanager/NguyenNhanForm/new/':u'Nguyên Nhân',\
             '/omckv2/modelmanager/FaultLibraryForm/new/':u'FaultLibraryForm',\
             '/omckv2/modelmanager/TrangThaiForm/new/':u'Trạng thái',\
             '/omckv2/modelmanager/SpecificProblemForm/new/':u'SpecificProblemForm',\
             '/omckv2/modelmanager/ThaoTacLienQuanForm/new/':u'Thao tác liên quan',\
             '/omckv2/modelmanager/UserProfileForm/new/':u'User Profile',
             '/omckv2/modelmanager/CaTrucForm/new/':u'Ca Trực',
             
             }
class  ModelManagerForm(forms.Form):  
    chon_loai_de_quan_ly = forms.ChoiceField(label = u'Chọn database để quản lý',required=False,widget = forms.Select(attrs={"class":"manager-form-select"}),\
    choices=[('/omckv2/modelmanager/DoiTacForm/new/',u'Đối tác'),('/omckv2/modelmanager/ThietBiForm/new/',u'Thiết bị'),\
             ('/omckv2/modelmanager/DuAnForm/new/',u'Dự án'),\
             ('/omckv2/modelmanager/SuCoForm/new/',u'Sự cố'),\
             ('/omckv2/modelmanager/NguyenNhanForm/new/',u'Nguyên Nhân'),\
             ('/omckv2/modelmanager/FaultLibraryForm/new/',u'FaultLibraryForm'),\
             ('/omckv2/modelmanager/TrangThaiForm/new/',u'Trạng thái'),\
             ('/omckv2/modelmanager/SpecificProblemForm/new/',u'SpecificProblemForm'),\
             ('/omckv2/modelmanager/ThaoTacLienQuanForm/new/',u'Thao tác liên quan'),\
             ('/omckv2/modelmanager/UserProfileForm/new/',u'User Profile'),
             ('/omckv2/modelmanager/CaTrucForm/new/',u'Ca Trực'),
             ('/omckv2/modelmanager/TinhForm/new/',u'Tỉnh'),
              ('/omckv2/modelmanager/UPEForm/new/',u'UPE'),
             ('/omckv2/modelmanager/BSCRNCForm/new/',u'BSC RNC'),
             ])
    def __init__(self, *args, **kwargs):
        super(ModelManagerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        #self.helper.layout = Layout(Div('chon_loai_de_quan_ly'))
        self.helper.form_tag = False

  
       
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        error_messages={'username':{'required': _('vui long nhap o nay!!')},}
class UserProfileForm_re(forms.ModelForm):
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_regex1 = RegexValidator(regex=r'^\+' , message="Phone number must bat dau bang dau +")
    phone_regex2 = RegexValidator(regex= r'\w{9,15}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    so_dien_thoai = forms.CharField(validators=[phone_regex1,phone_regex2]) # validators should be a list
    class Meta:
        model = UserProfile
        fields = ('so_dien_thoai',)
        
        
#$$$$$$$$$$$$$$$$$$MAINFORM
def update_trang_thai_cho_mll(mll_instance):
    last_comment_instance = mll_instance.comments.latest('id')
    mll_instance.trang_thai = last_comment_instance.trang_thai
    mll_instance.save()    
class CommentForm(BaseFormForManager):
    verbose_form_name  = 'Comment'
    modal_edit_title_style = 'background-color:#ec971f' 
    modal_add_title_style = 'background-color:#337ab7'
    allow_edit_modal_form=True
    datetime= DateTimeFieldWithBlankImplyNow(input_formats =[D4_DATETIME_FORMAT], widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),help_text="leave blank if now",required=False)
    doi_tac = DoiTacField(queryset=DoiTac.objects.all(),label = "Đối Tác",widget=forms.TextInput(attrs={'class':'form-control autocomplete'}),required=False)
    is_delete = forms.BooleanField(required=False,label= "Xóa comment này")
    #trang_thai = ChoiceFieldConvertBlank(queryset=TrangThai.objects.all(),required = False,label = u'Trạng thái')
    trang_thai = forms.CharField(label = u'Trạng Thái',required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    mll = forms.CharField(required=False,widget = forms.HiddenInput())
    thao_tac_lien_quan = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    nguoi_tao = forms.CharField(label=u"Người tạo",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    nguoi_sua_cuoi_cung = forms.CharField(label=u"Người sửa cuối cùng",widget=forms.TextInput(attrs={"readonly":"readonly"}),required =False)
    #comment = forms.CharField(required = False,max_length=2000,widget=CKEditorWidget())
    #mll = forms.CharField(required=False)
    def __init__(self,*args, **kw):
        self.mll = kw.pop('mll',None)
        super(CommentForm, self).__init__(*args, **kw)
        self.fields['thao_tac_lien_quan'].help_text=u'có thể chọn nhiều thao tác'
        para = [
     Div(AppendedText('datetime','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker-comment'),\
    'mll',
    AppendedText('trang_thai','<span style = "display:none" class="glyphicon glyphicon-plus"></span>'),
    'thao_tac_lien_quan',
    'comment',
    AppendedText('doi_tac','<span class="glyphicon glyphicon-plus"></span>'),

    ]
        if self.is_has_instance:
            para.extend(['is_delete','ngay_gio_tao',
    'nguoi_tao',
    'ngay_gio_sua','nguoi_sua_cuoi_cung'])
        self.helper.layout = Layout(*para)
    
    class Meta:
        model = Comment
        exclude = ('thanh_vien',)
        widgets = {
            'comment': forms.Textarea(attrs={'autocomplete': 'off'}),
        }

        error_messages={
                        'comment':{'required': _('Please enter your name')}
                        }
        help_texts = {'thao_tac_lien_quan':'','comment':'add some comments'}
    def clean_mll(self):
        if self.mll:
            return self.mll
        else:
            if not self.is_has_instance:
                return Mll.objects.get(id=self.request.POST['mll'])
            else:
                return self.instance.mll
        
    def clean_doi_tac(self):
        value = self.cleaned_data['doi_tac'].lstrip().rstrip()
        user_tao=self.request.user
        if value:
            if not self.is_loc:
                doi_tac_obj = luu_doi_tac_toold4(value,user_tao=user_tao,is_save_doitac_if_not_exit=True)
            else:
                doi_tac_obj = luu_doi_tac_toold4(value)
            return doi_tac_obj
        else:
            return None
    # neu dung mutiple thi bo cai ben duoi
    def clean_trang_thai(self): 
        value = self.cleaned_data['trang_thai'].lstrip().rstrip()
        if value:
            try:
                return_value = TrangThai.objects.get(Name = value)
            except TrangThai.DoesNotExist:
                if not self.is_loc:
                    return_value = TrangThai(Name=value,nguoi_tao = self.request.user)
                    return_value.save()
                else:
                    return_value = None
            return return_value
        else:
            return TrangThai.objects.get(Name = u'Raise sự kiện')
    def save(self,commit=True):
        super(CommentForm,self).save(commit = commit)
        if commit: # save mll_instance nhe!
            is_save_mll_instance = False
            mll_instance = self.cleaned_data['mll']
            if not self.is_has_instance:
                    is_this_instance_last_comment = True
            else:
                last_comment_instance = mll_instance.comments.latest('id')
                if self.instance == last_comment_instance:
                    is_this_instance_last_comment = True
                else:
                    is_this_instance_last_comment = False
            if self.cleaned_data['trang_thai'].is_cap_nhap_gio_tot:    
                mll_instance.gio_tot = self.instance.datetime
                is_save_mll_instance = True
            if self.cleaned_data['trang_thai'].Name==u'Báo ứng cứu':
                if mll_instance.ung_cuu != True:
                    mll_instance.ung_cuu = True
                    is_save_mll_instance = True
            if is_this_instance_last_comment:
                trang_thai_of_last_comment_instance = self.cleaned_data['trang_thai']
                if mll_instance.trang_thai != trang_thai_of_last_comment_instance:
                    mll_instance.trang_thai = trang_thai_of_last_comment_instance
                    is_save_mll_instance = True
            if is_save_mll_instance:
                mll_instance.save()
        return self.instance
    '''        
    def clean(self):
        super(CommentForm,self).clean()
        is_save_mll_instance = False
        mll_instance = self.cleaned_data['mll']
        if not self.is_has_instance:
                is_this_instance_last_comment = True
        else:
            last_comment_instance = mll_instance.comments.latest('id')
            if self.instance == last_comment_instance:
                is_this_instance_last_comment = True
        if self.cleaned_data['trang_thai'].is_cap_nhap_gio_tot:    
            mll_instance.gio_tot = self.instance.datetime
            is_save_mll_instance = True
        if self.cleaned_data['trang_thai'].Name==u'Báo ứng cứu':
            if mll_instance.ung_cuu != True:
                mll_instance.ung_cuu = True
                is_save_mll_instance = True
        if is_this_instance_last_comment:
            trang_thai_of_last_comment_instance = self.cleaned_data['trang_thai']
            if mll_instance.trang_thai != trang_thai_of_last_comment_instance:
                mll_instance.trang_thai = trang_thai_of_last_comment_instance
                is_save_mll_instance = True
        if is_save_mll_instance:
            mll_instance.save()
        return self.cleaned_data
    '''
    def clean_datetime(self):
        if self.is_has_instance:
            return self.instance.datetime
        else:
            return self.cleaned_data['datetime']
    def clean_thao_tac_lien_quan(self):
        value = self.cleaned_data['thao_tac_lien_quan'].lstrip().rstrip()
        if value:
            return_list = []
            itemlists =value.split(',')
            for item in itemlists:
                item  =item.lstrip()
                if not item:
                    continue
                try:
                    object_item = ThaoTacLienQuan.objects.get(Name = item )
                except:
                    if not self.is_loc:
                        object_item = ThaoTacLienQuan (Name = item,nguoi_tao = self.request.user)
                        object_item.save()
                    else:
                        continue
                return_list.append(object_item)
            return return_list
             
        else:
            return [] 

        
GENDER_CHOICES = (
    ('male', _('Men')),
    ('female', _('Women')),
)

'''
class SubjectField(forms.CharField):
    def to_python(self,value):
        value = re.sub(',\s*$','',value)
        return super(SubjectField,self).to_python(value)
'''
class MllForm(BaseFormForManager):
    #object = SubjectField(required=True)
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    #id =forms.CharField(required=False,widget=forms.HiddenInput(attrs={'hidden-input-name':'id-mll-entry'}))
    gio_mat= DateTimeFieldWithBlankImplyNow(label=u"Giờ mất",input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),help_text=u"Bỏ trống nếu là bây giờ",required=False)
    gio_mat_lon_hon= forms.DateTimeField(label =u'Giờ mất sau thời điểm', input_formats = [D4_DATETIME_FORMAT],required=False,help_text=u"Dùng để lọc đối tượng có thời điểm mất sau thời điểm này")
    gio_tot= forms.DateTimeField(label=u"Giờ tốt",input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),required=False)
    datetime = DateTimeFieldWithBlankImplyNow(label = u'Giờ của trạng thái',input_formats = [D4_DATETIME_FORMAT],widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={'class': 'form-control'}),help_text=u"Bỏ trống nếu là bây giờ",required=False)
    #trang_thai = ChoiceFieldConvertBlank(queryset=TrangThai.objects.all(),required = False,label = u'Trạng thái')
    doi_tac = DoiTacField(queryset=DoiTac.objects.all(),label = "Đối Tác",widget=forms.TextInput(attrs={'class':'autocomplete'}),required=False)
    nguyen_nhan = forms.CharField(label = u'Nguyên nhân',required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    su_co = forms.CharField(label = u'Sự cố',required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    thiet_bi = forms.CharField(label = u'Thiết bị',required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    trang_thai = forms.CharField(label = u'Trạng Thái',required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    du_an = forms.CharField(label = u'Dự án',required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    ung_cuu =  forms.NullBooleanField(label = u'Ứng cứu',initial='1',required=False)
    giao_ca = forms.NullBooleanField(label=u'Giao ca',initial='1',required=False)
    nghiem_trong = forms.NullBooleanField(label = u'Nghiêm trọng',initial='1',required=False)
    thao_tac_lien_quan = forms.CharField(label = u'Thao tác liên quan',help_text = u'Có thể chọn nhiều thao tác',required=False,widget=forms.TextInput(attrs={'class':'autocomplete'}))
    comment = forms.CharField(label = u'Comment:',widget=forms.Textarea(attrs={'class':'form-control'}),required=False)
    specific_problem_m2m = forms.CharField(label = u'Specific Problem',help_text=u'Input format: Mã lỗi**thành phần bị lỗi, hoặc: Mã lỗi** ,hoặc: Thành phần bị lỗi',required=False,widget=forms.Textarea(attrs={'class':'form-control autocomplete','style':"height:120px"}))
    #specific_problem_m2m = forms.CharField(label = u'Specific Problem',help_text=u'Input format: Mã lỗi**thành phần bị lỗi, hoặc: Mã lỗi** ,hoặc: Thành phần bị lỗi',required=False,widget=CKEditorWidget(attrs={'class':'form-control autocomplete'}))
    is_admin_set_update_edit_history = True
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ly_do_sua  = forms.CharField(required=False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    is_delete = forms.BooleanField(required=False,label= "Xóa MLL này")
    def __init__(self, *args, **kwargs):
        super(MllForm, self).__init__(*args, **kwargs)
        #self.fields['thao_tac_lien_quan'].help_text=u''
        self.helper.form_action='/omckv2/modelmanager/MllForm/new/'
        para = [Field('nguoi_tao',css_class= 'mySelect2'),'ca_truc',Div(AppendedText('gio_mat_lon_hon','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker')]
        if self.is_has_instance:
            para.extend(['is_delete'])
        self.helper.layout = Layout(
#27thang 2 change comboboxd4 to mySelect2
#neu dung select 2Field('su_co',css_class= 'mySelect2')
#,'specific_problem_m2m'
TabHolder(
    Tab('Nhap Form MLL',\
    
    Div(Div(Field('object',css_class="autocomplete_search_tram"), \
        AppendedText('su_co','<span href= "/omckv2/modelmanager/SuCoForm/New/" style = "display:none" class="glyphicon glyphicon-plus"></span>'),AppendedText('nguyen_nhan','<span style = "display:none" class="glyphicon glyphicon-plus"></span>'),\
        Div(AppendedText('gio_mat','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'),\
        Div(AppendedText('gio_tot','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'),'id', css_class= 'col-sm-6'),
    Div('site_name',  AppendedText('thiet_bi','<span style = "display:none" class="glyphicon glyphicon-plus"></span>'),AppendedText('du_an','<span style = "display:none" class="glyphicon glyphicon-plus"></span>'),'giao_ca','ung_cuu','nghiem_trong', css_class= 'col-sm-6')
    ,Div('specific_problem_m2m',HTML('<button type="button" id="replace-carrier-return" style="float:right;background:green;">Replace CR</button>'),css_class="col-sm-12")
    ,css_class = "col-sm-8"),
    
    Div(HTML('<h4>Comment đầu tiên</h4>'),Div(AppendedText('datetime','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker'),
        AppendedText('trang_thai','<span style = "display:none" class="glyphicon glyphicon-plus"></span>'),AppendedText('thao_tac_lien_quan','<span style = "display:none" class="glyphicon glyphicon-plus"></span>'),'comment',AppendedText('doi_tac','<span class="glyphicon glyphicon-plus"></span>'), css_class= 'col-sm-4 first-comment')
    
    ),
    
    
    
    Tab('Extra for filter', Div(*para,css_class= 'col-sm-6')),             
       Tab('Hide form trực ca',)  
       ,
    Tab('Edit History mllform','ngay_gio_tao','ngay_gio_sua','nguoi_sua_cuoi_cung','ly_do_sua',self.htmltable )
             
            ) #Tab end
)#Layout end
    class Meta:
        model = Mll
        exclude = ('gio_nhap','last_update_time')#,'thanh_vien'
    
    def save(self,commit=True):
        #print '@@@@@@@@@@@@nguyen duc tu@@@@@@@@@@@'
        super(MllForm,self).save(commit=True)
        #print '@@@@@@@@@@@@@@commit',commit
        if commit ==True:
            #print 'okkkkkkkkkkkkkkkkkkkk2'
            self.save_specific_problem_m2m()
            if not self.is_has_instance:
                CommentForm_i = CommentForm(self.request.POST,request = self.request,mll =self.instance)
                #if CommentForm_i.is_valid():
                CommentForm_i.save()
                #first_comment.nguoi_tao = user
                #first_comment.mll = mll_instance
                #first_comment.save()
                #CommentForm_i.save_m2m()
        return self.instance
    def clean_ca_truc(self):
        if not self.is_loc:
            if not self.is_has_instance:
                return self.request.user.get_profile().ca_truc
            else:
                return self.instance.ca_truc
        else:
            return self.cleaned_data['ca_truc']
    def clean(self):
        if self._errors:
            #print '@@@@@@@@@@@ da co loi roi ma cung vao clean nghia la sao'
            return self.cleaned_data
            #print '@@@@@@@@@@@ da co loi roi ma cung vao clean nghia la sao 2'
           
        return super(MllForm,self).clean()
    def save_specific_problem_m2m(self):
        if self.cleaned_data['specific_problem_m2m'] !='':
                specific_problem_m2ms = self.cleaned_data['specific_problem_m2m'].split('\n')
                for count,specific_problem_m2m in enumerate(specific_problem_m2ms):
                    if '**' in specific_problem_m2m:
                        faulcode_hyphen_objects = specific_problem_m2m.split('**')
                        try:
                            faultLibrary_instance = FaultLibrary.objects.get(Name = faulcode_hyphen_objects[0])
                        except :
                            faultLibrary_instance = FaultLibrary(Name = faulcode_hyphen_objects[0])
                            faultLibrary_instance.ngay_gio_tao = datetime.now()
                            faultLibrary_instance.nguoi_tao = self.request.user
                            faultLibrary_instance.save()
                        if len(faulcode_hyphen_objects) > 1:
                            object_name = faulcode_hyphen_objects[1]
                        else:
                            object_name=None
                    else:
                        faultLibrary_instance = None
                        object_name = specific_problem_m2m
                    if not self.is_has_instance:
                        SpecificProblem.objects.create(fault = faultLibrary_instance, object_name = object_name,mll=self.instance)
                    else:#ghi chong len nhung entry problem specific dang co
                        specific_problem_queryset_from_db_s = self.instance.specific_problems.all()
                        try:
                            specific_problem = specific_problem_queryset_from_db_s[count]
                            specific_problem.fault = faultLibrary_instance
                            specific_problem.object_name = object_name
                            specific_problem.save()
                        except IndexError: # neu thieu instance hien tai so voi nhung instance sap duoc ghi thi tao moi 
                            SpecificProblem.objects.create(fault = faultLibrary_instance, object_name = object_name,mll=self.instance)
                        # delete nhung cai specific_problems khong duoc ghi chong
                        if (len(specific_problem_queryset_from_db_s) > count): 
                            for x in specific_problem_queryset_from_db_s[count+1:]:
                                x.delete()    
    def clean_object(self):
        value = self.cleaned_data['object']
        if value:
            value = re.sub(',*\s*$','',value)
        return value
    def clean_ung_cuu(self):
        value = self.cleaned_data['ung_cuu']
        if not self.is_loc and value==None:
            return False
        else:
            return value
    def clean_giao_ca(self):
        value = self.cleaned_data['giao_ca']
        if not self.is_loc and value==None:
            return False
        else:
            return value
    def clean_nghiem_trong(self):
        value = self.cleaned_data['nghiem_trong']
        if not self.is_loc and value==None:
            return False
        else:
            return value
    def clean_nguyen_nhan(self): 
        value = self.cleaned_data['nguyen_nhan'].lstrip().rstrip()
        if value:
            try:
                return_value = NguyenNhan.objects.get(Name = value)
            except NguyenNhan.DoesNotExist:
                if not self.is_loc:
                    return_value = NguyenNhan(Name=value,nguoi_tao = self.request.user)
                    return_value.save()
                else:
                    return_value = None
            return return_value
        else:
            return None
    def clean_su_co(self): 
        value = self.cleaned_data['su_co'].lstrip().rstrip()
        if value:
            try:
                return_value = SuCo.objects.get(Name = value)
            except SuCo.DoesNotExist:
                if not self.is_loc:
                    return_value = SuCo(Name=value,nguoi_tao = self.request.user)
                    return_value.save()
                else:
                    return_value = None
            return return_value
        else:
            return None
    '''
    def clean_thiet_bi(self): 
        value = self.cleaned_data['thiet_bi'].lstrip().rstrip()
        if value:
            try:
                return_value = ThietBi.objects.get(Name = value)
            except ThietBi.DoesNotExist:
                if not self.is_loc:
                    return_value = ThietBi(Name=value,nguoi_tao = self.request.user)
                    return_value.save()
                else:
                    return_value = None
            return return_value
        else:
            return None
    '''
    def clean_thiet_bi(self):
        query = self.cleaned_data['thiet_bi'].lstrip().rstrip()
        if query:
            if '*' not in query:
                thietbi_name = query
                bts_type_name = None
            else:
                gach_index = query.find('*')
                thietbi_name = query[:gach_index].lstrip().rstrip()
                bts_type_name = query[gach_index+1:].lstrip().rstrip()
                if bts_type_name:
                    try:
                        bts_type = BTSType.objects.get(Name =bts_type_name )
                    except:
                        bts_type = None
            try:
                karg = {'Name':thietbi_name}
                if bts_type:
                    karg.update({'bts_type':bts_type})
                return_value = ThietBi.objects.filter(**karg)[0]
            except IndexError:
                if not self.is_loc:
                    return_value = ThietBi(Name = thietbi_name,bts_type = bts_type)
                    return_value.save()
                else:
                    return_value = None
                
            return return_value    
        else:
            return None
    def clean_trang_thai(self): 
        value = self.cleaned_data['trang_thai'].lstrip().rstrip()
        if value:
            try:
                if not self.is_has_instance:
                    return_value = TrangThai.objects.get(Name = value)
                else:
                    #return_value = self.instance.comments.latest('id')
                    last_comment_instance = self.instance.comments.latest('id')
                    return_value = last_comment_instance.trang_thai
            except TrangThai.DoesNotExist:
                if not self.is_loc:
                    return_value = TrangThai(Name=value,nguoi_tao = self.request.user)
                    return_value.save()
                    
                else:
                    return_value = None
            return return_value
        else:
            return TrangThai.objects.get(Name = u'Raise sự kiện')
    def clean_du_an(self): 
        value = self.cleaned_data['du_an'].lstrip().rstrip()
        if value:
            try:
                return_value = DuAn.objects.get(Name = value)
            except DuAn.DoesNotExist:
                if not self.is_loc:
                    return_value = DuAn(Name=value,nguoi_tao = self.request.user)
                    return_value.save()
                else:
                    return_value = None
            return return_value
        else:
            return None    
    def clean_thao_tac_lien_quan(self):
        value = self.cleaned_data['thao_tac_lien_quan'].lstrip().rstrip()
        if value:
            return_list = []
            itemlists =value.split(',')
            for item in itemlists:
                item  =item.lstrip()
                if not item:
                    continue
                try:
                    object_item = ThaoTacLienQuan.objects.get(Name = item )
                except:
                    if not self.is_loc:
                        object_item = ThaoTacLienQuan (Name = item,nguoi_tao = self.request.user)
                        object_item.save()
                    else:
                        continue
                return_list.append(object_item)
            return return_list
             
        else:
            return []
    def clean_doi_tac(self):
        value = self.cleaned_data['doi_tac']# khogn can .lstrip().rstrip() vi o luu_doi_tac_toold4 co roi
        if value:
            if not self.is_loc:
                user_tao=self.request.user
                doi_tac_obj = luu_doi_tac_toold4(value,user_tao=user_tao,is_save_doitac_if_not_exit=True)
            else:
                doi_tac_obj = luu_doi_tac_toold4(value)
            return doi_tac_obj
        else:
            return None         
    
       
class Tram_NTPForm(BaseFormForManager):
    ntpServerIpAddressPrimary= forms.CharField(required=True)
    ntpServerIpAddressSecondary= forms.CharField(required=False)
    ntpServerIpAddress1= forms.CharField(required=True)
    ntpServerIpAddress2= forms.CharField(required=False)
    design_common_button = False
    allow_edit_modal_form = False
    def __init__(self, *args, **kwargs):
        super(Tram_NTPForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('add-new', 'ADD NEW',css_class="edit-ntp submit-ntp submit-btn"))
        self.helper.add_input(Submit('first-argument', 'Update to db',css_class="submit-btn update_all_same_vlan_sites"))
        self.helper.add_input(Submit('download-script-first-argument', 'download-script',css_class="btn btn-success link_to_download_scipt"))
    
    def save(self,commit = True):
        super(Tram_NTPForm,self).save(commit=commit)
        if (self.request.GET.get('update_all_same_vlan_sites',None)=='yes') and commit:
                rnc = self.instance.RNC
                IUB_VLAN_ID = self.instance.IUB_VLAN_ID
                same_sites = Tram.objects.filter(RNC=rnc,IUB_VLAN_ID=IUB_VLAN_ID)
                same_sites.update(**dict([(fn,self.request.POST[fn])for fn in NTP_Field]))
                    
        return self.instance
    class Meta:
        model = Tram
        fields = ['ntpServerIpAddressPrimary' ,'ntpServerIpAddressSecondary',\
                         'ntpServerIpAddress1','ntpServerIpAddress2']
        help_texts = {
            'ntpServerIpAddress2': _('Update will update all site have same NTPconfig'),
        }
        
    '''
    def clean(self):
        super(Tram_NTPForm,self).clean()
        return self.cleaned_data
    '''
class NhanTinUngCuuForm(forms.Form):
    noi_dung_tin_nhan = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control'}))
    group = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    def __init__(self, *args, **kwargs):
        super(NhanTinUngCuuForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(form=self)
        self.helper.add_input(Submit('copy tin nhan', 'Copy Tin Nhan',css_class="submit-btn"))   
class TramForm(BaseFormForManager):
    id =forms.CharField(required =  False,widget = forms.TextInput(attrs={"readonly":"readonly"}))
    is_co_U900_rieng = forms.NullBooleanField(initial='1',required=False,label = u'Site 3G có Site U900 riêng')
    is_co_U2100_rieng = forms.NullBooleanField(initial='1',required=False,label = u'Site 3G có Site U2100 riêng')
    active_3G = forms.NullBooleanField(initial='1',required=False,label = u"Đang Active 3G",)
    active_2G = forms.NullBooleanField(initial='1',required=False,label = u"Đang Active 2G",)
    active_4G = forms.NullBooleanField(initial='1',required=False,label = u"Đang Active 4G",)
    Ngay_Phat_Song_3G =forms.DateTimeField(label=u"Ngày Phát sóng 3G",input_formats = [D4_DATE_ONLY_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATE_ONLY_FORMAT))
    Ngay_Phat_Song_3G_lon_hon =forms.DateTimeField(help_text = u'Field này dùng để lọc',label=u"Ngày Phát sóng 3G Lớn hơn",input_formats = [D4_DATE_ONLY_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATE_ONLY_FORMAT))
    
    Ngay_Phat_Song_2G =forms.DateTimeField(label=u"Ngày Phát sóng 2G",input_formats = [D4_DATE_ONLY_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATE_ONLY_FORMAT))
    Ngay_Phat_Song_2G_lon_hon =forms.DateTimeField(help_text = u'Field này dùng để lọc',label=u"Ngày Phát sóng 2G Lớn hơn",input_formats = [D4_DATE_ONLY_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATE_ONLY_FORMAT))
    Site_type  = forms.ModelChoiceField(SiteType.objects.all(),initial=2)
    ngay_gio_tao =forms.DateTimeField(label=u"Ngày giờ tạo",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    ngay_gio_sua =forms.DateTimeField(label=u"Ngày giờ sửa",input_formats = [D4_DATETIME_FORMAT],required =False,widget =forms.DateTimeInput(format=D4_DATETIME_FORMAT,attrs={"readonly":"readonly"}))
    is_admin_set_update_edit_history = True
    def clean_active_3G(self):
        if not self.is_loc and self.cleaned_data['active_3G']==None:
            return False
        else:
            return self.cleaned_data['active_3G']
    def clean_active_4G(self):
        if not self.is_loc and self.cleaned_data['active_4G']==None:
            return False
        else:
            return self.cleaned_data['active_4G']
    def clean_active_2G(self):
        if not self.is_loc and self.cleaned_data['active_2G']==None:
            return False
        else:
            return self.cleaned_data['active_2G']
    def __init__(self, *args, **kwargs):
        super(TramForm, self).__init__(*args, **kwargs)
        self.fields['du_an'].help_text=u'có thể chọn nhiều dự án'
        download_ahref = HTML("""<a href="/omckv2/modelmanager/Tram_NTPForm/%s/" class="btn btn-success show-modal-form-link downloadscript">Download Script</a> """%self.instance.id) if (self.instance and self.instance.Site_ID_3G and 'ERI_3G' in self.instance.Site_ID_3G ) else None
        self.helper.form_action = '/omckv2/modelmanager/TramForm/new/'
        self.helper.layout = Layout(
        TabHolder(
            Tab(
                      u'Thông tin 3G',
                      Div('Site_ID_3G',  'Site_Name_1', 'Site_Name_2','Project_Text', 'Status', 'du_an','active_3G','id','Site_type',css_class= 'col-sm-2'),
                      Div(  'Cell_1_Site_remote', 'Cell_2_Site_remote', 'Cell_3_Site_remote','Cell_4_Site_remote', 'Cell_5_Site_remote','Cell_6_Site_remote','is_co_U900_rieng','is_co_U2100_rieng',css_class= 'col-sm-2'),
                      Div('Cell_7_Site_remote', 'Cell_8_Site_remote', 'Cell_9_Site_remote','Cell_K_U900_PSI', Field('RNC',css_class= 'mySelect2') , Field('Cabinet',css_class= 'mySelect2')  , 'Port', download_ahref , css_class= 'col-sm-2'),
                      Div(HTML('<h4 style="color:red">Truyền dẫn IUB</h4>'),'IUB_HOST_IP','IUB_VLAN_ID', 'IUB_SUBNET_PREFIX', 'IUB_DEFAULT_ROUTER','Trans',css_class= 'col-sm-2'),
                      Div(  HTML('<h4 style="color:blue">Truyền dẫn MUB</h4>'),'MUB_HOST_IP','MUB_VLAN_ID',  'MUB_SUBNET_PREFIX', 'MUB_DEFAULT_ROUTER','ghi_chu_tram',\
                            Div(AppendedText('Ngay_Phat_Song_3G','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker_only_date'),\
                            Div(AppendedText('Ngay_Phat_Song_3G_lon_hon','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker_only_date'),\
                            css_class= 'col-sm-2'),
                      Div('U900','ntpServerIpAddressPrimary','ntpServerIpAddressSecondary','ntpServerIpAddress1','ntpServerIpAddress2',css_class= 'col-sm-2'),
                
            ),           
            Tab(u'Thông tin 2G',
              Div('BSC_2G','Site_ID_2G','Site_ID_2G_Number', 'LAC_2G','Cell_ID_2G',\
                   Div(AppendedText('Ngay_Phat_Song_2G','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker_only_date'),\
                Div(AppendedText('Ngay_Phat_Song_2G_lon_hon','<span class="glyphicon glyphicon-calendar"></span>'),css_class='input-group date datetimepicker_only_date'),\
                  'active_2G',css_class= 'col-sm-3'),
              Div('cau_hinh_2G',Field('nha_san_xuat_2G',css_class= 'mySelect2')  ,'TG_Text','TG','TG_1800' , 'TRX_DEF',css_class= 'col-sm-3')
            ),
           Tab(u'Thông tin 4G',
              Div('eNodeB_Name', 'eNodeB_ID_DEC',css_class= 'col-sm-3'),
              Div(Field('eNodeB_Type',css_class= 'mySelect2'),'active_4G',css_class= 'col-sm-3')
            ),
            Tab(
                 u'Thông tin trạm', Div('Ma_Tram_DHTT','Nha_Tram','dia_chi_2G', 'dia_chi_3G',css_class= 'col-sm-3'), Div('Long_3G','Lat_3G','Long_2G', 'Lat_2G',\
                Field('UPE',css_class= 'mySelect2'),Field('tinh',css_class= 'mySelect2'),Field('quan_huyen',css_class= 'mySelect2')  ,css_class= 'col-sm-3'),\
                 Div('nguoi_tao','ngay_gio_tao','nguoi_sua_cuoi_cung','ngay_gio_sua', 'ly_do_sua','import_ghi_chu',css_class= 'col-sm-3')
            ),

            Tab(
                 u'Hide',HTML('Hide')
            ),
            Tab(
                 'Edit History',self.htmltable
            ),
                  Tab(
                 'Hướng dẫn',HTML(HUONG_DAN)
            )
                
        )
    )
    
    def update_action_and_button(self,*args, **kwargs):
        super(TramForm, self).update_action_and_button(*args, **kwargs)
        self.update_edit_history()

    class Meta:
        model = Tram
        exclude=['License_60W_Power']
        help_texts = {'du_an':'','Site_ID_2G':u'Site Name 2G','Nha_Tram':u'Tên trạm VTT quản lý'     }
        widgets={'import_ghi_chu':forms.Textarea(),'ghi_chu':forms.Textarea()}
######################################################################################################################################################
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                                                                                                     #
#                                                                                                                                                     #
######################################################################################################################################################
#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE#TABLE

#class SearchHistoryTable(TableReport):
import models

class LenhTable(BaseTableForManager):
    is_report_download = True
    jquery_url= '/omckv2/modelmanager/LenhForm/new/'
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    edit_comlumn = tables.Column(accessor="pk", orderable=False)
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    
    class Meta:
        model = Lenh
        sequence = ("selection",'id','command','Name','thiet_bi','ghi_chu_lenh','edit_comlumn')
        attrs = {"class": "lenh-table table-bordered"}
    def render_edit_comlumn(self,value):
        return mark_safe('<div><button class="btn  btn-default edit-entry-btn-on-table" id= "%s" type="button">Edit</button></div></br>'%value)
class TrangThaiTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/TrangThaiForm/new/'
    class Meta:
        model = TrangThai
        attrs = {"class": "table-bordered"}       
class ThietBiTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/ThietBiForm/new/'
    class Meta:
        model = ThietBi
        attrs = {"class": "table-bordered"}
class CaTrucTable(BaseTableForManager):
    jquery_url= '/omckv2/modelmanager/CaTrucForm/new/'
    class Meta:
        model = CaTruc
        attrs = {"class": "table-bordered"}
class BSCRNCTable(BaseTableForManager):
    jquery_url= '/omckv2/modelmanager/BSCRNCForm/new/'
    class Meta:
        model = BSCRNC
        attrs = {"class": "table-bordered"}
class TinhTable(BaseTableForManager):
    jquery_url= '/omckv2/modelmanager/TinhForm/new/'
    class Meta:
        model = Tinh
        attrs = {"class": "table-bordered"}
class UPETable(BaseTableForManager):
    jquery_url= '/omckv2/modelmanager/UPEForm/new/'
    class Meta:
        model = UPE
        attrs = {"class": "table-bordered"}
class BCNOSSTable(BaseTableForManager):
    gio_mat = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    gio_tot = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    gio_canh_bao_ac = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/BCNOSSForm/new/'
    class Meta:
        model = BCNOSS
        attrs = {"class": "table-bordered"}
class DoiTacTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/DoiTacForm/new/'
    class Meta:
        model = DoiTac
        exclude = ('Name_khong_dau',)
        attrs = {"class": "table-bordered"}
class SuCoTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/SuCoForm/new/'
    class Meta:
        model = SuCo
        attrs = {"class": "table-bordered"}
class NguyenNhanTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/NguyenNhanForm/new/'
    class Meta:
        model = NguyenNhan
        attrs = {"class": "table-bordered"}
class DuAnTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/DuAnForm/new/'
    class Meta:
        model = DuAn
        attrs = {"class": "table-bordered"}
class ThaoTacLienQuanTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/ThaoTacLienQuanForm/new/'
    class Meta:
        model = ThaoTacLienQuan
        attrs = {"class": "table-bordered"}
class FaultLibraryTable(BaseTableForManager):
    ngay_gio_tao = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    ngay_gio_sua = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    jquery_url= '/omckv2/modelmanager/FaultLibraryForm/new/'
    class Meta:
        model = FaultLibrary
        attrs = {"class": "table-bordered"}
class SpecificProblemTable(BaseTableForManager):
    jquery_url= '/omckv2/modelmanager/SpecificProblemForm/new/'
    class Meta:
        model = SpecificProblem
        attrs = {"class": "table-bordered"}


class UserProfileTable(BaseTableForManager):
    jquery_url= '/omckv2/modelmanager/UserProfileForm/new/'
    class Meta:
        model = UserProfile
        attrs = {"class": "table-bordered"}  
class EditHistoryTable(TableReport):
    is_report_download = False
    object_name = tables.Column(accessor="edited_object_id",verbose_name="object_name")
    jquery_url= '/omckv2/modelmanager/EditHistoryForm/new/'
    def render_object_name(self,record,value):#record = row
        Classofedithistory = eval('models.' + record.modal_name)
        instance = Classofedithistory.objects.get(id = value)
        return instance.__unicode__
        #return str(value)+ record.modal_name
    class Meta:
        model = EditHistory
        exclude = ('id','modal_name','edited_object_id')
        sequence = ('object_name',)
        attrs = {"class": "table edit-history-table table-bordered"}
class SearchHistoryTable(TableReport):
    jquery_url= '/omckv2/modelmanager/SearchHistoryForm/new/'
    exclude = ('thanh_vien')
    edit_comlumn =  tables.Column(accessor="pk",)
    class Meta:
        model = SearchHistory
        attrs = {"class": "table history-table table-bordered","table-action":"/omckv2/edit_history_search/"}
    def render_edit_comlumn(self,value):
        return mark_safe('''<img src='media/images/pencil.png' class='btnEdit'/><img src='media/images/delete.png' class='btnDelete'/>''' )


class TramTable(BaseTableForManager):
    Ngay_Phat_Song_3G = tables.DateColumn(format=D4_DATE_FORMAT_TABLE)
    Ngay_Phat_Song_2G = tables.DateColumn(format=D4_DATE_FORMAT_TABLE)
    #selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    #jquery_url = '/omckv2/tram_table/'
    jquery_url= '/omckv2/modelmanager/TramForm/new/'
    #is_show_download_link = True
    class Meta:
        exclude = ("License_60W_Power", )
        model = Tram
        sequence = ("Site_ID_3G","Site_Name_1",'Site_ID_2G',"id",)
        attrs = {"class": "tram-table table-bordered","id": "tram-table-id"}
class Tram_NTPTable(TableReport):
    
    #selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    #jquery_url = '/omckv2/tram_table/'
    jquery_url= '/omckv2/modelmanager/Tram_NTPForm/new/'
    #is_show_download_link = True
    class Meta:
        fields=('Site_ID_3G','Site_Name_1','RNC','ntpServerIpAddressPrimary','ntpServerIpAddressSecondary','ntpServerIpAddress1','ntpServerIpAddress2')
        model = Tram
        attrs = {"class": "same-ntp table-bordered"}

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
class MllTable(TableReport):
    is_report_download = True
    edit_comlumn = tables.Column(accessor="pk", orderable=False,verbose_name="Edit/ADD")
    gio_tot = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    #last_update_time = tables.DateTimeColumn(format="H:i d-m")
    #doi_tac = tables.Column(accessor="doi_tac.Name",verbose_name="Doi tac")
    ca_truc = tables.Column(accessor="ca_truc.Name",verbose_name=u"Ca Trực")
    trang_thai = tables.Column(accessor="trang_thai.Name",verbose_name=u"Trạng thái")
    cac_buoc_xu_ly = tables.Column(accessor="pk",verbose_name=u"Các bước xử lý")
    specific_problem = tables.Column(accessor="pk")
    #su_co = tables.Column(accessor='su_co.Name',verbose_name="nguyên nhân")
    jquery_url = '/omckv2/modelmanager/MllForm/new/'
    gio_mat = tables.DateTimeColumn(format=TABLE_DATETIME_FORMAT)
    class Meta:
        model = Mll
        attrs = {"class": "tablemll table-bordered paleblue scroll",'name':'MllTable','id':'mll-table-id'}#paleblue
        exclude=('gio_nhap','gio_bao_uc','last_update_time','doi_tac','nguoi_sua_cuoi_cung','ngay_gio_tao','ngay_gio_sua','ly_do_sua')
        sequence = ('id','object','site_name','thiet_bi','su_co','nguyen_nhan','nghiem_trong','du_an','ung_cuu','nguoi_tao','ca_truc'\
                    ,'gio_mat','gio_tot','trang_thai','specific_problem','cac_buoc_xu_ly','edit_comlumn','giao_ca',)
    
    def as_row_generator(self):
        csv_header = [column.header for column in self.columns]
        yield csv_header
        for row in self.rows:
            csv_row = []
            for column, cell in row.items():
                if isinstance(cell, basestring):
                    # if cell is not a string strip_tags(cell) get an
                    # error in django 1.6
                    cell = strip_tags(cell)
                else:
                    cell = unicode(cell)
                csv_row.append(cell)
            yield csv_row
    def as_xls_d4_in_form_py_csv(self, request):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in self.as_row_generator()),
                                         content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        return response
    def as_xls_d4_in_form_py_xls(self,request):
        #from pytz import timezone
        #settingstime_zone = timezone(TIME_ZONE)
        
        response = HttpResponse()
        file_name = self.Meta.model.__name__
        response['Content-Disposition'] = 'attachment; filename="Table_%s.xls"'%file_name
        # Styles used in the spreadsheet.  Headings are bold.
        header_font = xlwt.Font()
        header_font.bold = True
        header_style = xlwt.XFStyle()
        header_style.font = header_font
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet 1')
        # Cell width information kept for every column, indexed by column number.
        cell_widths = collections.defaultdict(lambda: 0)
        is_ung_cuu_report = True if 'ung_cuu' in request.GET and request.GET['ung_cuu'] == '2' else False
        #csv_header = [column.header for column in self.columns if (column.header!='Edit Comlumn' and (column.header!='Cac Buoc Xu Ly' and is_ung_cuu_report) )]
        csv_header = []
        for column in self.columns:
            if column.header=='Cac Buoc Xu Ly' and is_ung_cuu_report:
                csv_header.append('Ghi chú')
            elif column.header!='Edit/ADD':
                csv_header.append(column.header)
             
            
            
        
        if is_ung_cuu_report:
            csv_header.extend(['thoi_diem_bao_ung_cuu','thoi_luong_ung_cuu','thoi_luong_mll'])
        write_row(ws, 0, csv_header, cell_widths, style=header_style, encoding='utf-8')
        for lno,row in enumerate(self.rows):
            csv_row = []
            
            
            if is_ung_cuu_report:
                comment_ung_cuu_object  =row.record.comments.filter(trang_thai=TrangThai.objects.get(Name=u'Báo ứng cứu')).first()
                if comment_ung_cuu_object:
                    
                    uc_datetime = comment_ung_cuu_object.datetime
                    '''
                    uc_datetime = uc_datetime.astimezone(settingstime_zone)
                    thoi_diem_bao_ung_cuu = uc_datetime.strftime(D4_DATETIME_FORMAT)
                    '''
                    uc_datetime = timezone.localtime(uc_datetime)
                    thoi_diem_bao_ung_cuu = uc_datetime.strftime(D4_DATETIME_FORMAT)
                    #print thoi_diem_bao_ung_cuu
                    noidungcomment = comment_ung_cuu_object.comment
                    if row.record.gio_tot:
                        thoi_luong_ung_cuu = str(int((row.record.gio_tot - comment_ung_cuu_object.datetime).total_seconds() / 60))
                        thoi_luong_mll = str(int((row.record.gio_tot - row.record.gio_mat).total_seconds() / 60))
                    else:
                        thoi_luong_ung_cuu = u'_'
                        thoi_luong_mll = u'_'
                else:
                    thoi_luong_ung_cuu = u'_'
                    thoi_diem_bao_ung_cuu = u'_'
                    thoi_luong_mll = u'_'
                    noidungcomment = u'—'
                    
                    
            for column, cell in row.items():
                if column.header=='Edit/ADD':
                    continue
                elif  column.header=='Cac Buoc Xu Ly' and is_ung_cuu_report:
                    cell = noidungcomment
                if isinstance(cell, basestring):
                    # if cell is not a string strip_tags(cell) get an
                    # error in django 1.6
                    cell = strip_tags(cell)
                else:
                    cell = unicode(cell)
                csv_row.append(cell)
            #csv_row.append(str(row.record.id))#comments
            
            if is_ung_cuu_report:    
                csv_row.extend([thoi_diem_bao_ung_cuu,thoi_luong_ung_cuu,thoi_luong_mll])#comments
            write_row(ws, lno+ 1, csv_row, cell_widths, style=None, encoding='utf-8')
        # Roughly autosize output column widths based on maximum column size.
        '''
        for col, width in cell_widths.items():
            ws.col(col).width = width
        '''
        setattr(response, 'content', '')
        wb.save(response)
        return response
    
    
    def render_specific_problem(self,value):
        mll = Mll.objects.get(id=value)
        sp_all =  mll.specific_problems.all()
        if not sp_all:
            return ''
        result = '<ul class="non-bullet-ul">'
        for x in sp_all:
            result = result + '<li>' + ( '<a  href="/omckv2/modelmanager/FaultLibraryForm/%s/" class="green-color-text show-modal-form-link">'%x.fault.id + ((x.fault.Name  + '</a>**' )) if x.fault else '')\
              + ( ('<a href="/omckv2/modelmanager/SpecificProblemForm/%s/" class="show-modal-form-link">'%x.id + x.object_name + '</a>') if x.object_name else '') + '</li>'
        result +='</ul>'
        result = mark_safe(result)
        return result
    def render_site_name(self,value):
        return mark_safe('<a href="/omckv2/modelmanager/TramForm/%s/" class="show-modal-form-link" style="color:red">%s</a>'%(value,value))
    def render_nguoi_tao(self,value):
        userprofile = User.objects.get(username=value).get_profile()
        return mark_safe('<a href="/omckv2/modelmanager/UserProfileForm/%s/" class="show-modal-form-link" style="color:%s">%s</a>'%(userprofile.id,userprofile.color_code,value))
    def render_thiet_bi(self,value,record):
        #tb_instance = ThietBi.objects.get(Name = value)
        tb_instance = record.thiet_bi
        return mark_safe('<a href="/omckv2/modelmanager/ThietBiForm/%s/" class="show-modal-form-link" style="color:%s" >%s</a>'%(tb_instance.id,tb_instance.color_code,str(tb_instance)))
    def render_ca_truc(self,value):
        tb_instance = CaTruc.objects.get(Name = value)
        return mark_safe('<a href="/omckv2/modelmanager/CaTrucForm/%s/" class="show-modal-form-link ca-truc-%s">%s</a>'%(tb_instance.id,value,value))
    def render_du_an(self,value):
        duan_instance = DuAn.objects.get(Name = value)
        return mark_safe('<a href="/omckv2/modelmanager/DuAnForm/%s/" class="show-modal-form-link" style="color:%s" >%s</a>'%(duan_instance.id,duan_instance.color_code,value))
    def render_su_co(self,value):
        instance = SuCo.objects.get(Name = value)
        return mark_safe('<a href="/omckv2/modelmanager/SuCoForm/%s/" class="show-modal-form-link" style="color:%s" >%s</a>'%(instance.id,instance.color_code,value))
    def render_nguyen_nhan(self,value):
        instance = NguyenNhan.objects.get(Name = value)
        return mark_safe('<a href="/omckv2/modelmanager/NguyenNhanForm/%s/" class="show-modal-form-link" style="color:%s" >%s</a>'%(instance.id,instance.color_code,value))
    def render_trang_thai(self,value):
        trang_thai_instance = TrangThai.objects.get(Name = value)
        return mark_safe('<a href="/omckv2/modelmanager/TrangThaiForm/%s/" class="show-modal-form-link" style="color:%s">%s</a>'%(trang_thai_instance.id,trang_thai_instance.color_code,value))
    '''
    def render_doi_tac(self,value,record):
        mll = Mll.objects.get(id=record.id)
        dt = mll.doi_tac
        return DoiTac_showing (dt,is_show_donvi=True)
    '''
    def render_cac_buoc_xu_ly(self,value):
        mll = Mll.objects.get(id=value)
        #cms = '<ul class="comment-ul">' + '<li>' + (timezone.localtime(mll.gio_mat)).strftime(D4_DATETIME_FORMAT)+ ' ' + mll.cac_buoc_xu_ly + '</li>'
        querysetcm = mll.comments.all().order_by("id")
        t = get_template('drivingtest/comment_in_mll_table_show.html')
        c = Context({ 'querysetcm': querysetcm })
        #rendered = t.render(c)
        return mark_safe(t.render(c))
        
    def render_edit_comlumn(self,value):
        return mark_safe('''
        <div><button class="btn  d4btn-edit-column btn-default edit-entry-btn-on-table" id= "%s" type="button">Edit</button></div>
        <div><a class="btn  d4btn-edit-column btn-primary show-modal-form-link add-comment" href="/omckv2/modelmanager/CommentForm/new/">Add</a></div>
        <div class="dropdown "><button class="btn btn-default d4btn-edit-column-dropdown dropdown-toggle dropdown-class" type="button" id="dropdownMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">More<span class="caret"></span></button> <ul class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenu"><li><a class="show-modal-form-link Nhan-Tin-UngCuu" href="/omckv2/modelmanager/NhanTinUngCuuForm/new/">Nt</a></li></ul></div>''' %value)
        


            
            




               
