# -*- coding: utf-8 -*- 

import xlrd,datetime
from django.core.exceptions import MultipleObjectsReturned
from unidecode import unidecode
import tempfile
import zipfile
import re
import random
#from pytz import timezone
from time import strftime
from django.utils import timezone
import pytz
import os
from exceptions import AttributeError
from django.forms.fields import DateField
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from rnoc.forms import D4_DATETIME_FORMAT, D4_DATE_ONLY_FORMAT
from rnoc.models import Tram, Mll, DoiTac, SuCo,\
    CaTruc, UserProfile, TrangThai, DuAn, ThaoTacLienQuan, ThietBi,\
    EditHistory, Lenh, FaultLibrary, NguyenNhan, Tinh, BSCRNC,\
    SiteType



def unique_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def read_line(path,split_item):
    f =  open(path, "r")
    content = f.read().decode('utf-8')
    content = content.split(split_item)
    f.close()
    return content


def read_file_from_disk (path):
    f =  open(path, "rb") 
    a = f.read().decode('utf-8')
    f.close()
    return a


def save_file_to_disk(path,content, is_over_write):
    if is_over_write:
        with open(path, "wb") as f:
            f.write(content.encode('utf-8'))
    else:
        with open(path, "ab") as f:
            f.write(content.encode('utf-8'))


def myprint():
    pass       
def read_excel_cell(worksheet,curr_row_number,curr_col):
    print  'curr_col curr_row_number ',curr_col, curr_row_number
    cell_value = worksheet.cell_value(curr_row_number, curr_col)
    print 'cell_value',cell_value
    return cell_value

