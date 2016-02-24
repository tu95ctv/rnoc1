# -*- coding: utf-8 -*- 
import os
import xlrd,datetime
from django.core.exceptions import MultipleObjectsReturned
from unidecode import unidecode
from random import randint
import tempfile
import zipfile
from collections import OrderedDict
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from rnoc.models import Tram, Mll, Doitac, Nguyennhan,\
    Catruc, UserProfile, TrangThaiCuaTram, Duan, ThaoTacLienQuan, ThietBi,\
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


        
def read_excel_cell(worksheet,curr_row,curr_col,is_dict_attr = True):
    try:
        attr_name = dict_attr[curr_col]
    except:
        attr_name =''
    cell_value = worksheet.cell_value(curr_row, curr_col)
    print  attr_name,'curr_col %s,curr_row %s'%(curr_col, curr_row)
    return cell_value

class Excel_2_3g(object):
    added_foreinkey_types = set() # cai nay dung de tinh so luong du an, hoac thietbi, duoc add, neu nhieu qua thi stop
    max_length_added_foreinkey_types = 30
    backwards_sequence =[]
    many2manyFields = []
    update_or_create_main_item = ''#site_id_3g
    worksheet_name = u''
    begin_row=0
    manual_mapping_dict = {}
    mapping_function_to_value_dict = {}
    check = False
    auto_map = True
    model = Tram
    created_number =0
    update_number = 0
    just_create_map_field = False
    def __init__(self,workbook=None):
        if self.check:
            field = "site_ID_2G"
            method_of_field_name = 'value_for_'+field
            to_value_function = getattr(self, method_of_field_name)
            value = to_value_function('2G_adfdfdfdf')
            return None
        self.workbook = workbook
        self.read_excel()
        self.dict_attrName_columnNumber_excel_lower = self.define_attr_dict() # dict_attrName_columnNumber_excel_lower la ten cua cac cot lay trong file excel ra
        print 'dict_attrName_columnNumber_excel_lower',self.dict_attrName_columnNumber_excel_lower
        self.fieldnames = [f.name for f in self.model._meta.fields]
        if self.many2manyFields: # self.ModelClass._meta.many_to_many
            for x in self.many2manyFields:
                if x not in self.fieldnames:
                    self.fieldnames.append(x)
        self.base_fields = {}
        #self.auto_matching_dict ={}#auto mapping dict nghia la field name trung voi excel column name
        self.missing_fiedls =[]
        for fname in self.fieldnames:
            fname_lower = fname.lower()
            if self.auto_map and (fname_lower in self.dict_attrName_columnNumber_excel_lower):
                self.base_fields[fname] = self.dict_attrName_columnNumber_excel_lower[fname_lower]
            
            else: # 1 so attribute khong nam trong file excel
                if fname in self.manual_mapping_dict: #manual_mapping_dict la manual , do minh tu tao anh xa fieldname voi ten cot cua file excel
                    fieldname_in_excel = self.manual_mapping_dict[fname]
                    if isinstance(fieldname_in_excel, int):
                        self.base_fields.update({fname:fieldname_in_excel})
                    else:
                        fieldname_in_excel =  unidecode(fieldname_in_excel).lower().replace(' ','_') # file name format
                        #print 'fieldname_in_excel',fieldname_in_excel
                        if fieldname_in_excel in self.dict_attrName_columnNumber_excel_lower:
                            self.base_fields[fname]= self.dict_attrName_columnNumber_excel_lower[fieldname_in_excel] #= so thu tu cua column chua field do, vi du 5
                        else: # thieu cot nay hoac da bi doi ten                        
                            raise ValueError('trong file excel thieu cot %s '%fieldname_in_excel)
                else:
                    self.missing_fiedls.append(fname)
                    
        print 'self.base_fields',self.base_fields
        if self.just_create_map_field:
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
        curr_row = self.begin_row
        curr_col = 0
        global dict_attr
        while curr_col <= self.num_cols:
            value = read_excel_cell(self.worksheet, curr_row,curr_col,is_dict_attr = False)
            #atrrname la field name hay la collumn name
            atrrname = unidecode(value).lower().replace(" ","_")
            dict_attrName_columnNumber_excel_not_underscore[atrrname ]=   curr_col
            dict_attr[curr_col]= atrrname
            curr_col +=1
        return dict_attrName_columnNumber_excel_not_underscore
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
    def value_for_Cabinet(self,cell_value):
        thietbi = ThietBi.objects.get_or_create(Name=cell_value)[0]
        self.added_foreinkey_types.add(thietbi)#set().add
        l = len(self.added_foreinkey_types)
        print "cabin**",l
        if l >self.max_length_added_foreinkey_types:
            raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
        self.obj.Cabinet=thietbi
        return None
    def value_for_common_VLAN_ID (self,cell_value):
        value = int(cell_value)
        return value
    def loop_excel_and_insertdb(self):
        curr_row = self.begin_row
        main_field_index_excel_column = self.base_fields.pop(self.update_or_create_main_item) #index of main fields
        self.convert_basefield_to_list_of_tuple()
        while curr_row < self.num_rows:
            curr_row += 1
            to_value_function = self.get_function(self.update_or_create_main_item) # function for main field
            value = read_excel_cell(self.worksheet, curr_row,main_field_index_excel_column)
            if to_value_function:
                value = to_value_function(value)
            karg = {self.update_or_create_main_item:value}
            execute = self.model.objects.filter(**karg)
            if execute: # co db_row nay roi, update thoi
                self.created_or_update = 0
                for self.obj in execute:
                    self.update_field_for_obj(curr_row)
                    self.update_number +=1
            else: #tao moi
                self.created_or_update = 1   
                self.obj = self.model(**karg)
                self.update_field_for_obj(curr_row)
                self.created_number +=1
    def update_field_for_obj(self,curr_row):
        updated_values = {}
        for field_tuple in self.odering_base_columns_list_tuple:
            field = field_tuple[0]
            value =  read_excel_cell(self.worksheet, curr_row,field_tuple[1])
            if value and value !="null":
                to_value_function = self.get_function(field)
                if to_value_function:
                    value = to_value_function(value)
                if value:
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
class Excel_3G(Excel_2_3g):
    many2manyFields = ['du_an']
    just_create_map_field = False
    update_or_create_main_item = 'site_id_3g'
    worksheet_name = u'Ericsson 3G'
    backwards_sequence =['du_an']
    manual_mapping_dict = {'projectE':5,'du_an':5,'License_60W_Power':u'60W Power License','site_id_2g_E':u'Site ID 2G','Cell_1_Site_remote':u'Cell 1 (carrier 1)', \
                    'Cell_2_Site_remote':u'Cell 2 (Carrier 1)', 'Cell_3_Site_remote':u'Cell 3 (Carrier 1)',\
                     'Cell_4_Site_remote':u'Cell 4 (Carrier 2)', 'Cell_5_Site_remote':u'Cell 5 (Carrier 2)', 'Cell_6_Site_remote':u'Cell 6 (Carrier 2)', \
                     'Cell_7_Site_remote':u'Cell 7 (remote/U900/3 carrier)', 'Cell_8_Site_remote':u'Cell 8 (remote/U900/3 carrier)', 'Cell_9_Site_remote':u'Cell 9 (remote/U900/3 carrier)',\
                     'Cell_K_U900_PSI':u'Cell K (U900 PSI)'
                     }
    mapping_function_to_value_dict = {'Ngay_Phat_Song_2G':'value_for_dateField','Ngay_Phat_Song_3G':'value_for_dateField',\
                                      'IUB_VLAN_ID':'value_for_int_to_string','MUB_VLAN_ID':'value_for_int_to_string',\
                                    }
    def value_for_du_an(self,cell_value):
        if self.created_or_update == 1 :
            self.obj.save()
        execute = Duan.objects.get_or_create(Name=cell_value)
        du_an = execute[0]
        self.added_foreinkey_types.add(du_an)
        l = len(self.added_foreinkey_types)
        print "**",l
        if l>self.max_length_added_foreinkey_types:
            raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
        if execute[1]:
            du_an.type_2G_or_3G = '3G'
            du_an.save()
        self.obj.du_an.add(du_an)
        return None
    def value_for_site_id_3g(self,cell_value):
        value = 'ERI_3G_' + cell_value
        return value
    def value_for_site_ID_2G(self,value):
        return 'SRN_2G_' + value
    def value_for_site_name_2(self,cell_value):
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
    def value_for_site_name_1 (self,value):
        value = value.replace("3G_","")
        return value
    def value_for_Cabinet(self,cell_value):
        thietbi = ThietBi.objects.get_or_create(Name=cell_value)[0]
        self.added_foreinkey_types.add(thietbi)#set().add
        l = len(self.added_foreinkey_types)
        print "cabin**",l
        if l >self.max_length_added_foreinkey_types:
            raise ValueError("so luong m2m field qua nhieu, kha nang la ban da chon thu tu field tuong ung voi excel column bi sai")
        self.obj.Cabinet=thietbi
        return None
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
    
