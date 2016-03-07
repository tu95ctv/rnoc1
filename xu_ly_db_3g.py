# -*- coding: utf-8 -*- 
import os
import xlrd,datetime
from django.core.exceptions import MultipleObjectsReturned
from unidecode import unidecode
from random import randint
import tempfile
import zipfile
from collections import OrderedDict
import re
import random

SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from rnoc.forms import D4_DATETIME_FORMAT
from rnoc.models import Tram, Mll, DoiTac, Nguyennhan,\
    CaTruc, UserProfile, TrangThai, DuAn, ThaoTacLienQuan, ThietBi,\
    EditHistory

#dict_attr = OrderedDict()
dict_attr ={}

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


        
def read_excel_cell(worksheet,curr_row_number,curr_col):
    try:
        attr_name = dict_attr[curr_col]
    except:
        attr_name =''
    cell_value = worksheet.cell_value(curr_row_number, curr_col)
    print  attr_name,'curr_col curr_row_number ,value(co hoac khong)',curr_col, curr_row_number,cell_value
    return cell_value

class Excel_2_3g(object):
    allow_create_one_instance_if_not_exit = True
    fields_allow_empty_use_function =[]# nhung cai field ma excel = rong van dung fucntion de gan gia tri cho field, vi du nhu field namekhong dau
    is_import_from_exported_file = False
    #added_foreinkey_types = set() # cai nay dung de tinh so luong du an, hoac thietbi, duoc add, neu nhieu qua thi stop
    added_foreinkey_types = 0 # cai nay dung de tinh so luong du an, hoac thietbi, duoc add, neu nhieu qua thi stop
    max_length_added_foreinkey_types = 30
    backwards_sequence =[]
    many2manyFields = []
    update_or_create_main_item = ''#Site_ID_3G
    worksheet_name = u''
    begin_row=0
    manual_mapping_dict = {}
    mapping_function_to_value_dict = {}
    auto_map = True
    model = Tram
    created_number =0
    update_number = 0
    just_create_map_field = False
    def __init__(self,workbook=None,is_import_from_exported_file=None):
        if is_import_from_exported_file:
            self.is_import_from_exported_file = True
            self.worksheet_name = u'Sheet 1'
        self.workbook = workbook
        self.read_excel()
        self.excel_dict = self.define_attr_dict() # excel_dict la ten cua cac cot lay trong file excel ra
        print 'excel_dict',self.excel_dict
        self.base_fields = {}
        self.missing_fields =[]
        print [f.name for f in self.model._meta.fields]
        if self.is_import_from_exported_file:
            for f in  self.model._meta.fields:
                if f.verbose_name in self.excel_dict :
                    if f.name =='id':
                        continue
                    else:
                        self.base_fields[f.name] = self.excel_dict[f.verbose_name]
                else:
                    self.missing_fields.append(f.name)
            print '#####self.base_fields',self.base_fields
            print '######self.missing_fields.',self.missing_fields
        else:
            self.fieldnames = [f.name for f in self.model._meta.fields if f.name!='id' ]
            if self.many2manyFields: # self.ModelClass._meta.many_to_many
                for x in self.many2manyFields:
                    if x not in self.fieldnames:
                        self.fieldnames.append(x)
            for fname in self.fieldnames:
                fname_lower = fname.lower()
                if self.auto_map and (fname_lower in self.excel_dict):
                    self.base_fields[fname] = self.excel_dict[fname_lower]
                else: # 1 so attribute khong nam trong file excel
                    if fname in self.manual_mapping_dict: #manual_mapping_dict la manual , do minh tu tao anh xa fieldname voi ten cot cua file excel
                        fieldname_in_excel = self.manual_mapping_dict[fname]
                        if isinstance(fieldname_in_excel, int):
                            self.base_fields.update({fname:fieldname_in_excel})
                        else:
                            fieldname_in_excel =  unidecode(fieldname_in_excel).lower().replace(' ','_') # file name format
                            if fieldname_in_excel in self.excel_dict:
                                self.base_fields[fname]= self.excel_dict[fieldname_in_excel] #= so thu tu cua column chua field do, vi du 5
                            else: # thieu cot nay hoac da bi doi ten                        
                                raise ValueError('trong file excel thieu cot %s '%fieldname_in_excel)
                    else:
                        self.missing_fields.append(fname)
            print 'self.base_fields',self.base_fields
        if self.just_create_map_field:#for test
            return None
        self.loop_excel_and_insertdb()
    def convert_basefield_to_list_of_tuple(self):
        if self.backwards_sequence:
            sequence = [x for x in self.base_fields.iterkeys()]
            for x in self.backwards_sequence:
                if x in sequence:
                    sequence.remove(x)
                sequence.append(x)
            self.odering_base_columns_list_tuple = [(x, self.base_fields[x]) for x in sequence]
        else:
            self.odering_base_columns_list_tuple = [(k,v) for k, v in self.base_fields.iteritems()]
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
                atrrname = unidecode(atrrname).lower().replace(" ","_")
            else:
                atrrname = atrrname.replace("_"," ")
            dict_attrName_columnNumber_excel_not_underscore[atrrname ]=   curr_col
            curr_col +=1
        return dict_attrName_columnNumber_excel_not_underscore
    
    def loop_excel_and_insertdb(self):
        curr_row_number = self.begin_row
        main_field_index_excel_column = self.base_fields.pop(self.update_or_create_main_item) #index of main fields
        self.convert_basefield_to_list_of_tuple()
        while curr_row_number < self.num_rows:
            curr_row_number += 1
            to_value_function = self.get_function(self.update_or_create_main_item) # function for main field
            value = read_excel_cell(self.worksheet, curr_row_number,main_field_index_excel_column)
            if to_value_function:
                value = to_value_function(value)
            karg = {self.update_or_create_main_item:value}
            execute = self.model.objects.filter(**karg)
            if execute: # co db_row nay roi, update thoi
                self.created_or_update = 0
                for self.obj in execute:# loop va gan gia tri vao self.obj
                    self.update_field_for_obj(curr_row_number)
                    self.update_number +=1
            else: #tao moi
                if self.allow_create_one_instance_if_not_exit:
                    self.created_or_update = 1   
                    self.obj = self.model(**karg)
                    self.update_field_for_obj(curr_row_number)
                    self.created_number +=1
                else:
                    continue
    def update_field_for_obj(self,curr_row_number):
        for field_tuple in self.odering_base_columns_list_tuple:
            field = field_tuple[0]
            value =  read_excel_cell(self.worksheet, curr_row_number,field_tuple[1])
            if value=='' or value =="null"or value ==u'—':
                value = None
            if  value or field in self.fields_allow_empty_use_function:
                to_value_function = self.get_function(field)
                if to_value_function:
                    value = to_value_function(value)
                if value!=None:#to_value_function chu dong tra ve None neu khong muon luu field
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
    def save_to_db(self,updated_values):
        for key, value in updated_values.iteritems():
                setattr(self.obj, key, value)
        self.obj.save()
    def value_for_stylecss_name(self,cell_value):
        return  unidecode(self.obj.Name).replace(' ','-')
    def value_for_color_code(self,cell_value):#boolean
        if cell_value:
            return cell_value
        else:
            return "#%06x" % random.randint(0, 0xFFFFFF)
    def value_for_common_datefield(self,cell_value):
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(cell_value)) # delta du lieu datetime
            #get_col2 = str(date + get_)[:10] # convert date to string theo dang nao do
            #value = get_col2 # moi them vo
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
            thietbi.save()
        setattr(self.obj,name_ThietBi_attr,thietbi)
        return None
    def value_for_common_VLAN_ID (self,cell_value):
        value = int(cell_value)
        return value   