class Excel_2_3g(object):
    allow_create_one_instance_if_not_exit = True
    fields_allow_empty_use_function =[]# nhung cai field ma excel = rong van dung fucntion de gan gia tri cho field, vi du nhu field namekhong dau
    is_import_from_exported_file = False
    #added_foreinkey_types = set() # cai nay dung de tinh so luong du an, hoac thietbi, duoc add, neu nhieu qua thi stop
    added_foreinkey_types = 0 # cai nay dung de tinh so luong du an, hoac thietbi, duoc add, neu nhieu qua thi stop
    max_length_added_foreinkey_types = 500
    backwards_sequence =[]
    many2manyFields = []
    update_or_create_main_item = ''#Site_ID_3G
    worksheet_name = u'Sheet 1'
    begin_row=0
    manual_mapping_dict = {}
    mapping_function_to_value_dict = {}
    auto_map = False
    model = Tram
    created_number =0
    update_number = 0
    just_create_map_field = False
    
    def __init__(self,workbook=None):
        
            
        self.workbook = workbook
        self.read_excel()
        self.excel_dict = self.define_attr_dict() # excel_dict la ten cua cac cot lay trong file excel ra
        print 'excel_dict',self.excel_dict
        self.base_fields = {}
        self.missing_fields =[]
        self.model_fieldnames = [f.name for f in self.model._meta.fields if f.name!='id' ]
        if self.many2manyFields: # self.ModelClass._meta.many_to_many
                for x in self.many2manyFields:
                    if x not in self.model_fieldnames:
                        self.model_fieldnames.append(x)
        if self.is_import_from_exported_file:
            for f in  self.model._meta.fields:
                if (f.verbose_name in self.excel_dict)  :
                    if f.name =='id':
                        continue
                    else:
                        print '@@@f.name ',f.name 
                        self.base_fields[f.name] = self.excel_dict.get(f.verbose_name)
                elif f.name.replace("_",' ') in self.excel_dict:
                    self.base_fields[f.name] = self.excel_dict.get(f.name.replace("_",' ') )
                else:
                    self.missing_fields.append(f.name)
        else:
            for fname in self.model_fieldnames:
                fname_lower = fname.lower()
                if self.auto_map and (fname_lower in self.excel_dict):
                    self.base_fields[fname] = self.excel_dict[fname_lower]
                else: # 1 so attribute khong nam trong file excel
                    if fname in self.manual_mapping_dict: #manual_mapping_dict la manual , do minh tu tao anh xa fieldname voi ten cot cua file excel
                        fieldname_compare_with_fn_excel = self.manual_mapping_dict[fname]
                        if isinstance(fieldname_compare_with_fn_excel, int):
                            self.base_fields.update({fname:fieldname_compare_with_fn_excel})
                        else:
                            fieldname_in_excel =  unidecode(fieldname_compare_with_fn_excel).lower().replace(' ','_') # file name format
                            if fieldname_in_excel in self.excel_dict:
                                self.base_fields[fname]= self.excel_dict[fieldname_in_excel] #= so thu tu cua column chua field do, vi du 5
                            else: # thieu cot nay hoac da bi doi ten                        
                                raise ValueError('trong file excel thieu cot %s '%fieldname_in_excel)
                    else:
                        self.missing_fields.append(fname)
        for fname in self.fields_allow_empty_use_function:
            if fname in self.model_fieldnames and fname not in self.base_fields:
                self.base_fields[fname] = None
        print '@@@@@@@@@@@@@base_fields',self.base_fields
        self.main_field_index_excel_column = self.base_fields.pop(self.update_or_create_main_item) #index of main fields
        self.convert_basefield_to_list_of_tuple()
        
        if self.just_create_map_field:#for test
            return None
        
        self.loop_through_row_and_insertdb()
    def convert_basefield_to_list_of_tuple(self):
        if self.backwards_sequence:
            #can phai sap xep lai theo chuan [(),()] theo thu tu
            base_fields_lists = [x for x in self.base_fields.iterkeys()]
            for x in self.backwards_sequence:
                if x in base_fields_lists:
                    base_fields_lists.remove(x)
                    base_fields_lists.append(x)
            self.odering_base_columns_list_tuple = [(x, self.base_fields[x]) for x in base_fields_lists]
        else:
            self.odering_base_columns_list_tuple = [(k,v) for k, v in self.base_fields.iteritems()]
        print 'self.odering_base_columns_list_tuple',self.odering_base_columns_list_tuple
    def read_excel(self):
        self.worksheet = self.workbook .sheet_by_name(self.worksheet_name)
        self.num_rows = self.worksheet .nrows - 1
        self.num_cols = self.worksheet.ncols - 1
    def define_attr_dict(self):
        dict_attrName_columnNumber_excel_not_underscore = {}
        curr_row_number = self.begin_row
        curr_col = 0
        while curr_col <= self.num_cols:
            atrrname = read_excel_cell(self.worksheet, curr_row_number,curr_col)
            #atrrname la field name hay la collumn name
            if not self.is_import_from_exported_file:
                print '@@@@@@@@@@@atrrname',curr_col,atrrname
                atrrname = unidecode(atrrname).lower().replace(" ","_")
            else:
                atrrname = atrrname.replace("_"," ")
                
            dict_attrName_columnNumber_excel_not_underscore[atrrname ]=   curr_col
            curr_col +=1
        return dict_attrName_columnNumber_excel_not_underscore
    
    def loop_through_row_and_insertdb(self):
        curr_row_number = self.begin_row 
        self.tram_co_trong_3g_location_but_not_in_db3g = 0
        while curr_row_number < self.num_rows:
            curr_row_number += 1
            print ' @@@@@@@@@@@@@ curr_row_number',curr_row_number
            to_value_function = self.get_function(self.update_or_create_main_item) # function for main field
            value = read_excel_cell(self.worksheet, curr_row_number,self.main_field_index_excel_column)
            if to_value_function:
                value = to_value_function(value)
            karg = {self.update_or_create_main_item:value}
            filters = self.model.objects.filter(**karg)
            if filters: # co db_row nay roi, update thoi
                print '*update'
                self.created_or_update = 0
                for self.obj in filters:# loop va gan gia tri vao self.obj
                    self.update_field_for_obj(curr_row_number)
                    self.update_number +=1
                    print '@ so luong instance duoc update,',self.update_number
            else: #tao moi
                print '*tao moi'
                if self.allow_create_one_instance_if_not_exit:
                    self.created_or_update = 1   
                    self.obj = self.model(**karg)
                    self.update_field_for_obj(curr_row_number)
                    self.created_number +=1
                    print '@ so luong instance duoc tao moi(new),',self.created_number
                else:
                    self.tram_co_trong_3g_location_but_not_in_db3g +=1
                    print '@ so luong instance tram_co_trong_3g_location_but_not_in_db3g,',self.tram_co_trong_3g_location_but_not_in_db3g
                    continue
        print '***Tong Ket '
        print '@ so luong instance duoc update,',self.update_number
        print '@ so luong instance duoc tao moi(new),',self.created_number
        print '@ so luong instance tram_co_trong_3g_location_but_not_in_db3g,',self.tram_co_trong_3g_location_but_not_in_db3g
    def update_field_for_obj(self,curr_row_number):
        for field_tuple in self.odering_base_columns_list_tuple:
            field = field_tuple[0]
            column_number = field_tuple[1]
            print 'field',field
            if column_number !=None:
                value =  read_excel_cell(self.worksheet, curr_row_number,column_number)
            else:
                value = None
            if value=='' or value =="null"or value ==u'—':
                value = None
            if  value !=None or field in self.fields_allow_empty_use_function:
                to_value_function = self.get_function(field)
                if to_value_function:
                    value = to_value_function(value)
                    if value==None:#to_value_function chu dong tra ve None neu khong muon luu field
                        continue
                setattr(self.obj, field, value) # save
           
        self.obj.save()        
    def get_function(self,field):
        if field in self.mapping_function_to_value_dict:
            func_name = self.mapping_function_to_value_dict[field]
            to_value_function = getattr(self, func_name)
            return to_value_function
        else:
            try:
                method_of_field_name = 'value_for_'+field
                to_value_function = getattr(self, method_of_field_name) #
                return to_value_function
            except: # Ko co ham nao thay doi gia tri value
                return None
    def value_for_Site_type(self,value):
        return SiteType.objects.get_or_create(Name = u'Site thường')[0]
    def value_for_dateField(self,cell_value):
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(cell_value)) # delte du lieu datetime
            get_col2 = str(date + get_)[:10] # convert date to string theo dang nao do
            value = get_col2 # moi them vo
            return value
        except:
            return None
    def value_for_RNC(self,value):
        if value:
            try:
                instance = Tram.objects.get(Site_Name_1 = value)
            except Tram.DoesNotExist:
                if self.added_foreinkey_types  > self.max_length_added_foreinkey_types:
                    raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
                instance = Tram(Site_Name_1 = value,Site_type = SiteType.objects.get(Name = u'Site 0 (RNC,BSC)'),ngay_gio_tao = timezone.now(),nguoi_tao = User.objects.get(username = u'rnoc2'))
                instance.save()
                
                
            try:
                instance = BSCRNC.objects.get(Name = value)
            except BSCRNC.DoesNotExist:
                if self.added_foreinkey_types  > self.max_length_added_foreinkey_types:
                    raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
                instance = BSCRNC(Name = value, ngay_gio_tao = timezone.now(),nguoi_tao = User.objects.get(username = 'rnoc2'))
                instance.save()
            return instance
        else:
            return None
    def value_for_Name(self,value):
        if value:
            return value.rstrip().lstrip()
        else:
            return ''
    def value_for_common_datefield(self,cell_value):
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(cell_value)) # delta du lieu datetime
            value = date + get_
            return value
        except:
            return None
    def value_for_common_datefield_exported_type(self,cell_value):
        cell_value = re.sub("$'", "", cell_value)
        d = datetime.datetime.strptime(cell_value, '%d/%m/%Y')
        return d
    def value_for_Cabinet(self,cell_value,name_ThietBi_attr= 'Cabinet'):
        try:
            thietbi = ThietBi.objects.get(Name=cell_value)
        except:
            thietbi = ThietBi(Name=cell_value)
            self.added_foreinkey_types +=1
            if self.added_foreinkey_types  > self.max_length_added_foreinkey_types:
                raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
            thietbi.is_duoc_tao_truoc = True
            thietbi.nguoi_tao = User.objects.get(username="rnoc2")
            thietbi.save()
        setattr(self.obj,name_ThietBi_attr,thietbi)
        return None
    def value_for_common_VLAN_ID (self,cell_value):
        value = int(cell_value)
        return value   
    
    def value_for_nguoi_tao (self,cell_value):
        print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ value_for_nguoi_tao',self.created_or_update 
        if self.created_or_update ==1:
            if cell_value==None:
                user = User.objects.get (username = 'rnoc2')
                return user
            else:
                user = User.objects.get (username = cell_value)
                return user
        else:
            return None
    def value_for_nguoi_sua_cuoi_cung (self,cell_value):
        user = User.objects.get (username = cell_value)
        return user

    def value_for_ngay_gio_tao(self,cell_value):
        if self.created_or_update ==1:
            if cell_value:
                cell_value = re.sub("^'", "", cell_value)
                cell_value = re.sub('\s$', '', cell_value)
                d = datetime.datetime.strptime(str(cell_value), D4_DATETIME_FORMAT)
                '''eastern = pytz.timezone('Asia/Bangkok')
                loc_dt = eastern.localize(d)
                '''
                #loc_dt = timezone.localtime(d)
                return d
            else:
                #now = datetime.datetime.now()
                now = timezone.now()
                '''
                now_str = now.strftime(D4_DATETIME_FORMAT)
                now = datetime.datetime.strptime(now_str, D4_DATETIME_FORMAT)
                print '@@@@@@@@type cua now',type(now)
                '''
                return now
        else:
            return None
    def value_for_ngay_gio_sua(self,cell_value):
        cell_value = re.sub("^'", "", cell_value)
        cell_value = re.sub(' $', '', cell_value)
        d = datetime.datetime.strptime(str(cell_value), D4_DATETIME_FORMAT)
        return d
     
    def value_for_excel_export_boolean(self,cell_value):#boolean not null allowed
        print '@@@@@@@@@cell_value',cell_value
        if cell_value ==u'✘' or cell_value==None:
            return False
        else:
            return True
    def value_for_Name_khong_dau(self,cell_value):
        field_co_dau = self.obj.Name
        if field_co_dau==None:
            return None
        return unidecode(field_co_dau)