class Excel_to_2g (Excel_2_3g):
    backwards_sequence =['site_ID_2G',]
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'Database 2G'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'site_name_1':u'Tên BTS','dia_chi_2G':u'Địa chỉ', 'BSC_2G':u'Tên BSC',\
                    'LAC_2G':u'LAC', 'Nha_Tram':u'Nhà trạm', 'Ma_Tram_DHTT':u'Mã trạm ĐHTT', 'Cell_ID_2G':u'CellId', \
                    'cau_hinh_2G':u'Cấu hình', 'nha_san_xuat_2G':u'Nhà SX', 'site_ID_2G':u'Tên BTS',}
    
    def value_for_site_name_1 (self,cell_value):
        value = cell_value.replace("2G_","")
        return value
    def value_for_site_ID_2G(self,cell_value):
        
        self.obj.save()
        if cell_value.startswith('2G_'):
            return None  # return none for not save to database this field
        else:
            cell_value = self.obj.nha_san_xuat_2G.Name[0:3].upper() + '_2G_' + cell_value
            return  cell_value
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
class Excel_to_3g_location (Excel_2_3g):
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'site_id_3g'
    worksheet_name = u'3G Site Location'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'site_id_3g':u'Site ID','dia_chi_3G':u'Location'}
    def value_for_site_id_3g(self,cell_value):
        value = 'ERI_3G_' + cell_value
        return value