class ExcelChung (Excel_2_3g):
    #backwards_sequence =['Site_ID_2G',]#de lay gia tri nha_san_xuat_2G truoc
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
class ExcelImportDoiTac (Excel_2_3g):
    fields_allow_empty_use_function = ['Full_name_khong_dau']
    backwards_sequence =['Full_name_khong_dau',]#de lay gia tri nha_san_xuat_2G truoc
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Full_name'
    worksheet_name = u''
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {}
    model = DoiTac
    def value_for_Full_name_khong_dau(self,cell_value):
        return unidecode(self.obj.Full_name)
class ExcelImportTrangThai (Excel_2_3g):
    fields_allow_empty_use_function = ['stylecss_name','color_code','is_cap_nhap_gio_tot']
    backwards_sequence =['stylecss_name',]#de lay gia tri nha_san_xuat_2G truoc
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Name'
    worksheet_name = u''
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {}
    model = TrangThai
    def value_for_is_cap_nhap_gio_tot(self,cell_value):#boolean not null allowed
        #if cell_value ==u'✔':
            #return True
        if cell_value ==u'✘' or cell_value==None:
            return False
        else:
            return True
    
        
class ExcelImportNguyennhan(Excel_2_3g):
    fields_allow_empty_use_function = ['stylecss_name','color_code','ngay_gio_tao']
    backwards_sequence =['']#de lay gia tri nha_san_xuat_2G truoc #'stylecss_name',
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Name'
    worksheet_name = u''
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {}
    model = Nguyennhan
 
    def value_for_ngay_gio_tao(self,cell_value):
        if cell_value:
            cell_value = re.sub("$'", "", cell_value)
            cell_value = re.sub(' $', '', cell_value)
            d = datetime.datetime.strptime(str(cell_value), D4_DATETIME_FORMAT)
            return d
        else:
            return datetime.datetime.now()