class ExcelChung (Excel_2_3g):
    #backwards_sequence =['Site_ID_2G',]#de lay gia tri nha_san_xuat_2G truoc
    is_import_from_exported_file = True
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'Database 2G'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_2G':'value_for_common_datefield_exported_type','Ngay_Phat_Song_3G':'value_for_common_datefield_exported_type'}
    manual_mapping_dict = {}

    def value_for_nha_san_xuat_2G(self,cell_value):
        thietbi = ThietBi.objects.get_or_create(Name=cell_value)[0]
        self.added_foreinkey_types.add(thietbi)#set().add
        l = len(self.added_foreinkey_types)
        print "cabin**",l
        if l >self.max_length_added_foreinkey_types:
            raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
        self.obj.nha_san_xuat_2G=thietbi
        #self.obj.save()
        return None
    
    
    



    
class ExcelImportTrangThai (Excel_2_3g):
    is_import_from_exported_file = True
    fields_allow_empty_use_function = ['color_code','is_cap_nhap_gio_tot','nguoi_tao','ngay_gio_tao','is_duoc_tao_truoc','Name_khong_dau']
    #backwards_sequence =['Name_khong_dau']#de lay gia tri nha_san_xuat_2G truoc
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Name'
    worksheet_name = u'Sheet 1'
    mapping_function_to_value_dict ={'is_cap_nhap_gio_tot':'value_for_excel_export_boolean','is_duoc_tao_truoc':'value_for_excel_export_boolean'}
    manual_mapping_dict = {}
    model = TrangThai
    
    def value_for_color_code(self,cell_value):#boolean
        if cell_value:
            return cell_value
        else:
            return "#%06x" % random.randint(0, 0xFFFFFF)
    '''
    def value_for_is_cap_nhap_gio_tot(self,cell_value):#boolean not null allowed
        #if cell_value ==u'✔':
            #return True
        if cell_value ==u'✘' or cell_value==None:
            return False
        else:
            return True
    
    def value_for_is_duoc_tao_truoc(self,cell_value):
        if self.obj.Name  ==u"Raise sự kiện":
            return True
        else:
            return False
    '''
class ExcelImportSuCo(ExcelImportTrangThai):
    model = SuCo
'''
class ExcelImportSuCo_old(Excel_2_3g):
    is_import_from_exported_file = True
    fields_allow_empty_use_function = ['nguoi_tao','ngay_gio_tao','Name_khong_dau']
    backwards_sequence =[]
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Name'
    worksheet_name = u'Sheet 1'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {}
    model = SuCo
'''
class ExcelImportNguyenNhan(ExcelImportTrangThai):
    model = NguyenNhan
    def value_for_color_code(self,cell_value):#boolean
        if cell_value:
            return cell_value
        else:
            #return "#%06x" % random.randint(0, 0xFFFFFF)
            return 'green'
class ExcelImportDoiTac (ExcelImportTrangThai):
    model = DoiTac
class ExcelImportDoiTac_ungcuu (Excel_2_3g):
    fields_allow_empty_use_function = ['Name_khong_dau','nguoi_tao','ngay_gio_tao']
    manual_mapping_dict = {'Name':u'HO_TEN','Don_vi' :u'TINH_TP1','So_dien_thoai':u'DIEN_THOAI','Thong_tin_khac':u'TINH_TP','email':u'EMAIL'}
    model = DoiTac
    worksheet_name = u'Sheet1'
    update_or_create_main_item = u'Name'
    def value_for_So_dien_thoai(self,value):
        if value:
            value = str(value)
            
            rs = re.subn('\.0$', '', value, 1)
            if rs[1]:
                value = rs[0]
                if value[0] !='0':
                    value = '0' + value
                return value
            else:
                return value
        else:
            return None
    def value_for_Thong_tin_khac(self,value):
        if value:
            try:
                tinh = Tinh.objects.get(ma_tinh=value)
                value = value + u', ' + tinh.dia_ban
                return value
            except Tinh.DoesNotExist:
                return value
        else:
            return None
class ImportTinh(Excel_2_3g):
    fields_allow_empty_use_function = ['Name_khong_dau']
    manual_mapping_dict = {'Name':u'Tên tỉnh','ma_tinh' :u'TINH_TP',}
    model = Tinh
    worksheet_name = u'Sheet1'
    update_or_create_main_item = u'Name'
class ImportTinh_diaban(Excel_2_3g):
    fields_allow_empty_use_function = []
    manual_mapping_dict = {'Name':u'Khu vực','dia_ban' :u'Địa bàn','ghi_chu':u'Trực UCTT'}
    model = Tinh
    worksheet_name = u'Sheet3'
    update_or_create_main_item = u'Name'    
class ImportRNC(Excel_2_3g):
    auto_map = True
    fields_allow_empty_use_function = ['nguoi_tao','ngay_gio_tao']
    manual_mapping_dict = {'Name':u'RNCID'}
    model = BSCRNC
    worksheet_name = u'Thong ke NodeB-RNC'
    update_or_create_main_item = u'Name'
    def value_for_VI_TRI_RNC(self,value):
        if value:
            return Tinh.objects.get(ma_tinh = value)
        else:
            return None
class Import_RNC_Tram(Excel_2_3g):
    fields_allow_empty_use_function = ['nguoi_tao','ngay_gio_tao','Site_type']
    manual_mapping_dict = {'Site_Name_1':u'Name','dia_chi_2G':u'DIA CHI','dia_chi_3G':u'DIA CHI'}
    model = Tram
    worksheet_name = u'Sheet 1'
    update_or_create_main_item = 'Site_Name_1'
    def value_for_ngay_gio_tao(self,value):
        return timezone.now()
    def value_for_Site_type(self,value):
        return SiteType.objects.get_or_create(Name = u'Site 0 (RNC,BSC)')[0]