class Excel_to_2g_config_SRAN (Excel_2_3g):
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'2G SRAN HCM Config'
    mapping_function_to_value_dict ={}
    manual_mapping_dict = {'site_name_1':u'RSITE','TG':u'TG','TRX_DEF':u'TRX DEF'}
    def value_for_site_name_1 (self,cell_value):
        cell_value = cell_value.replace('2G_','')
        return cell_value
class Excel_NSM(Excel_2_3g):
    begin_row=1
    just_create_map_field = False
    auto_map = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'NSN Database'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_3G':'value_for_common_datefield','IUB_VLAN_ID':'value_for_common_VLAN_ID'}
    manual_mapping_dict = {'site_name_1':u'3G Site Name','site_id_3g':u'3G Site Name','Cabinet':u'Province',\
                    'Ngay_Phat_Song_3G':u'Ngày PS U900','RNC':u'RNC name','IUB_VLAN_ID':u'VLAN ID','IUB_DEFAULT_ROUTER':u'GW IP ',\
                    'IUB_HOST_IP':u'IP','MUB_SUBNET_PREFIX':u'Network IP','MUB_DEFAULT_ROUTER':u'TRS IP',\
                    'ntpServerIpAddressPrimary':u'NTP Primary IP','ntpServerIpAddressSecondary':u'NTP Secondary  IP'
                    }
    def value_for_site_name_1 (self,cell_value):
        cell_value = cell_value.replace('3G_','')
        return cell_value
    def value_for_site_id_3g(self,cell_value):
        #cell_value = cell_value.replace('3G_','NSM_')
        cell_value = 'NSM_'+ cell_value
        return cell_value
    