class Excel_3G(Excel_2_3g):
    many2manyFields = ['du_an']
    just_create_map_field = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'Ericsson 3G'
    backwards_sequence =['du_an']
    manual_mapping_dict = {'Project_Text':5,'du_an':5,'License_60W_Power':u'60W Power License','Cell_1_Site_remote':u'Cell 1 (carrier 1)', \
                    'Cell_2_Site_remote':u'Cell 2 (Carrier 1)', 'Cell_3_Site_remote':u'Cell 3 (Carrier 1)',\
                     'Cell_4_Site_remote':u'Cell 4 (Carrier 2)', 'Cell_5_Site_remote':u'Cell 5 (Carrier 2)', 'Cell_6_Site_remote':u'Cell 6 (Carrier 2)', \
                     'Cell_7_Site_remote':u'Cell 7 (remote/U900/3 carrier)', 'Cell_8_Site_remote':u'Cell 8 (remote/U900/3 carrier)', 'Cell_9_Site_remote':u'Cell 9 (remote/U900/3 carrier)',\
                     'Cell_K_U900_PSI':u'Cell K (U900 PSI)'
                     }
    mapping_function_to_value_dict = {'Ngay_Phat_Song_2G':'value_for_dateField','Ngay_Phat_Song_3G':'value_for_dateField',\
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
            du_an.save()
        self.obj.du_an.add(du_an)
        return None
    
    
    def value_for_Site_ID_3G(self,cell_value):
        value = 'ERI_3G_' + cell_value
        return value
    def value_for_Site_ID_2G(self,value):
        return 'SRN_2G_' + value
    def value_for_Site_Name_2(self,cell_value):
        value = cell_value.replace('3G_','')
        return value
    def value_for_dateField(self,cell_value):
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(cell_value)) # delte du lieu datetime
            get_col2 = str(date + get_)[:10] # convert date to string theo dang nao do
            value = get_col2 # moi them vo
            return value
        except:
            return None
    def value_for_int_to_string (self,cell_value):
        value = int(cell_value)
        return value
    def value_for_Site_Name_1 (self,value):
        value = value.replace("3G_","")
        return value
    def value_for_nha_san_xuat_2G(self,cell_value):
        return_value = super(Excel_3G, self).value_for_Cabinet(self,cell_value,name_ThietBi_attr= 'nha_san_xuat_2G')
        return  return_value
    