'''
class ExcelImportDoiTac_old (Excel_2_3g):
    is_import_from_exported_file = True
    fields_allow_empty_use_function = ['Name_khong_dau','nguoi_tao','ngay_gio_tao']
    backwards_sequence =['Name_khong_dau',]#de lay gia tri nha_san_xuat_2G truoc
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Name'
    worksheet_name = u'Sheet 1'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {}
    model = DoiTac
    def value_for_Name_khong_dau(self,cell_value):
        field_co_dau = self.obj.Name
        if cell_value:
            return unidecode(cell_value)
        else:
            return unidecode(field_co_dau)
        
'''
class ExcelImportDuAn(ExcelImportTrangThai):
    model = DuAn
    def value_for_color_code(self,cell_value):#boolean
        if cell_value:
            return cell_value
        else:
            #return "#%06x" % random.randint(0, 0xFFFFFF)
            return 'organe'
'''      
class ExcelImportDuAn_old(Excel_2_3g):
    is_import_from_exported_file = True
    fields_allow_empty_use_function = ['nguoi_tao','ngay_gio_tao','Name_khong_dau']
    backwards_sequence =[]#de lay gia tri nha_san_xuat_2G truoc 
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Name'
    worksheet_name = u'Sheet 1'
    mapping_function_to_value_dict ={'is_duoc_tao_truoc':'value_for_excel_export_boolean'}#uu tien sau
    manual_mapping_dict = {}
    model = DuAn
'''
class ExcelImportThietBi(ExcelImportTrangThai):
    model = ThietBi
    def value_for_color_code(self,cell_value):#boolean
        if cell_value:
            return cell_value
        else:
            #return "#%06x" % random.randint(0, 0xFFFFFF)
            return 'purple'
class ExcelImportFaultLibrary(ExcelImportTrangThai):
    model = FaultLibrary
class ExcelImportThaoTacLienQuan (ExcelImportTrangThai):
    model = ThaoTacLienQuan
class ExcelImportLenh (ExcelImportDuAn):
    fields_allow_empty_use_function = ['color_code','is_cap_nhap_gio_tot','nguoi_tao','ngay_gio_tao','is_duoc_tao_truoc','Name_khong_dau',]
    backwards_sequence= ['Name_khong_dau']
    update_or_create_main_item = 'command'
    model = Lenh
    def value_for_thiet_bi(self,value):
        if value:
            try:
                tb = ThietBi.objects.get(Name=value)
                return tb
            except ThietBi.DoesNotExist:
                return None
        else:
            return None
    '''    
    def value_for_Name(self,value):
        print '@@@@@@@@i want see'
        if value==None:
            print '@@@@@@@@i want see2'
            return ''
        else:
            return value
    '''
class Excel_3G(Excel_2_3g):
    fields_allow_empty_use_function = ['nguoi_tao','ngay_gio_tao','active_3G','Site_type']
    auto_map = True
    many2manyFields = ['du_an']
    just_create_map_field = False
    update_or_create_main_item = 'Site_ID_3G'
    worksheet_name = u'Ericsson 3G'
    backwards_sequence =['du_an']
    manual_mapping_dict = {'Project_Text':2,'du_an':2,'Cell_1_Site_remote':u'Cell 1 (carrier 1)', \
                    'Cell_2_Site_remote':u'Cell 2 (Carrier 1)', 'Cell_3_Site_remote':u'Cell 3 (Carrier 1)',\
                     'Cell_4_Site_remote':u'Cell 4 (Carrier 2)', 'Cell_5_Site_remote':u'Cell 5 (Carrier 2)', 'Cell_6_Site_remote':u'Cell 6 (Carrier 2)', \
                     'Cell_7_Site_remote':u'Cell 7 (remote/U900/3 carrier)', 'Cell_8_Site_remote':u'Cell 8 (remote/U900/3 carrier)', 'Cell_9_Site_remote':u'Cell 9 (remote/U900/3 carrier)',\
                     'Cell_K_U900_PSI':u'Cell K (U900 PSI)'
                     }
    mapping_function_to_value_dict = {'Ngay_Phat_Song_2G':'value_for_dateField',\
                                      'Ngay_Phat_Song_3G':'value_for_dateField',\
                                      'IUB_VLAN_ID':'value_for_int_to_string','MUB_VLAN_ID':'value_for_int_to_string',\
                                      'Cell_1_Site_remote':u'value_error_but_equal_42', \
                    'Cell_2_Site_remote':u'value_error_but_equal_42', 'Cell_3_Site_remote':u'value_error_but_equal_42',\
                     'Cell_4_Site_remote':u'value_error_but_equal_42', 'Cell_5_Site_remote':u'value_error_but_equal_42', 'Cell_6_Site_remote':u'value_error_but_equal_42', \
                     'Cell_7_Site_remote':u'value_error_but_equal_42', 'Cell_8_Site_remote':u'value_error_but_equal_42', 'Cell_9_Site_remote':u'value_error_but_equal_42',\
                     'Cell_K_U900_PSI':u'value_error_but_equal_42'
                                    }
    
    def value_error_but_equal_42(self,value):
        if value ==42:
            return None
        else:
            return value
    def value_for_du_an(self,cell_value):
        
        if self.created_or_update == 1 :#create
            self.obj.save()
        try:
            du_an = DuAn.objects.get(Name=cell_value)
        except:
            du_an = DuAn(Name=cell_value)
            self.added_foreinkey_types +=1
            if self.added_foreinkey_types > self.max_length_added_foreinkey_types:
                raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
            du_an.type_2G_or_3G = '3G'
            du_an.is_duoc_tao_truoc = True
            du_an.nguoi_tao = User.objects.get(username="rnoc2")
            du_an.ngay_gio_tao = timezone.now()
            du_an.save()
        self.obj.du_an.add(du_an)
        return None
    
    
    def value_for_Site_ID_3G(self,cell_value):
        ex = re.subn('_U900$','',cell_value)
        if ex[1]:# co phat hien chuoi _U900 o trong
            self.is_U900_hay_U2100 = 'U900'
            same_3g_has_site_name1 = ex[0]
            try:# co tram U2100 tuong ung voi tram U900 nay
                samesite_instance = Tram.objects.get(Site_ID_3G = 'ERI_3G_' + same_3g_has_site_name1)
                #giasu u2100 luon duoc tao ra truoc,
                samesite_instance.is_co_U900_rieng = True
                samesite_instance.save()
                self.is_co_U2100_rieng = True
            except:
                self.is_co_U2100_rieng = False
        else:# tram U2100
            self.is_U900_hay_U2100 = 'U2100'
            try:# neu co tram U900 rieng
                samesite_instance = Tram.objects.get(Site_ID_3G = 'ERI_3G_' + cell_value + '_U900')
                samesite_instance.is_co_U2100_rieng = True
                self.is_co_U900_rieng = True
            except:# khogn co tram U900 nao ung voi tram U2100 nay
                self.is_co_U900_rieng = False
        value = 'ERI_3G_' + cell_value
        return value
    def value_for_Site_ID_2G(self,value):
        return 'SRN_2G_' + value
    def value_for_Site_Name_2(self,cell_value):
        value = cell_value.replace('3G_','')
        return value
    
    def value_for_int_to_string (self,cell_value):
        value = int(cell_value)
        return value
    def value_for_Site_Name_1 (self,value):
        
        
        if self.is_U900_hay_U2100 == 'U900':
            self.obj.is_co_U2100_rieng = self.is_co_U2100_rieng
        elif self.is_U900_hay_U2100 == 'U2100':
            self.obj.is_co_U900_rieng = self.is_co_U900_rieng
        value = value.replace("3G_","")
        return value
    def value_for_active_3G(self,value):
        if self.created_or_update == 1 :#create
            return True
        
    def value_for_nha_san_xuat_2G(self,cell_value):
        return_value = super(Excel_3G, self).value_for_Cabinet(self,cell_value,name_ThietBi_attr= 'nha_san_xuat_2G')
        return  return_value