class Excel_ALU(Excel_2_3g):
    begin_row=3
    just_create_map_field = False
    
    auto_map = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'Database_ALU'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_3G':'value_for_common_datefield','IUB_VLAN_ID':'value_for_common_VLAN_ID','MUB_VLAN_ID':'value_for_common_VLAN_ID'}
    manual_mapping_dict = {'site_name_1':u'Tên trạm (ALU)','site_id_3g':u'Tên trạm (ALU)','Cabinet':u'RNC',\
                    'RNC':u'RNC',
                    'IUB_VLAN_ID':u'Iub Vlan','IUB_SUBNET_PREFIX':u'Iub Subnet',
                    'IUB_DEFAULT_ROUTER':u'Iub Default Router','IUB_HOST_IP':u'Iub Host',
                    'MUB_VLAN_ID':u'Mub Vlan','MUB_SUBNET_PREFIX':u'Mub Subnet',\
                    'MUB_HOST_IP':u'Mub Host','MUB_DEFAULT_ROUTER':u'Mub Default Router',\
                   
                    }
    manual_mapping_dict = {'site_name_1':2,'site_id_3g':2,'Cabinet':8,\
                    'RNC':8,\
                    'IUB_VLAN_ID':11,'IUB_SUBNET_PREFIX':12,\
                    'IUB_DEFAULT_ROUTER':13,'IUB_HOST_IP':14,\
                    'MUB_VLAN_ID':15,'MUB_SUBNET_PREFIX':16,\
                    'MUB_HOST_IP':18,'MUB_DEFAULT_ROUTER':17,\
                   
                    }
    def value_for_site_name_1 (self,cell_value):
        cell_value = cell_value.replace('3G_','')
        return cell_value
    def value_for_site_id_3g(self,cell_value):
        #cell_value = cell_value.replace('3G_','NSM_')
        cell_value = 'ALU_'+ cell_value
        return cell_value
    '''
    def value_for_Cabinet(self,cell_value):
        return 'ALU'
    '''

from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
def create_user():
    workbook = xlrd.open_workbook(MEDIA_ROOT+ '/document/DanhSachEmail.xls')
    worksheet = workbook.sheet_by_name(u'Sheet3')
    num_rows = worksheet.nrows - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        username =   read_excel_cell(worksheet, curr_row, 6)
        sdt  =   read_excel_cell(worksheet, curr_row, 5)
        groupname =   read_excel_cell(worksheet, curr_row, 7)
        user = User.objects.get_or_create (
                                        username = username
                                        )[0]
        user.set_password(username)
        user.save()                          
        group = Group.objects.get_or_create (name = groupname)[0]
        group.user_set.add(user)
        profile = UserProfile.objects.get_or_create(user =user)[0]
        profile.so_dien_thoai=sdt
        ca_truc = Catruc.objects.latest('id')
        profile.ca_truc = ca_truc
        profile.save()
def create_nguyen_nhan():
    nguyennhans= [u'MLL',u"Mất điện",u"Lỗi TD VTT",u"Mất cell",u"Mất 3 cell",u"Mất cell site remote",]
    for name in nguyennhans:
        nn = Nguyennhan.objects.get_or_create (
                                            Name = name,
                                            )[0]
        nn.Name_khong_dau = unidecode(name)
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
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        try:
            cellstt = read_excel_cell(worksheet, curr_row, 0)
            stt =   int(cellstt)
        except:
            continue
        Full_name = read_excel_cell(worksheet, curr_row, 1)
        Don_vi  = read_excel_cell(worksheet, curr_row, 4 )
        So_dien_thoai  =  read_excel_cell(worksheet, curr_row, 6)
        Nam_sinh  =  read_excel_cell(worksheet, curr_row,3 )
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(Nam_sinh))
            string_date_value = str(date + get_)[:10]# 
            d = datetime.datetime.strptime(string_date_value, '%Y-%m-%d') #date_time type
            Nam_sinh = d.strftime('%d/%m/%Y') # convert to string, again
        except:
            pass
        dia_chi_email = read_excel_cell(worksheet, curr_row, 5)
        try:
            doitac = Doitac.objects.get_or_create (
                                        Full_name = Full_name,
                                        )[0]
        except MultipleObjectsReturned:
            doitac = Doitac.objects.filter (
                                        Full_name = Full_name,)[0]
        doitac.Full_name_khong_dau = unidecode (Full_name)
        doitac.Don_vi  = Don_vi.replace('-',' ')
        doitac.So_dien_thoai  =  So_dien_thoai
        doitac.Nam_sinh  =  Nam_sinh
        doitac.dia_chi_email = dia_chi_email
        doitac.save()
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
        permission = Permission.objects.get_or_create(codename='d4_create_truc_ca_permission')
        #print 'username,user.has_perm',username,user.has_perm('drivingtest.d4_create_truc_ca_permission')