class Excel_to_2g (Excel_2_3g):
    backwards_sequence =['Site_ID_2G',]
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'Database 2G'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'Site_Name_1':u'Tên BTS','dia_chi_2G':u'Địa chỉ', 'BSC_2G':u'Tên BSC',\
                    'LAC_2G':u'LAC', 'Nha_Tram':u'Nhà trạm', 'Ma_Tram_DHTT':u'Mã trạm ĐHTT', 'Cell_ID_2G':u'CellId', \
                    'cau_hinh_2G':u'Cấu hình', 'nha_san_xuat_2G':u'Nhà SX', 'Site_ID_2G':u'Tên BTS',}
    def value_for_Site_Name_1 (self,cell_value):
        value = cell_value.replace("2G_","")
        return value
    def value_for_Site_ID_2G(self,cell_value):
        
        self.obj.save()
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
    allow_create_one_instance_if_not_exit = False
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Site_ID_3G'
    worksheet_name = u'3G Site Location'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'Site_ID_3G':u'Site ID','dia_chi_3G':u'Location'}
    def value_for_Site_ID_3G(self,cell_value):
        value = 'ERI_3G_' + cell_value
        return value
class Excel_to_2g_config_SRAN (Excel_2_3g):
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'Site_Name_1'
    worksheet_name = u'2G SRAN HCM Config'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'Site_Name_1':u'RSITE','TG':u'TG','TRX_DEF':u'TRX DEF'}
    def value_for_Site_Name_1 (self,cell_value):
        cell_value = cell_value.replace('2G_','')
        return cell_value
class Excel_NSM(Excel_2_3g):
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
        #cell_value = cell_value.replace('3G_','NSM_')
        cell_value = 'NSM_'+ cell_value
        return cell_value
    
class Excel_ALU(Excel_2_3g):
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
        cell_value = 'ALU_'+ cell_value
        return cell_value
    def value_for_Cabinet(self,cell_value):
        cell_value = 'ALU'
        return_value = super(Excel_ALU, self).value_for_Cabinet(cell_value)
        return  return_value

class Excel_4G(Excel_2_3g):
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
        user = User.objects.get_or_create (
                                        username = username
                                        )[0]
        user.set_password(username)
        user.save()                          
        group = Group.objects.get_or_create (name = groupname)[0]
        group.user_set.add(user)
        profile = UserProfile.objects.get_or_create(user =user)[0]
        profile.so_dien_thoai=sdt
        profile.color_code = "#%06x" % random.randint(0, 0xFFFFFF)
        ca_truc = CaTruc.objects.latest('id')
        profile.ca_truc = ca_truc
        profile.save()
def create_nguyen_nhan():
    nguyennhans= [u'MLL',u"Mất điện",u"Lỗi TD VTT",u"Mất cell",u"Mất 3 cell",u"Mất cell site remote",]
    for name in nguyennhans:
        nn = Nguyennhan.objects.get_or_create (
                                            Name = name,
                                            )[0]
        #nn.Name_khong_dau = unidecode(name)
        nn.save()
def create_thiet_bi():
    thiet_bis=  [u'ALU',u'NSM',u'MOTO',u'2GSRAN',u'RBS3206M',u'RBS3418',u'RBS6601W',u'RBS6601W',u'RBS6601W-Dual',u'RBS6202W',u'2G&3G']
    for name in thiet_bis:
        nn = ThietBi.objects.get_or_create (
                                            Name = name,
                                            )[0]
        nn.save()     