D4_DATE_ONLY_FORMAT_gachngang = '%d-%m-%Y'    
class Excel_to_2g (Excel_2_3g):
    fields_allow_empty_use_function = ['Site_ID_2G_Number','Site_type']
    backwards_sequence =['Site_ID_2G','Site_ID_2G_Number']
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'Database 2G'
    mapping_function_to_value_dict = {#'Ngay_Phat_Song_2G':'value_for_dateField'
                                      }
    manual_mapping_dict = {'Ngay_Phat_Song_2G': u'Phát sóng','Site_Name_1':u'Tên BTS','dia_chi_2G':u'Địa chỉ', 'BSC_2G':u'Tên BSC',\
                    'LAC_2G':u'LAC', 'Nha_Tram':u'Nhà trạm', 'Ma_Tram_DHTT':u'Mã trạm ĐHTT', 'Cell_ID_2G':u'CellId', \
                    'cau_hinh_2G':u'Cấu hình', 'nha_san_xuat_2G':u'Nhà SX', 'Site_ID_2G':u'Tên BTS','Long_2G':u'Tọa độ - Kinh độ','Lat_2G':u'Tọa độ - Vĩ độ'}
    
    
    def value_for_Ngay_Phat_Song_2G(self,value):
        print '@@@@@@@@@@@@ ngay phat song 2g',value,type(value)
        rs = datetime.datetime.strptime(value, D4_DATE_ONLY_FORMAT_gachngang)
        print rs
        return rs
    def value_for_Site_ID_2G_Number(self,value):
        value = self.obj.Cell_ID_2G
        if value:
            value = int(value)
            if value < 1000:
                value = str(value)[-2:]
            else:
                value = str(value)[-3:-1]
            return value
        else:
            return None
    def value_for_BSC_2G(self,value):
        if value:
            try:
                instance = Tram.objects.get(Site_Name_1 = value)
            except Tram.DoesNotExist:
                if self.added_foreinkey_types  > self.max_length_added_foreinkey_types:
                    raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
                instance = Tram(Site_Name_1 = value,Site_type = SiteType.objects.get(Name = u'Site 0 (RNC,BSC)'),ngay_gio_tao = timezone.now(),nguoi_tao = User.objects.get(username = u'rnoc2'))
                instance.save()
        
        if value:
            print '@@@@@@@@value BSC_2G',value
            try:
                instance = BSCRNC.objects.get(Name = value)
            except BSCRNC.DoesNotExist:
                instance = BSCRNC(Name = value, ngay_gio_tao = timezone.now(),nguoi_tao = User.objects.get(username = 'rnoc2'))
                self.added_foreinkey_types +=1
                if self.added_foreinkey_types  > self.max_length_added_foreinkey_types:
                    raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
                instance.save()
            return instance
        else:
            return None
    def value_for_Site_Name_1 (self,cell_value):
        value = cell_value.replace("2G_","")
        return value
    def value_for_Site_ID_2G(self,cell_value):
        self.obj.active_2G = True
        if self.created_or_update ==1:
            self.obj.nguoi_tao = User.objects.get(username='rnoc2')
            self.obj.ngay_gio_tao = timezone.now()
        if cell_value.startswith('2G_'):
            return None  # return none for not save to database this field
        else:
            cell_value = self.obj.nha_san_xuat_2G.Name[0:3].upper() + '_2G_' + cell_value
            return  cell_value
    def value_for_nha_san_xuat_2G(self,cell_value):
        return_value = super(Excel_to_2g, self).value_for_Cabinet(cell_value,name_ThietBi_attr= 'nha_san_xuat_2G')
        return  return_value    
    '''
    def value_for_nha_san_xuat_2G(self,cell_value):
        thietbi = ThietBi.objects.get_or_create(Name=cell_value)[0]
        self.added_foreinkey_types.add(thietbi)#set().add
        l = len(self.added_foreinkey_types)
        print "cabin**",l
        if l >self.max_length_added_foreinkey_types:
            raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
        self.obj.nha_san_xuat_2G=thietbi
        #self.obj.save()
        return None
    '''
class Excel_to_3g_location (Excel_2_3g):
    fields_allow_empty_use_function = ['Site_type']
    allow_create_one_instance_if_not_exit = False
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Site_ID_3G'
    worksheet_name = u'3G Site Location'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'Site_ID_3G':u'Site ID','dia_chi_3G':u'Location','Long_3G':u'Long','Lat_3G':u'Lat',}
    def value_for_Site_ID_3G(self,cell_value):
        value = 'ERI_3G_' + cell_value
        return value
class Excel_to_2g_config_SRAN (Excel_2_3g):
    fields_allow_empty_use_function = ['Site_type']
    begin_row=39
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'2G SRAN HCM Config'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'Site_Name_1':u'RSITE','TG_Text':u'TG','TRX_DEF':u'TRX DEF'}
    def value_for_TG_Text(self,value):
        self.obj.active_2G = True
        if self.created_or_update ==1:
            self.obj.nguoi_tao = User.objects.get(username='rnoc2')
            self.obj.ngay_gio_tao = timezone.now()
        rs = re.findall('RXOTG-(\d+)',value)
        if len(rs)==1:
            self.obj.TG = rs[0]
        elif len(rs)>1:
            self.obj.TG = rs[0]
            self.obj.TG_1800 = rs[1]
                
        return value
    def value_for_Site_Name_1 (self,cell_value):
        cell_value = cell_value.replace('2G_','')
        return cell_value