def import_database_4_cai_new (runlists,workbook = None,is_available_file= True):
    all_db3gfiles = ['Excel_3G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location',]
    if not is_available_file:#must file upload ,workbook = workbook_upload
        if 'ALL' in runlists:
            for class_func_name in all_db3gfiles:
                running_class = eval(class_func_name)
                running_class(workbook = workbook)
                if class_func_name in runlists:
                    runlists.remove(class_func_name)
            runlists.remove('ALL')
        #just remain alu,nsm, when alu,nsm,E in 1 file
        for class_func_name in runlists:
            running_class = eval(class_func_name)
            running_class(workbook = workbook)
    else: # get available file from disk           
        if 'ALL' in runlists:
            path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_134.xlsx'
            workbook= xlrd.open_workbook(path)
            for class_func_name in all_db3gfiles:
                running_class = eval(class_func_name)
                running_class(workbook = workbook)
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
                running_class(workbook = workbook)             
        for class_func_name in runlists:
            if class_func_name =='Excel_NSM':
                path = MEDIA_ROOT+ '/document/NSN_Database_version_4.xlsx'
            elif class_func_name =='Excel_ALU':
                path = MEDIA_ROOT+ '/document/Database_ALU lot 1-2 -3 den NGAY  5-8-2015 .xls'
            workbook= xlrd.open_workbook(path)
            running_class = eval(class_func_name)
            running_class(workbook = workbook)
            
                  
from django.template import Context,Template 
def tao_script_r6000_w12a(instance_site,ntpServerIpAddressPrimary = '10.213.227.98',ntpServerIpAddressSecondary = '10.213.227.102',\
                         ntpServerIpAddress1="10.213.235.134",ntpServerIpAddress2="10.213.235.135"):
    save_type = 'save to disk 1 achive file'
    now = datetime.datetime.now()
    site_id_3g= instance_site.site_id_3g
    instance_site.now = now
    return_file_lists = []
    achive_path=None
    sum_w11w12_temp = tempfile.TemporaryFile() # this time achive_path is template object file
    sum_w11w12__archive = zipfile.ZipFile(sum_w11w12_temp, 'w', zipfile.ZIP_DEFLATED)
    instance_site.id_n =  site_id_3g[-4:]
    instance_site.ntpServerIpAddressPrimary = ntpServerIpAddressPrimary
    instance_site.ntpServerIpAddressSecondary = ntpServerIpAddressSecondary
    instance_site.ntpServerIpAddress1 = ntpServerIpAddress1
    instance_site.ntpServerIpAddress2 = ntpServerIpAddress2
    template_files = ['CM6167_IUB_W12_3.mo','CM6167_OAM_W12_1.xml','CM6167_SE-2carriers_2.xml']
    template_files2 = ['IUB_W11_3.mo','OAM_W11_1.xml','SE-W11_2carriers_2.xml']
    wversion_templates = [template_files]
    for count_teplate,template_files in enumerate(wversion_templates):
        pathd = (MEDIA_ROOT+ '/document/template_script/CM6167_r6000_w12/') if (count_teplate==0) else (MEDIA_ROOT+ 'document/template_script/6000_site1_w11_dien/')
        for counts,tf in enumerate(template_files):
            path_to_1_template_file =  pathd + tf
            template = read_file_from_disk (path_to_1_template_file)
            t = Template(template)
            c = Context({'site3g':instance_site})
            output = t.render(c)
            fname = site_id_3g + tf.replace('CM6167','')
            folder_name = '5484692'
            new_directory_path = MEDIA_ROOT+ '/for_user_download_folder/' + folder_name + '/'
            if save_type == 'save_to_disk_3_file':
                if not os.path.exists(new_directory_path): os.makedirs(new_directory_path)
                filepath = new_directory_path  + fname
                return_file_lists.append(folder_name + '/' +  fname)
                save_file_to_disk(filepath,output,1)
            else:
                if counts==0:
                    if save_type =='save to disk 1 achive file':
                        achive_path = new_directory_path + site_id_3g +'.zip'
                    elif  save_type == 'temp 1 achive file':
                        achive_path = tempfile.TemporaryFile() # this time achive_path is template object file
                    archive = zipfile.ZipFile(achive_path, 'w', zipfile.ZIP_DEFLATED)
            archive.writestr(fname, output)
        arcname = site_id_3g +('_W12_'if (count_teplate==0) else '_W11_' ) + '.zip'
        sum_w11w12__archive.write(achive_path,arcname )
        return return_file_lists,sum_w11w12_temp