def import_doi_tac ():
    path = MEDIA_ROOT+ '/document/SO DT- MAIL CA NHAN - MAIL TO.xls'
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(u'main')
    num_rows = worksheet.nrows - 1
    curr_row_number = -1
    while curr_row_number < num_rows:
        curr_row_number += 1
        try:
            cellstt = read_excel_cell(worksheet, curr_row_number, 0)
            stt =   int(cellstt)
        except:
            continue
        Full_name = read_excel_cell(worksheet, curr_row_number, 1)
        Don_vi  = read_excel_cell(worksheet, curr_row_number, 4 )
        So_dien_thoai  =  read_excel_cell(worksheet, curr_row_number, 6)
        Nam_sinh  =  read_excel_cell(worksheet, curr_row_number,3 )
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(Nam_sinh))
            string_date_value = str(date + get_)[:10]# 
            d = datetime.datetime.strptime(string_date_value, '%Y-%m-%d') #date_time type
            Nam_sinh = d.strftime('%d/%m/%Y') # convert to string, again
        except:
            pass
        dia_chi_email = read_excel_cell(worksheet, curr_row_number, 5)
        try:
            doi_tac = DoiTac.objects.get_or_create (
                                        Full_name = Full_name,
                                        )[0]
        except MultipleObjectsReturned:
            doi_tac = DoiTac.objects.filter (
                                        Full_name = Full_name,)[0]
        doi_tac.Full_name_khong_dau = unidecode (Full_name)
        doi_tac.Don_vi  = Don_vi.replace('-',' ')
        doi_tac.So_dien_thoai  =  So_dien_thoai
        doi_tac.Nam_sinh  =  Nam_sinh
        doi_tac.dia_chi_email = dia_chi_email
        doi_tac.save()
def grant_permission_to_group():
    content_type = ContentType.objects.get_for_model(Mll)
    name_and_codes = [('d4_create_truc_ca_permission','Can truc ca'),('can add on modal code','can add on modal')]
    truc_ca_group = Group.objects.get_or_create (name = 'truc_ca')[0]
    for x in name_and_codes:
        permission = Permission.objects.get_or_create(codename=x[0],
                                           name=x[1],
                                           content_type=content_type)[0]
    
        truc_ca_group.permissions.add(permission)
def check_permission_of_group():
    for username in ['tund','lucvk']:
        user = User.objects.get_or_create (
                                            username = username,
                                            )[0]
        permission = Permission.objects.get(codename='d4_create_truc_ca_permission')
        print 'username,user.has_perm',username,user.has_perm('drivingtest.d4_create_truc_ca_permission')

def import_database_4_cai_new (runlists,workbook = None,is_available_file= True,is_import_from_exported_file=None):
    if is_import_from_exported_file=='yes':
        for class_func_name in runlists:
            if workbook:
                pass
            else:
                if class_func_name =='ExcelChung':
                    path = '/home/ductu/Documents/Downloads/Table_Tram.xls'
                else: 
                    rs = re.match('^ExcelImport(.*?)$',class_func_name)
                    classname = rs.group(1)
                    path = '/home/ductu/Documents/Downloads/Table_%s.xls'%classname
                    print 'path',path
                workbook= xlrd.open_workbook(path)
            running_class = eval(class_func_name)
            running_class(workbook = workbook,is_import_from_exported_file=is_import_from_exported_file)
    else:
        all_db3gfiles = ['Excel_3G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location','Excel_4G']
        if not is_available_file:#must file upload ,workbook = workbook_upload
            if 'ALL' in runlists:
                for class_func_name in all_db3gfiles:
                    running_class = eval(class_func_name)
                    running_class(workbook = workbook,is_import_from_exported_file=is_import_from_exported_file)
                    if class_func_name in runlists:
                        runlists.remove(class_func_name)
                runlists.remove('ALL')
            #just remain alu,nsm, when alu,nsm,E in 1 file
            for class_func_name in runlists:
                running_class = eval(class_func_name)
                running_class(workbook = workbook,is_import_from_exported_file=is_import_from_exported_file)
        else: # get available file from disk           
            if 'ALL' in runlists:
                path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_149.xlsx'
                workbook= xlrd.open_workbook(path) # tranh truong hop mo file nhieu lan
                for class_func_name in all_db3gfiles:
                    running_class = eval(class_func_name)
                    running_class(workbook = workbook,is_import_from_exported_file=is_import_from_exported_file)
                    if class_func_name in runlists:
                        runlists.remove(class_func_name)
                runlists.remove('ALL')
            
            ericsson_lists = []
            for x in runlists:
                if x in all_db3gfiles:
                    ericsson_lists.append(x)
                    runlists.remove(x)
            if ericsson_lists:
                #path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_134.xlsx'
                path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_149.xlsx'
                workbook= xlrd.open_workbook(path)
                for class_func_name in ericsson_lists:
                    running_class = eval(class_func_name)
                    running_class(workbook = workbook,is_import_from_exported_file=is_import_from_exported_file)             
            for class_func_name in runlists:
                if class_func_name =='Excel_NSM':
                    path = MEDIA_ROOT+ '/document/NSN_Database_version_4.xlsx'
                elif class_func_name =='Excel_ALU':
                    path = MEDIA_ROOT+ '/document/Database_ALU lot 1-2 -3 den NGAY  5-8-2015 .xls'
                elif class_func_name =='ExcelChung':
                    path = '/home/ductu/Documents/Downloads/Table_Tram.xls'
                workbook= xlrd.open_workbook(path)
                running_class = eval(class_func_name)
                running_class(workbook = workbook,is_import_from_exported_file=is_import_from_exported_file)
            
                  
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