class Excel_NSM(Excel_2_3g):
    fields_allow_empty_use_function = ['Site_type']
    begin_row=1
    just_create_map_field = False
    auto_map = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'NSN Database'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_3G':'value_for_common_datefield','IUB_VLAN_ID':'value_for_common_VLAN_ID'}
    manual_mapping_dict = {'Site_Name_1':u'3G Site Name','Site_ID_3G':u'3G Site Name','Cabinet':u'Type',\
                    'Ngay_Phat_Song_3G':u'Ngày PS U900','RNC':u'RNC name','IUB_VLAN_ID':u'VLAN ID','IUB_DEFAULT_ROUTER':u'GW IP ',\
                    'IUB_HOST_IP':u'IP','MUB_SUBNET_PREFIX':u'Network IP','MUB_DEFAULT_ROUTER':u'TRS IP',\
                    'ntpServerIpAddressPrimary':u'NTP Primary IP','ntpServerIpAddressSecondary':u'NTP Secondary  IP'
                    }
    def value_for_Cabinet(self,cell_value):
        cell_value = 'NSM'
        return_value = super(Excel_NSM, self).value_for_Cabinet(cell_value)
        return  return_value
    def value_for_Site_Name_1 (self,cell_value):
        cell_value = cell_value.replace('3G_','')
        return cell_value
    def value_for_Site_ID_3G(self,cell_value):
        self.obj.active_3G = True
        if self.created_or_update ==1:
            self.obj.nguoi_tao = User.objects.get(username='rnoc2')
            self.obj.ngay_gio_tao = timezone.now()
        #cell_value = cell_value.replace('3G_','NSM_')
        cell_value = 'NSM_'+ cell_value
        return cell_value
    
class Excel_ALU(Excel_2_3g):
    fields_allow_empty_use_function = ['nguoi_tao','ngay_gio_tao','Site_type']
    begin_row=3
    just_create_map_field = False
    auto_map = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'Database_ALU'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_3G':'value_for_common_datefield','IUB_VLAN_ID':'value_for_common_VLAN_ID','MUB_VLAN_ID':'value_for_common_VLAN_ID'}
    manual_mapping_dict = {'Site_Name_1':u'Tên trạm (ALU)','Site_ID_3G':u'Tên trạm (ALU)','Cabinet':u'RNC',\
                    'RNC':u'RNC',
                    'IUB_VLAN_ID':u'Iub Vlan','IUB_SUBNET_PREFIX':u'Iub Subnet',
                    'IUB_DEFAULT_ROUTER':u'Iub Default Router','IUB_HOST_IP':u'Iub Host',
                    'MUB_VLAN_ID':u'Mub Vlan','MUB_SUBNET_PREFIX':u'Mub Subnet',\
                    'MUB_HOST_IP':u'Mub Host','MUB_DEFAULT_ROUTER':u'Mub Default Router',\
                   
                    }
    # bat dau dem column tu 0
    manual_mapping_dict = {'Site_Name_1':2,'Site_ID_3G':2,'Cabinet':8,\
                    'RNC':8,\
                    'IUB_VLAN_ID':11,'IUB_SUBNET_PREFIX':12,\
                    'IUB_DEFAULT_ROUTER':13,'IUB_HOST_IP':14,\
                    'MUB_VLAN_ID':15,'MUB_SUBNET_PREFIX':16,\
                    'MUB_HOST_IP':18,'MUB_DEFAULT_ROUTER':17,\
                   
                    }
    def value_for_Site_Name_1 (self,cell_value):
        cell_value = cell_value.replace('3G_','')
        return cell_value
    def value_for_Site_ID_3G(self,cell_value):
        self.obj.active_3G = True
        
        cell_value = 'ALU_'+ cell_value
        return cell_value
    def value_for_Cabinet(self,cell_value):
        cell_value = 'ALU'
        return_value = super(Excel_ALU, self).value_for_Cabinet(cell_value)
        return  return_value
class Excel_ALU_tuan(Excel_2_3g):
    fields_allow_empty_use_function = ['nguoi_tao','ngay_gio_tao','Cabinet','Site_type']
    begin_row=0
    just_create_map_field = False
    auto_map = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'Sheet1'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_3G':'value_for_common_datefield','IUB_VLAN_ID':'value_for_common_VLAN_ID','MUB_VLAN_ID':'value_for_common_VLAN_ID'}
    manual_mapping_dict = {'Site_Name_1':u'NodeB Name','Site_ID_3G':u'NodeB Name',\
                    'RNC':u'RNC Nam','IUB_DEFAULT_ROUTER':u'Iub Default GW NodeB','IUB_HOST_IP':u'Iub NodeB Ip add',
                    'IUB_VLAN_ID':u'Iub Vlan','IUB_SUBNET_PREFIX':u'Iub Default GW NodeB',
                    'MUB_VLAN_ID':u'Mub Vlan','MUB_SUBNET_PREFIX':u'Mub Default GW NodeB',\
                    'MUB_HOST_IP':u'Mub NodeB Ip add','MUB_DEFAULT_ROUTER':u'Mub Default GW NodeB',\
                   
                    }
    
    def value_for_Site_Name_1 (self,cell_value):
        cell_value = cell_value.replace('3G_','')
        return cell_value
    def value_for_Site_ID_3G(self,cell_value):
        self.obj.active_3G = True
        cell_value = 'ALU_'+ cell_value
        return cell_value
    def value_for_Cabinet(self,cell_value):
        cell_value = 'ALU'
        return_value = super(Excel_ALU_tuan, self).value_for_Cabinet(cell_value)
        return  return_value