def tao_script_r6000_w12(instance_site,ntpServerIpAddressPrimary = '10.213.227.98',ntpServerIpAddressSecondary = '10.213.227.102',\
                         ntpServerIpAddress1="10.213.235.134",ntpServerIpAddress2="10.213.235.135"):
    Cabinet = instance_site.Cabinet
    luu_o_cung = True
    save_type = 'temp 1 achive file'
    now = datetime.datetime.now()
    site_id_3g= instance_site.site_id_3g
    instance_site.now = now
    return_file_lists = []
    achive_path=None
    instance_site.id_n =  site_id_3g[-4:]
    instance_site.ntpServerIpAddressPrimary = ntpServerIpAddressPrimary
    instance_site.ntpServerIpAddressSecondary = ntpServerIpAddressSecondary
    instance_site.ntpServerIpAddress1 = ntpServerIpAddress1
    instance_site.ntpServerIpAddress2 = ntpServerIpAddress2
    template_files =[]
    if "RBS6" in Cabinet.Name:
        type_rbs = "6000"
        path_directory = MEDIA_ROOT+ '/document/template_script/6000/'
    elif "RBS3" in Cabinet.Name:
        path_directory = MEDIA_ROOT+ '/document/template_script/3000/'
        type_rbs = "3000"
    for root, dirs, files in os.walk(path_directory):
        for file in files:
            template_files.append(file)
    for counts,tf in enumerate(template_files):
        path_to_1_template_file =  path_directory + tf
        template = read_file_from_disk (path_to_1_template_file)
        t = Template(template)
        c = Context({'site3g':instance_site})
        output = t.render(c)
        fname = site_id_3g + '_' + tf
        folder_name = '5484692'
        new_directory_path = MEDIA_ROOT+ '/for_user_download_folder/' + folder_name + '/'
        if save_type == 'save_to_disk_3_file':
            if not os.path.exists(new_directory_path): os.makedirs(new_directory_path)
            filepath = new_directory_path  + fname
            return_file_lists.append(folder_name + '/' +  fname)
            save_file_to_disk(filepath,output,1)
        else:
            if counts==0:
                if save_type =='save to disk 1 achive file':
                    achive_path = new_directory_path + site_id_3g +'.zip'
                elif  save_type == 'temp 1 achive file':# dang dung
                    achive_path = tempfile.TemporaryFile() # this time achive_path is template object file
                archive = zipfile.ZipFile(achive_path, 'w', zipfile.ZIP_DEFLATED)
            if luu_o_cung:
                if not os.path.exists(new_directory_path): os.makedirs(new_directory_path)
                filepath = new_directory_path  + fname
                save_file_to_disk(filepath,output,1)
            archive.writestr(fname, output)
    return return_file_lists, achive_path, type_rbs # achive_path become tempt zip file

def import_TrangThaiCuaTram():
    path = MEDIA_ROOT+ '/document/trangthaicuatram.xls'
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(u'Sheet3')
    num_rows = worksheet.nrows - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        Name_trangthai = read_excel_cell(worksheet, curr_row, 1)
        TrangThaiCuaTram.objects.get_or_create(Name = Name_trangthai)
class ThaoTac(Excel_2_3g):
    model=ThaoTacLienQuan
    worksheet_name = u'Sheet3'
    begin_row=0
    update_or_create_main_item = 'name'
    #manual_mapping_dict = {'projectE':5,'du_an':5,'License_60W_Power':u'60W Power License'}
def import_thao_tac():
    path = MEDIA_ROOT+ '/document/thaotaclienquan.xls'
    workbook= xlrd.open_workbook(path)
    ThaoTac(workbook)
def create_ca_truc():
    for ca_truc_name in ['Moto','Alu','Huawei','Sran']:
        instance = Catruc.objects.get_or_create(Name=ca_truc_name)[0]
        instance.save()
import shutil
def remove_folder(path):
    shutil.rmtree(path)
def delete_edithistory_table3g():
    EditHistory.objects.filter(modal_name='Tram').delete()
if __name__ == '__main__':
    '''
    create_ca_truc()
    create_user()
    grant_permission_to_group()
    #check_permission_of_group()
    import_doi_tac()
    import_TrangThaiCuaTram()
    import_thao_tac()
    create_nguyen_nhan()
    create_thiet_bi()
    '''
    #delete_edithistory_table3g()
    #import_database_4_cai_new(['Excel_3G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location','Excel_NSM','Excel_ALU'] )
    #import_database_4_cai_new(['Excel_3G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location',])
    #import_database_4_cai_new(['Excel_ALU'] )
    #import_database_4_cai_new(['Excel_to_2g'] )
    import_database_4_cai_new(['Excel_3G'])