def import_TrangThai():
    path = MEDIA_ROOT+ '/document/TrangThai.xls'
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(u'Sheet3')
    num_rows = worksheet.nrows - 1
    curr_row_number = -1
    while curr_row_number < num_rows:
        curr_row_number += 1
        Name_trangthai = read_excel_cell(worksheet, curr_row_number, 1)
        TrangThai.objects.get_or_create(Name = Name_trangthai)
class ThaoTac(Excel_2_3g):
    model=ThaoTacLienQuan
    worksheet_name = u'Sheet3'
    begin_row=0
    update_or_create_main_item = 'name'
    #manual_mapping_dict = {'Project_Text':5,'du_an':5,'License_60W_Power':u'60W Power License'}
def import_thao_tac():
    path = MEDIA_ROOT+ '/document/thaotaclienquan.xls'
    workbook= xlrd.open_workbook(path)
    ThaoTac(workbook)
def create_ca_truc():
    for ca_truc_name in ['Moto','Alu','Huawei','Sran']:
        instance = CaTruc.objects.get_or_create(Name=ca_truc_name)[0]
        instance.save()
import shutil
def remove_folder(path):
    shutil.rmtree(path)
def delete_edithistory_table3g():
    EditHistory.objects.filter(modal_name='Tram').delete()
if __name__ == '__main__':
    #import_TrangThai()
    #create_nguyen_nhan()
    import_thao_tac()
    '''
    create_ca_truc()
    create_user()
    grant_permission_to_group()
    #check_permission_of_group()
    import_doi_tac()
    import_TrangThai()
    import_thao_tac()
    create_nguyen_nhan()
    create_thiet_bi()
    '''
    #delete_edithistory_table3g()
    #import_database_4_cai_new(['Excel_3G','Excel_4G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location','Excel_NSM','Excel_ALU'] )
    #import_database_4_cai_new(['Excel_4G','Excel_to_2g_config_SRAN','Excel_to_3g_location','Excel_NSM','Excel_ALU'] )
    #import_database_4_cai_new(['Excel_3G'])
    #import_database_4_cai_new(['Excel_ALU'] )
    #import_database_4_cai_new(['Excel_to_2g'] )
    #import_database_4_cai_new(['Excel_4G'],is_import_from_exported_file=None)
    #import_database_4_cai_new(['ExcelImportNguyennhan'],is_import_from_exported_file='yes')
    #import_database_4_cai_new(['ExcelImportTrangThai'],is_import_from_exported_file='yes')
    '''
    path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_149.xlsx'
    workbook= xlrd.open_workbook(path)
    worksheet = workbook .sheet_by_name('Ericsson 3G')
    num_rows = worksheet .nrows - 1
    num_cols = worksheet.ncols - 1
    for curr_row_number in range(10):
        print '****row'
        for curr_col in range(num_cols-7,num_cols):
            value = read_excel_cell(worksheet,curr_row_number,curr_col)
            print value
    '''