class Excel_4G(Excel_2_3g):
    fields_allow_empty_use_function = ['Site_type']
    #begin_row=3
    just_create_map_field = False
    auto_map = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'Ericsson 4G'
    mapping_function_to_value_dict ={'eNodeB_ID_DEC':'value_for_common_VLAN_ID'}
    manual_mapping_dict = {'eNodeB_Name':u'eNodeB_Name','Site_Name_1':u'eNodeB_Name','eNodeB_ID_DEC':u'eNodeB_ ID(DEC)','eNodeB_Type':u'eNodeB_Type',     }

    def value_for_Site_Name_1 (self,cell_value):
        #results = re.findall('4G_(.*?_', cell_value)
        cell_value = cell_value.replace('4G_','')
        return cell_value
    def value_for_eNodeB_Type(self,cell_value):
        self.obj.active_4G = True
        if self.created_or_update ==1:
            self.obj.nguoi_tao = User.objects.get(username='rnoc2')
            self.obj.ngay_gio_tao = timezone.now()
        return_value = super(Excel_4G, self).value_for_Cabinet(cell_value,name_ThietBi_attr = 'eNodeB_Type')
        return  return_value    
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
def create_user():
    workbook = xlrd.open_workbook(MEDIA_ROOT+ '/document/DanhSachEmail.xls')
    worksheet = workbook.sheet_by_name(u'Sheet3')
    num_rows = worksheet.nrows - 1
    curr_row_number = -1
    while curr_row_number < num_rows:
        curr_row_number += 1
        username =   read_excel_cell(worksheet, curr_row_number, 6)
        sdt  =   read_excel_cell(worksheet, curr_row_number, 5)
        groupname =   read_excel_cell(worksheet, curr_row_number, 7)
        ex = User.objects.get_or_create (username = username)
        user = ex[0]
        if ex[1]:#Neu user = New                                
            user.set_password(username)
            user.save()                          
        group = Group.objects.get_or_create (name = groupname)[0]
        group.user_set.add(user)
        ex = UserProfile.objects.get_or_create(user =user)
        if ex[1]:
            profile = ex[0]
            profile.so_dien_thoai=sdt
            profile.color_code = "#%06x" % random.randint(0, 0xFFFFFF)
            ca_truc = CaTruc.objects.latest('id')
            profile.ca_truc = ca_truc
            profile.save()
    more_users = ['ductu','rnoc2']
    for username in more_users:
        ex = User.objects.get_or_create (username = username)
        user = ex[0]
        if ex[1]:#Neu user = New                                
            user.set_password(username)
            user.save()  
        ex = UserProfile.objects.get_or_create(user =user)
        if ex[1]:
            profile = ex[0]
            profile.color_code = "#%06x" % random.randint(0, 0xFFFFFF)
            ca_truc = CaTruc.objects.latest('id')
            profile.ca_truc = ca_truc
            profile.save()
 

def grant_permission_to_group():
    content_type = ContentType.objects.get_for_model(Mll)
    name_and_codes = [('d4_create_truc_ca_permission','Can truc ca'),('can add on modal code','can add on modal')]
    truc_ca_group = Group.objects.get_or_create (name = 'truc_ca')[0]
    for x in name_and_codes:
        permission = Permission.objects.get_or_create(codename=x[0],
                                           name=x[1],
                                           content_type=content_type)[0]
    
        truc_ca_group.permissions.add(permission)
def grant_permission_admin():
    content_type = ContentType.objects.get_for_model(Mll)
    code_and_names= [('d4_admin','Can admin')]
    user = User.objects.get (
                                            username = 'rnoc2',
                                            )
    for x in code_and_names:
        permission = Permission.objects.get_or_create(codename=x[0],
                                           name=x[1],
                                           content_type=content_type)[0]
    
        user.user_permissions.add(permission)
        
def check_permission_of_group():
    for username in ['rnoc2','lucvk']:
        user = User.objects.get_or_create (
                                            username = username,
                                            )[0]
        permission = Permission.objects.get(codename='d4_create_truc_ca_permission')
        print 'username,user.has_perm',username,user.has_perm('drivingtest.d4_create_truc_ca_permission')

def import_database_4_cai_new (runlists,workbook = None):
        DB3G_SHEETS = ['Excel_3G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location','Excel_4G','ImportRNC']
        if workbook:#must file upload ,workbook = workbook_upload
            for class_func_name in runlists:
                running_class = eval(class_func_name)
                running_class(workbook = workbook)
        else:
            if 'ALL' in runlists:
                runlists.remove('ALL')
                runlists.extend(DB3G_SHEETS)
                runlists = set(runlists)
            runlists_reorder = []
            for count,x in enumerate(runlists):
                if x in DB3G_SHEETS:
                    runlists_reorder.insert(count,x)
                else:
                    runlists_reorder.append(x)
            runlists = runlists_reorder
  
            is_already_read_db3g_file  = False           
            for class_func_name in runlists:
                print 'dang chay class_func_name',class_func_name
                if class_func_name in DB3G_SHEETS:
                    if not is_already_read_db3g_file:
                        path = MEDIA_ROOT+ u'/document/Ericsson_Database_Ver_160.xlsx'
                elif class_func_name =='Excel_NSM':
                    path = MEDIA_ROOT+ '/document/NSN_Database_version_4.xlsx'
                elif class_func_name =='Excel_ALU':
                    path = MEDIA_ROOT+ '/document/Database_ALU lot 1-2 -3 den NGAY  5-8-2015 .xls'
                elif class_func_name =='Excel_ALU_tuan':
                    path = MEDIA_ROOT+ '/document/alu_tuan.xlsx'
                elif class_func_name =='ExcelImportDoiTac_ungcuu':
                    path = MEDIA_ROOT+ '/document/danh sach nv xuong quan ly dia ban.xls'
                elif class_func_name =='ImportTinh':
                    path = MEDIA_ROOT+ '/document/danh sach nv xuong quan ly dia ban.xls'
                elif class_func_name =='ImportTinh_diaban':
                    path = MEDIA_ROOT+ '/document/To Ung cuu_New.tu.xls'
                elif class_func_name =='Import_RNC_Tram':
                    path = MEDIA_ROOT+ '/document/Table_BSCRNC.xls'
                elif class_func_name =='ExcelChung':
                    path = '/home/ductu/Documents/Downloads/Table_Tram.xls'
                
                else: 
                    rs = re.match('^ExcelImport(.*?)$',class_func_name)
                    try:
                        classname = rs.group(1)
                        path = MEDIA_ROOT+ '/document/Table_%s.xls'%classname
                    except AttributeError:
                        raise ValueError('khong ton tai file name nao nhu the trong thu muc media')
                if class_func_name in DB3G_SHEETS:
                    if not is_already_read_db3g_file:     
                        workbook= xlrd.open_workbook(path)
                        is_already_read_db3g_file = True
                else:
                    workbook= xlrd.open_workbook(path)
                print 'dang chay class_func_name',class_func_name
                running_class = eval(class_func_name)
                running_class(workbook = workbook)
            
              
from django.template import Context,Template 

def tao_script(instance_site,ntpServerIpAddressPrimary = '',ntpServerIpAddressSecondary = '',\
                         ntpServerIpAddress1="",ntpServerIpAddress2=""):
    if (ntpServerIpAddressPrimary=='' or ntpServerIpAddress1==""):
        return None
    print 'hello, wellcome to download'
    Cabinet = instance_site.Cabinet
    is_luu_o_cung_moi_file_output_rieng = True
    save_type = 'temporary_achive_output_script'#or save_type = 'disk_achive_output_script',khong xai, 
    #chi de hieu rang achive object co the ghi len o cung hoac len file tam
    now = datetime.datetime.now()
    Site_ID_3G= instance_site.Site_ID_3G
    instance_site.now = now
    return_file_lists = []
    achive_path=None
    instance_site.ntpServerIpAddressPrimary = ntpServerIpAddressPrimary
    instance_site.ntpServerIpAddressSecondary = ntpServerIpAddressSecondary
    instance_site.ntpServerIpAddress1 = ntpServerIpAddress1
    instance_site.ntpServerIpAddress2 = ntpServerIpAddress2
    template_files =[]
    if "RBS6" in Cabinet.Name:
        type_rbs = "6000"
        path_template_directory = MEDIA_ROOT+ '/document/template_script/6000/'
    elif "RBS3" in Cabinet.Name:
        path_template_directory = MEDIA_ROOT+ '/document/template_script/3000/'
        type_rbs = "3000"
    for root, dirs, files in os.walk(path_template_directory):
        for file in files:
            template_files.append(file)
    for counts,template_file in enumerate(template_files):
        path_to_1_template_file =  path_template_directory + template_file
        template = read_file_from_disk (path_to_1_template_file)
        t = Template(template)
        c = Context({'site3g':instance_site})
        output = t.render(c)
        fname = Site_ID_3G + '_' + template_file
        folder_name = '5484692'
        new_directory_path = MEDIA_ROOT+ '/for_user_download_folder/' + folder_name + '/'
        if save_type == 'save_to_disk_3_file':# chi luu o cung trong giao dien console nay
            if not os.path.exists(new_directory_path): os.makedirs(new_directory_path)
            filepath = new_directory_path  + fname
            return_file_lists.append(folder_name + '/' +  fname)
            save_file_to_disk(filepath,output,1)
        else:
            if counts==0:
                if save_type =='disk_achive_output_script':
                    achive_path = new_directory_path + Site_ID_3G +'.zip'#achive_path den o cung
                elif  save_type == 'temporary_achive_output_script':# dang dung
                    achive_path = tempfile.TemporaryFile() # this time achive_path is template object file,achive_path la 1 object template
                archive_object = zipfile.ZipFile(achive_path, 'w', zipfile.ZIP_DEFLATED)# tao ra 1 object achive de write len path
            if is_luu_o_cung_moi_file_output_rieng:#luu o cung 3 file rieng re, de doi chieu voi download o giao dien web
                if not os.path.exists(new_directory_path):
                    os.makedirs(new_directory_path)
                filepath = new_directory_path  + fname
                save_file_to_disk(filepath,output,1)
            archive_object.writestr(fname, output)#write to object theo kieu data voi file name la fname
    return return_file_lists, achive_path, type_rbs # achive_path become tempt zip file

    #grant_permission_admin()

def create_ca_truc():
    for ca_truc_name in ['Moto','Alu','Huawei','Sran']:
        ex = CaTruc.objects.get_or_create(Name=ca_truc_name)
        instance = ex[0]
        if ex[1]:
            instance.is_duoc_tao_truoc = True
            #instance.nguoi_tao = User.objects.get(username = "rnoc2")
            #instance.ngay_tao = timezone.now()
            instance.save()
def create_type_site():
    for x in ['Site 0 (RNC,BSC)',u'Site thường']:
        try:
            instance = SiteType.objects.get(Name = x)
        except SiteType.DoesNotExist:
            instance = SiteType(Name=x)
            instance.save()
                        

def delete_edithistory_table3g():
    EditHistory.objects.filter(modal_name='Tram').delete()
def init_rnoc():
    
    create_ca_truc()#1
    create_user()#2
    import_database_4_cai_new(['ExcelImportTrangThai'])#3
    import_database_4_cai_new(['ExcelImportSuCo'])#4
    import_database_4_cai_new(['ExcelImportDuAn'])#5
    import_database_4_cai_new(['ExcelImportNguyenNhan'])#6
    import_database_4_cai_new(['ExcelImportThietBi'])#7
    import_database_4_cai_new(['ExcelImportFaultLibrary'])#8
    import_database_4_cai_new(['ExcelImportThaoTacLienQuan'])#9
    
    import_database_4_cai_new(['ExcelImportLenh'])#10
    import_database_4_cai_new(['ExcelImportDoiTac'])#11
    import_database_4_cai_new(['ExcelImportDoiTac_ungcuu'] )
    import_database_4_cai_new(['ImportTinh'] )
    import_database_4_cai_new(['ImportTinh_diaban'] )
    create_type_site()
    import_database_4_cai_new(['Import_RNC_Tram'] )
    
if __name__ == '__main__':
    #import_database_4_cai_new(['ExcelImportLenh'])#10
    #import_database_4_cai_new(['ExcelImportLenh'])#10
    #init_rnoc()
    #create_ca_truc()#1
    #create_user()#2
    #import_database_4_cai_new(['ExcelImportTrangThai'])#3
    #import_database_4_cai_new(['ExcelImportSuCo'])
    #import_database_4_cai_new(['ExcelImportDuAn'])
    #import_database_4_cai_new(['ExcelImportNguyenNhan'])
    #import_database_4_cai_new(['ExcelImportThietBi'])
    #import_database_4_cai_new(['ExcelImportFaultLibrary'])
    #import_database_4_cai_new(['ExcelImportThaoTacLienQuan'])
    #import_database_4_cai_new(['ExcelImportLenh'])
    #import_database_4_cai_new(['ExcelImportDoiTac'])
    
    #Chua sai
    #grant_permission_admin()
    #import_doi_tac()
    #grant_permission_to_group()
    #check_permission_of_group()
    #delete_edithistory_table3g()
    
    #'Excel_3G','Excel_4G',
    #import_database_4_cai_new(['Excel_4G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location','ImportRNC','Excel_NSM','Excel_ALU_tuan',] )
    #import_database_4_cai_new(['Excel_NSM','Excel_ALU_tuan',] )

    #import_database_4_cai_new(['Excel_to_3g_location'] )
    
    #path = MEDIA_ROOT+ '/document/db2g.xls'
    #workbook= xlrd.open_workbook(path)
    #import_database_4_cai_new(['Excel_to_2g'] ,workbook=workbook)
    
    import_database_4_cai_new(['ExcelImportDoiTac_ungcuu'] )
    #import_database_4_cai_new(['ImportTinh'] )
    #import_database_4_cai_new(['ImportTinh_diaban'] )
    #import_database_4_cai_new(['ImportRNC'] )
    #import_database_4_cai_new(['Import_RNC_Tram'] )
    #import_database_4_cai_new(['Excel_to_2g'] )
    #create_type_site()