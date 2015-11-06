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
from drivingtest.models import Table3g, Command3g, Mll, Doitac, Nguyennhan,\
    Catruc, UserProfile, TrangThaiCuaTram, Duan

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
    print  attr_name,'curr_col %s,curr_row %s, cell_value %s'%(curr_col, curr_row,cell_value)
    return cell_value

class Excel_2_3g(object):
    backwards_sequence =[]
    #dict_attrName_columnNumber_excel_not_underscore ={'Cell 9 (Site remote)': 41, 'Site Name 1': 9, 'Site Name 2': 12, 'MUB VLAN ID': 24, 'IUB VLAN ID': 20, 'Ngay phat song 2G': 8, 'Cell 7 (Site remote)': 39, 'Cell 8 (Site remote)': 40, 'Status': 15, 'Cell 1 (carrier 1)': 33, '60W Power License': 2, 'Cabinet': 17, 'Site ID 3G': 6, 'MUB DEFAULT ROUTER': 26, 'Cell 6 (Carrier 2)': 38, 'Cell 3 (Carrier 1)': 35, 'MUB HOST IP': 27, 'BSC': 14, 'Ngay phat song 3G': 13, 'Count Province': 31, 'Thu hoi': 42, 'Check name': 10, '3 Carriers': 4, 'UPE': 28, 'Project': 30, 'U900': 3, 'IUB DEFAULT ROUTER': 22, 'Site remote': 44, 'IUB SUBNET PREFIX': 21, 'Trans': 16, 'Cell 5 (Carrier 2)': 37, 'STT': 0, 'Compare': 11, 'Cell 2 (Carrier 1)': 34, 'RNC': 19, 'Splitter': 43, 'DUW 3001': 1, 'Cell 4 (Carrier 2)': 36, 'Count RNC': 32, 'Site ID 2G': 7, 'MUB SUBNET PREFIX': 25, 'GHI CHU': 29, 'Port': 18, 'IUB HOST IP': 23}
    #specific_db_fields=[]
    many2manyFields = []
    update_or_create_main_item = ''#site_id_3g
    worksheet_name = u''
    begin_row=0
    mapping_dict = {}
    mapping_function_to_value_dict = {}
    check = False
    auto_map = True
    model = Table3g
    created_number =0
    update_number = 0
    just_create_map_field = False
    def __init__(self,workbook=None):
        if self.check:
            field = "site_ID_2G"
            method_of_field_name = 'value_for_'+field
            print method_of_field_name
            to_value_function = getattr(self, method_of_field_name)
            value = to_value_function('2G_adfdfdfdf')
            print value
            return None
        self.workbook = workbook
        self.read_excel()
        self.dict_attrName_columnNumber_excel_lower = self.define_attr_dict() # no underscore and lower
        self.fieldnames = [f.name for f in self.model._meta.fields]
        if self.many2manyFields:
            for x in self.many2manyFields:
                if x not in self.fieldnames:
                    self.fieldnames.append(x)
        print 'fieldnames',len(self.fieldnames),self.fieldnames
        self.base_fields = {}
        self.matching_map_dict ={}
        self.missing_fiedls =[]
        for fname in self.fieldnames:
            fname_lower = fname.lower()
            if self.auto_map and (fname_lower in self.dict_attrName_columnNumber_excel_lower):
                print 'fname',fname
                self.matching_map_dict[fname] = self.dict_attrName_columnNumber_excel_lower[fname_lower]
            else: # 1 so attribute khong nam trong file excel
                if fname in self.mapping_dict: 
                    match_element = self.mapping_dict[fname]
                    if isinstance(match_element, int):
                        self.base_fields.update({fname:match_element})
                    else:
                        match_element =  unidecode(match_element).lower().replace(' ','_') # file name format
                        print 'match_element',match_element
                        if match_element in self.dict_attrName_columnNumber_excel_lower:
                            self.base_fields[fname]= self.dict_attrName_columnNumber_excel_lower[match_element]
                        else: # thieu cot nay hoac da bi doi ten                        
                            raise ValueError('trong file excel thieu cot %s '%match_element)
                else:
                    self.missing_fiedls.append(fname)
        
        
        '''
        self.specific_db_fields_dict = {}
        for fname in self.specific_db_fields:
            if fname in self.mapping_dict: # qui uoc 1 so attribute khong nam trong file excel nhung tuong ung voi nhung column 
                match_element = self.mapping_dict[fname]
                if isinstance(match_element, int):
                    if fname in self.base_fields:
                        self.base_fields.pop(fname)
                    self.specific_db_fields_dict[fname] =match_element
                else:
                    match_element =  unidecode(match_element).lower().replace(' ','_') # file name format
                    print 'match_element',match_element
                    if match_element in self.dict_attrName_columnNumber_excel_lower:
                        self.specific_db_fields_dict[fname]= self.dict_attrName_columnNumber_excel_lower[match_element]
                    else: # thieu cot nay hoac da bi doi ten                        
                        raise ValueError('trong file excel thieu cot %s '%match_element)
            else:
                self.missing_fiedls.append(fname)
        '''        
                
        
        print 'self.fieldnames = [f.name for f in self.model._meta.fields] ,',len(self.fieldnames ),self.fieldnames 
        print 'pre mapping_dict',len(self.mapping_dict),self.mapping_dict
        print 'set_up_dict',len(self.base_fields),self.base_fields
        print 'self.matching_map_dict',len(self.matching_map_dict),self.matching_map_dict
        self.base_fields.update(self.matching_map_dict)
        print 'self.base_fields',len(self.base_fields),self.base_fields ,'\n self.missing_fiedls',len(self.missing_fiedls) ,self.missing_fiedls
        #print 'self.specific_db_fields_dict',len(self.specific_db_fields_dict),self._dict
        print 'excel field',len(self.dict_attrName_columnNumber_excel_lower),self.dict_attrName_columnNumber_excel_lower
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
            #sequence.remove(self.update_or_create_main_item)    
            print 'sequence',len(sequence),sequence
            print 'self.base_fields',len(self.base_fields),self.base_fields
            self.odering_base_columns_list_tuple = [(x, self.base_fields[x]) for x in sequence]
        else:
            self.odering_base_columns_list_tuple = [(k,v) for k, v in self.base_fields.iteritems()]
        print 'self.odering_base_columns_list_tuple',self.odering_base_columns_list_tuple
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
            atrrname = unidecode(value).lower().replace(" ","_")
            dict_attrName_columnNumber_excel_not_underscore[atrrname ]=   curr_col
            dict_attr[curr_col ]=   atrrname
            curr_col +=1
        print dict_attrName_columnNumber_excel_not_underscore
        return dict_attrName_columnNumber_excel_not_underscore
    def value_for_common_datefield(self,cell_value):
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(cell_value)) # delte du lieu datetime
            get_col2 = str(date + get_)[:10] # convert date to string theo dang nao do
            value = get_col2 # moi them vo
            return value
        except:
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
            #print to_value_function
            value = read_excel_cell(self.worksheet, curr_row,main_field_index_excel_column)
            if to_value_function:
                value = to_value_function(value)
            karg = {self.update_or_create_main_item:value}
            execute = Table3g.objects.filter(**karg)
            print 'execute',execute
            if execute: # co db_row nay roi, update thoi
                self.created_or_update = 0
                for self.obj in execute:
                    self.update_field_for_obj(curr_row)
                    self.update_number +=1
            else: #tao moi
                self.created_or_update = 1   
                self.obj = Table3g(**karg)
                self.update_field_for_obj(curr_row)
                self.created_number +=1
            print 'self.update_number',self.update_number,'self.created_number',self.created_number
    def update_field_for_obj(self,curr_row):
        updated_values = {}
        print ' self.odering_base_columns_list_tuple', self.odering_base_columns_list_tuple
        for field_tuple in self.odering_base_columns_list_tuple:
            print '**field_tuple in update_field_for_obj',field_tuple
            field = field_tuple[0]
            value =  read_excel_cell(self.worksheet, curr_row,field_tuple[1])
            if value:
                to_value_function = self.get_function(field)
                if to_value_function:
                    value = to_value_function(value)
                if value:
                    setattr(self.obj, field, value) # save
        self.obj.save()        
                    #updated_values[field] = value
        #print 'updated_values',updated_values
        #self.save_to_db(updated_values)
        
        
        
    def get_function(self,field):
        if field in self.mapping_function_to_value_dict:
            func_name = self.mapping_function_to_value_dict[field]
            to_value_function = getattr(self, func_name)
            return to_value_function
        else:
            try:
                method_of_field_name = 'value_for_'+field
                #print 'method_of_field_name',method_of_field_name
                to_value_function = getattr(self, method_of_field_name) #
                return to_value_function
            except: # Ko co ham nao thay doi gia tri value
                return None
        
    def save_to_db(self,updated_values):
        
        print 'obj in save_to_db',self.obj
        for key, value in updated_values.iteritems():
                setattr(self.obj, key, value)
        self.obj.save()
        
    '''
    def save_to_db1(self,karg,updated_values):
        try:
            print karg
            obj = Table3g.objects.filter(**karg)[0]
            for key, value in updated_values.iteritems():
                setattr(obj, key, value)
            obj.save()
            self.update_number = self.update_number + 1
        except :
            updated_values.update(karg)
            obj = Table3g(**updated_values)
            obj.save()
            self.created_number = self.created_number + 1
        print 'created_number',self.created_number,'update_number',self.update_number
        '''
class Excel_3G(Excel_2_3g):
    many2manyFields = ['du_an']
    just_create_map_field = False
    update_or_create_main_item = 'site_id_3g'
    worksheet_name = u'Ericsson 3G'
    backwards_sequence =['du_an']
    #specific_db_fields = ['du_an']
    mapping_dict = {'projectE':5,'du_an':5,'License_60W_Power':u'60W Power License','site_id_2g_E':u'Site ID 2G','Cell_1_Site_remote':u'Cell 1 (carrier 1)', \
                    'Cell_2_Site_remote':u'Cell 2 (Carrier 1)', 'Cell_3_Site_remote':u'Cell 3 (Carrier 1)',\
                     'Cell_4_Site_remote':u'Cell 4 (Carrier 2)', 'Cell_5_Site_remote':u'Cell 5 (Carrier 2)', 'Cell_6_Site_remote':u'Cell 6 (Carrier 2)', \
                     'Cell_7_Site_remote':u'Cell 7 (Site remote)', 'Cell_8_Site_remote':u'Cell 8 (Site remote)', 'Cell_9_Site_remote':u'Cell 9 (Site remote)',}
    mapping_function_to_value_dict = {'Ngay_Phat_Song_2G':'value_for_dateField','Ngay_Phat_Song_3G':'value_for_dateField',\
                                      'IUB_VLAN_ID':'value_for_int_to_string','MUB_VLAN_ID':'value_for_int_to_string',\
                                    }
    def value_for_du_an(self,cell_value):
        if self.created_or_update == 1 :
            self.obj.save()
        print 'obj',self.obj
        print 'in du_an '
        execute = Duan.objects.get_or_create(Name=cell_value)
        du_an = execute[0]
        if execute[1]:
            print '**create 1 '
            du_an.type_2G_or_3G = '3G'
            du_an.save()
        self.obj.du_an.add(du_an)
        return None
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
    def value_for_site_id_3g(self,cell_value):
        value = 'ERI_3G_' + cell_value
        return value
    
    '''
    def main_field_to_value (self,cell_value):
        cell_value = cell_value.replace("3G_","")
        return cell_value
    '''
    
class Excel_to_2g (Excel_2_3g):
    backwards_sequence =['site_ID_2G']
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'Database 2G'
    mapping_function_to_value_dict ={}
    mapping_dict = {'site_name_1':u'Tên BTS','dia_chi_2G':u'Địa chỉ', 'BSC_2G':u'Tên BSC',\
                    'LAC_2G':u'LAC', 'Nha_Tram':u'Nhà trạm', 'Ma_Tram_DHTT':u'Mã trạm ĐHTT', 'Cell_ID_2G':u'CellId', \
                    'cau_hinh_2G':u'Cấu hình', 'nha_san_xuat_2G':u'Nhà SX', 'site_ID_2G':u'Tên BTS',}
    #def value_for_nha_san_xuat_2G(self):
    def value_for_site_name_1 (self,cell_value):
        value = cell_value.replace("2G_","")
        return value
    def value_for_site_ID_2G(self,cell_value):
        
        self.obj.save()
        if cell_value.startswith('2G_'):
            return None  # return none for not save to database this field
        else:
            print  'self.obj.site_name_1',self.obj.site_name_1
            print  'self.obj.Cell_ID_2G',self.obj.Cell_ID_2G
            print  'self.obj.dia_chi_2G',self.obj.dia_chi_2G
            print  'self.obj.cau_hinh_2G',self.obj.cau_hinh_2G
            print  'self.obj.LAC_2G',self.obj.LAC_2G
            cell_value = self.obj.nha_san_xuat_2G[0:3].upper() + '_2G_' + cell_value
            return  cell_value
class Excel_to_3g_location (Excel_2_3g):
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'site_id_3g'
    worksheet_name = u'3G Site Location'
    mapping_function_to_value_dict ={}
    mapping_dict = {'site_id_3g':u'Site ID','dia_chi_3G':u'Location'}
    def main_field_to_value (self,cell_value):
        return cell_value
class Excel_to_2g_config_SRAN (Excel_2_3g):
    auto_map = False
    just_create_map_field = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'2G SRAN HCM Config'
    mapping_function_to_value_dict ={}
    mapping_dict = {'site_name_1':u'RSITE','TG':u'TG','TRX_DEF':u'TRX DEF'}
    def main_field_to_value (self,cell_value):
        cell_value = cell_value.replace('2G_','')
        return cell_value
class Excel_NSM(Excel_2_3g):
    begin_row=1
    just_create_map_field = False
    auto_map = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'NSN Database'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_3G':'value_for_common_datefield','IUB_VLAN_ID':'value_for_common_VLAN_ID'}
    mapping_dict = {'site_name_1':u'3G Site Name','site_id_3g':u'3G Site Name','Cabinet':u'Province',\
                    'Ngay_Phat_Song_3G':u'Ngày PS U900','RNC':u'RNC name','IUB_VLAN_ID':u'VLAN ID','IUB_DEFAULT_ROUTER':u'GW IP ',\
                    'IUB_HOST_IP':u'IP','MUB_SUBNET_PREFIX':u'Network IP','MUB_DEFAULT_ROUTER':u'TRS IP',\
                    'ntpServerIpAddressPrimary':u'NTP Primary IP','ntpServerIpAddressSecondary':u'NTP Secondary  IP'
                    }
    def main_field_to_value (self,cell_value):
        cell_value = cell_value.replace('3G_','')
        return cell_value
    def value_for_site_id_3g(self,cell_value):
        #cell_value = cell_value.replace('3G_','NSM_')
        cell_value = 'NSM_'+ cell_value
        return cell_value
    def value_for_Cabinet(self,cell_value):
        return 'NSM'
class Excel_ALU(Excel_2_3g):
    begin_row=3
    just_create_map_field = False
    
    auto_map = False
    update_or_create_main_item = 'site_name_1'
    worksheet_name = u'Database_ALU'
    mapping_function_to_value_dict ={'Ngay_Phat_Song_3G':'value_for_common_datefield','IUB_VLAN_ID':'value_for_common_VLAN_ID','MUB_VLAN_ID':'value_for_common_VLAN_ID'}
    mapping_dict = {'site_name_1':u'Tên trạm (ALU)','site_id_3g':u'Tên trạm (ALU)','Cabinet':u'RNC',\
                    'RNC':u'RNC',
                    'IUB_VLAN_ID':u'Iub Vlan','IUB_SUBNET_PREFIX':u'Iub Subnet',
                    'IUB_DEFAULT_ROUTER':u'Iub Default Router','IUB_HOST_IP':u'Iub Host',
                    'MUB_VLAN_ID':u'Mub Vlan','MUB_SUBNET_PREFIX':u'Mub Subnet',\
                    'MUB_HOST_IP':u'Mub Host','MUB_DEFAULT_ROUTER':u'Mub Default Router',\
                   
                    }
    mapping_dict = {'site_name_1':2,'site_id_3g':2,'Cabinet':8,\
                    'RNC':8,\
                    'IUB_VLAN_ID':11,'IUB_SUBNET_PREFIX':12,\
                    'IUB_DEFAULT_ROUTER':13,'IUB_HOST_IP':14,\
                    'MUB_VLAN_ID':15,'MUB_SUBNET_PREFIX':16,\
                    'MUB_HOST_IP':18,'MUB_DEFAULT_ROUTER':17,\
                   
                    }
    def main_field_to_value (self,cell_value):
        cell_value = cell_value.replace('3G_','')
        return cell_value
    def value_for_site_id_3g(self,cell_value):
        #cell_value = cell_value.replace('3G_','NSM_')
        cell_value = 'ALU_'+ cell_value
        return cell_value
    def value_for_Cabinet(self,cell_value):
        return 'ALU'
'''
def read_txt_database_3G(workbook):
    #datemodebook = workbook.datemode
    #print 'datemodebook',datemodebook
    worksheet = workbook.sheet_by_name(u'Ericsson 3G')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    num_cols = worksheet.ncols - 1
    curr_col = 0
    global dict_attr
    while curr_col < num_cols:
        atrrname = unidecode(read_excel_cell(worksheet, curr_row,curr_col,is_dict_attr = False)).replace("_"," ")
        dict_attr[atrrname ]=   curr_col
        curr_col +=1
    print 'dict_attr',dict_attr
    return None
    
    
    while curr_row < num_rows:
        offset =2 
        curr_row += 1
        print 'Row:', curr_row
        site_id_3g = read_excel_cell(worksheet, curr_row,4 + offset)
        print 'site_id_3g',
        new_instance = Table3g.objects.get_or_create (
                                         site_id_3g= site_id_3g
                                        )[0]

        new_instance.License_60W_Power = read_excel_cell(worksheet, curr_row, 1 )
        new_instance.U900 = read_excel_cell(worksheet, curr_row, 2) 
        new_instance.site_id_2g_E= read_excel_cell(worksheet, curr_row, 5+offset) 
        Ngay_Phat_Song_2G = read_excel_cell(worksheet, curr_row, 6 + offset) 

        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(Ngay_Phat_Song_2G))
            get_col2 = str(date + get_)[:10]
            d = datetime.datetime.strptime(get_col2, '%Y-%m-%d')
            get_col = d.strftime('%d-%m-%Y')
            print d
            new_instance.Ngay_Phat_Song_2G = get_col
        except:
            pass
        
        new_instance.site_name_1= read_excel_cell(worksheet, curr_row, 7 + offset).replace("3G_","") 
        offset =4
        new_instance.site_name_2= read_excel_cell(worksheet, curr_row, 8 + offset).replace("3G_","")
        
        Ngay_Phat_Song_3G = read_excel_cell(worksheet, curr_row, 9 + offset)
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(Ngay_Phat_Song_3G))
            get_col2 = str(date + get_)[:10]
            d = datetime.datetime.strptime(get_col2, '%Y-%m-%d')
            get_col = d.strftime('%d-%m-%Y')
            print d
            new_instance.Ngay_Phat_Song_3G = get_col
        except:
            pass 
        new_instance.BSC  = read_excel_cell(worksheet, curr_row, 10 + offset)
        Status = read_excel_cell(worksheet, curr_row, 11 + offset) 
        if len(Status)<=15:
            new_instance.Status = Status
        new_instance.Trans= read_excel_cell(worksheet, curr_row, 12 + offset) 
        new_instance.Cabinet = read_excel_cell(worksheet, curr_row, 13 + offset) 
        new_instance.Port = read_excel_cell(worksheet, curr_row, 14 + offset) 
        new_instance.RNC = read_excel_cell(worksheet, curr_row, 15 + offset) 
        try:
            new_instance.IUB_VLAN_ID = int(read_excel_cell(worksheet, curr_row, 16 + offset))
        except: 
            new_instance.IUB_VLAN_ID = read_excel_cell(worksheet, curr_row, 16 + offset)
            
        IUB_SUBNET_PREFIX = read_excel_cell(worksheet, curr_row, 17 + offset)
        print 'IUB_SUBNET_PREFIX',IUB_SUBNET_PREFIX
        if IUB_SUBNET_PREFIX:
            new_instance.IUB_SUBNET_PREFIX =  IUB_SUBNET_PREFIX
        IUB_DEFAULT_ROUTER = read_excel_cell(worksheet, curr_row, 18 + offset)
        if  IUB_DEFAULT_ROUTER:
            new_instance.IUB_DEFAULT_ROUTER = read_excel_cell(worksheet, curr_row, 18 + offset)
        IUB_HOST_IP = read_excel_cell(worksheet, curr_row, 19 + offset)
        if IUB_HOST_IP:
            new_instance.IUB_HOST_IP = IUB_HOST_IP
        try: 
            new_instance.MUB_VLAN_ID = int(read_excel_cell(worksheet, curr_row, 20 + offset))
        except:
            new_instance.MUB_VLAN_ID = read_excel_cell(worksheet, curr_row, 20 + offset)
        MUB_SUBNET_PREFIX = read_excel_cell(worksheet, curr_row, 21 + offset)
        if  MUB_SUBNET_PREFIX:
            new_instance.MUB_SUBNET_PREFIX = MUB_SUBNET_PREFIX
        MUB_DEFAULT_ROUTER = read_excel_cell(worksheet, curr_row, 22 + offset) 
        if MUB_DEFAULT_ROUTER:
            new_instance.MUB_DEFAULT_ROUTER = MUB_DEFAULT_ROUTER
        MUB_HOST_IP = read_excel_cell(worksheet, curr_row, 23 + offset)
        if MUB_HOST_IP:
            new_instance.MUB_HOST_IP = MUB_HOST_IP
        new_instance.UPE = read_excel_cell(worksheet, curr_row, 24 + offset) 
        new_instance.GHI_CHU = read_excel_cell(worksheet, curr_row, 25 + offset) 
        
        offset =5 
        new_instance.Count_Province = read_excel_cell(worksheet, curr_row, 26 + offset) 
        new_instance.Count_RNC = read_excel_cell(worksheet, curr_row, 27 + offset) 
        new_instance.Cell_1_Site_remote = read_excel_cell(worksheet, curr_row, 28 + offset) 
        new_instance.Cell_2_Site_remote = read_excel_cell(worksheet, curr_row, 29 + offset) 
        new_instance.Cell_3_Site_remote = read_excel_cell(worksheet, curr_row, 30 + offset) 
        new_instance.Cell_4_Site_remote = read_excel_cell(worksheet, curr_row, 31 + offset) 
        new_instance.Cell_5_Site_remote = read_excel_cell(worksheet, curr_row, 32 + offset) 
        new_instance.Cell_6_Site_remote = read_excel_cell(worksheet, curr_row, 33 + offset) 
        new_instance.Cell_7_Site_remote = read_excel_cell(worksheet, curr_row, 34 + offset) 
        new_instance.Cell_8_Site_remote = read_excel_cell(worksheet, curr_row, 35 + offset) 
        new_instance.Cell_9_Site_remote = read_excel_cell(worksheet, curr_row, 36 + offset) 
        new_instance.save()

def read_txt_database_2G(workbook):
    #workbook = xlrd.open_workbook(path)

    worksheet = workbook.sheet_by_name(u'Database 2G')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        print 'Row:', curr_row
        site_name_2g = read_excel_cell(worksheet, curr_row, 2).replace("2G_","")
        try:
            new_instance = Table3g.objects.get_or_create (
                                             site_name_1= site_name_2g
                  
    
                                            )[0]
        except MultipleObjectsReturned:
            continue
            
        if not new_instance.site_id_2g_E:
            new_instance.site_id_2g_E = site_name_2g
        new_instance.site_ID_2G =  read_excel_cell(worksheet, curr_row, 5)
        new_instance.BSC_2G =  read_excel_cell(worksheet, curr_row, 0)
        new_instance.Cell_ID_2G =  read_excel_cell(worksheet, curr_row, 18)
        new_instance.LAC_2G =  read_excel_cell(worksheet, curr_row, 12)
        
        new_instance.Nha_Tram =  read_excel_cell(worksheet, curr_row, 1)
        new_instance.Ma_Tram_DHTT =  read_excel_cell(worksheet, curr_row, 3)
 
        
        new_instance.dia_chi_2G = read_excel_cell(worksheet, curr_row, 10) 
        new_instance.cau_hinh_2G = read_excel_cell(worksheet, curr_row, 17) 
        new_instance.nha_san_xuat_2G= read_excel_cell(worksheet, curr_row, 31) 
        
        new_instance.save()

def read_txt_database_3G_Site_Location(workbook):

    worksheet = workbook.sheet_by_name(u'3G Site Location')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        print 'Row:', curr_row
        new_instance = Table3g.objects.get_or_create (
                                         site_id_3g= read_excel_cell(worksheet, curr_row, 1)
              

                                        )[0]

        new_instance.dia_chi_3G = read_excel_cell(worksheet, curr_row, 6) 
        new_instance.save()
def read_txt_database_2G_SRAN_HCM_Config(workbook):

    worksheet = workbook.sheet_by_name(u'2G SRAN HCM Config')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        print 'Row:', curr_row
        new_instance = Table3g.objects.get_or_create (
                                         site_name_1= read_excel_cell(worksheet, curr_row, 2).replace("2G_","")
              

                                        )[0]

        new_instance.TG = read_excel_cell(worksheet, curr_row, 3)
        new_instance.TRX_DEF = read_excel_cell(worksheet, curr_row, 5)  
        new_instance.save()
        
def read_txt_database_alu(workbook):
    datemodebook = workbook.datemode
    print 'datemodebook',datemodebook
    worksheet = workbook.sheet_by_name(u'Database_ALU')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        print 'Row:', curr_row
        site_name1_no_3g_prefix = read_excel_cell(worksheet, curr_row,2).replace("3G_","")
        
        new_instance = Table3g.objects.get_or_create (
                                        site_name_1 = site_name1_no_3g_prefix 
                                        
                                        )[0]


        new_instance.site_id_3g= 'ALU_' + site_name1_no_3g_prefix
        new_instance.Status = read_excel_cell(worksheet, curr_row, 6)
        new_instance.RNC = read_excel_cell(worksheet, curr_row, 8)
        new_instance.GHI_CHU = read_excel_cell(worksheet, curr_row, 9)
        new_instance.Port = read_excel_cell(worksheet, curr_row, 10)
        try:
            new_instance.IUB_VLAN_ID = int(read_excel_cell(worksheet, curr_row, 11))
        except: 
            new_instance.IUB_VLAN_ID = read_excel_cell(worksheet, curr_row, 11)
        new_instance.IUB_SUBNET_PREFIX = read_excel_cell(worksheet, curr_row, 12) 
        new_instance.IUB_DEFAULT_ROUTER = read_excel_cell(worksheet, curr_row, 13) 
        new_instance.IUB_HOST_IP = read_excel_cell(worksheet, curr_row, 14)
        try: 
            new_instance.MUB_VLAN_ID = int(read_excel_cell(worksheet, curr_row, 15))
        except:
            new_instance.MUB_VLAN_ID = read_excel_cell(worksheet, curr_row, 15)
        new_instance.MUB_SUBNET_PREFIX = read_excel_cell(worksheet, curr_row, 16) 
        new_instance.MUB_DEFAULT_ROUTER = read_excel_cell(worksheet, curr_row, 17) 
        new_instance.MUB_HOST_IP = read_excel_cell(worksheet, curr_row, 18) 
        new_instance.UPE = read_excel_cell(worksheet, curr_row, 19) 
      
        new_instance.save()
def read_txt_database_command():

    worksheet = workbook.sheet_by_name(u'Sheet3')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        print 'Row:', curr_row
        sign_command= read_excel_cell(worksheet, curr_row,0)
        if sign_command != "l":
            continue
            print 'khong xu ly row nay'
        Command= read_excel_cell(worksheet, curr_row,6)
        
        new_instance = Command3g.objects.get_or_create (
                                        command = Command 
                                        
                                        )[0]


        new_instance.ten_lenh = read_excel_cell(worksheet, curr_row, 7)
        new_instance.mo_ta = read_excel_cell(worksheet, curr_row, 8)
        new_instance.save()
'''
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
def create_user(path):
    '''
    user = User.objects.create_user('thi', 'lennon@thebeatles.com', 'thi')  
    user.is_staff = True
    user.save()
    
    new_instance = User.objects.get_or_create (
                                        username = "tuyen" ,
                                                                                
                                        )[0]
    new_instance.set_password('tuyen')
    new_instance.save()
    print' cr ok 1 user'
    '''
    workbook = xlrd.open_workbook(path)
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
        profile.save()
def import_nguyen_nhan():
    nguyennhans= [u'MLL',u"Mất điện",u"Lỗi TD VTT",u"Mất cell",u"Mất 3 cell",u"Mất cell site remote",]
    for name in nguyennhans:
        nn = Nguyennhan.objects.get_or_create (
                                            Name = name,
                                            )[0]
        nn.Name_khong_dau = unidecode(name)
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
            print 'ignore this row becase not int cell' ,cellstt
            continue
        print 'stt',stt
        
        Full_name = read_excel_cell(worksheet, curr_row, 1)
        #First_name = 
        #Full_name_khong_dau = 
        Don_vi  = read_excel_cell(worksheet, curr_row, 4 )
        So_dien_thoai  =  read_excel_cell(worksheet, curr_row, 6)
        Nam_sinh  =  read_excel_cell(worksheet, curr_row,3 )
        try:
            date = datetime.datetime(1899, 12, 30)
            get_ = datetime.timedelta(int(Nam_sinh))
            get_col2 = str(date + get_)[:10]
            d = datetime.datetime.strptime(get_col2, '%Y-%m-%d')
            Nam_sinh = d.strftime('%d/%m/%Y')
            print d
            
        except:
            pass
        dia_chi_email = read_excel_cell(worksheet, curr_row, 5)
        #Thong_tin_khac  =  read_excel_cell(worksheet, curr_row, )
        
        print 'Full_name',Full_name
        print 'Don_vi',Don_vi
        print 'So_dien_thoai',So_dien_thoai
        print 'Nam_sinh',Nam_sinh
        print 'dia_chi_email',dia_chi_email
        
        doitac = Doitac.objects.get_or_create (
                                        Full_name = Full_name,

                                        )[0]
        
        #doitac.Full_name = 
        #First_name = 
        doitac.Full_name_khong_dau = unidecode (Full_name)
        doitac.Don_vi  = Don_vi.replace('-',' ')
        doitac.So_dien_thoai  =  So_dien_thoai
        doitac.Nam_sinh  =  Nam_sinh
        doitac.dia_chi_email = dia_chi_email
        doitac.save()
def grant_permission_to_group():
    content_type = ContentType.objects.get_for_model(Mll)
    permission = Permission.objects.get_or_create(codename='d4_create_truc_ca_permission',
                                           name='Can truc ca',
                                           content_type=content_type)
    group = Group.objects.get_or_create (name = 'truc_ca')[0]
    group.permissions =(permission)
def check_permission_of_group():
    for username in ['tund','lucvk']:
        user = User.objects.get_or_create (
                                            username = username,
    
                                            )[0]
        permission = Permission.objects.get_or_create(codename='d4_create_truc_ca_permission')
        print username,user.has_perm('drivingtest.d4_create_truc_ca_permission')
def import_database_4_cai (workbook):
    read_txt_database_3G(workbook)
    read_txt_database_2G(workbook)
    read_txt_database_3G_Site_Location(workbook)
    read_txt_database_2G_SRAN_HCM_Config(workbook)
def import_database_4_cai_new (runlists,workbook = None,is_available_file= True):
    all = ['Excel_3G','Excel_to_2g','Excel_2_3g','Excel_to_3g_location',]
    if not is_available_file:#must file upload ,workbook = workbook_upload
        if 'ALL' in runlists:
            for class_func_name in all:
                running_class = eval(class_func_name)
                running_class(workbook = workbook)
                if class_func_name in runlists:
                    runlists.remove(class_func_name)
            runlists.remove('ALL')
        #just remain alu,nsm, when alu,nsm,E in 1 file
        for class_func_name in runlists:
            running_class = eval(class_func_name)
            running_class(workbook = workbook)
    else: # get file from disk           
        if 'ALL' in runlists:
            path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_134.xlsx'
            workbook= xlrd.open_workbook(path)
            for class_func_name in all:
                running_class = eval(class_func_name)
                running_class(workbook = workbook)
                if class_func_name in runlists:
                    runlists.remove(class_func_name)
            runlists.remove('ALL')
        ericsson_lists = []
        for x in runlists:
            if x in all:
                ericsson_lists.append(x)
                runlists.remove(x)
        if ericsson_lists:
            path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_134.xlsx'
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
    if "RBS6" in Cabinet:
        type_rbs = "6000"
        path_directory = MEDIA_ROOT+ '/document/template_script/6000/'
    elif "RBS3" in Cabinet:
        path_directory = MEDIA_ROOT+ '/document/template_script/3000/'
        type_rbs = "3000"
    for root, dirs, files in os.walk(path_directory):
        for file in files:
            template_files.append(file)
    print template_files
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
                elif  save_type == 'temp 1 achive file':
                    achive_path = tempfile.TemporaryFile() # this time achive_path is template object file
                archive = zipfile.ZipFile(achive_path, 'w', zipfile.ZIP_DEFLATED)
            if luu_o_cung:
                if not os.path.exists(new_directory_path): os.makedirs(new_directory_path)
                filepath = new_directory_path  + fname
                save_file_to_disk(filepath,output,1)
            save_file_to_disk(filepath,output,1)
            archive.writestr(fname, output)
    return return_file_lists,achive_path,type_rbs # achive_path become tempt zip file

def create_TrangThaiCuaTram():
    path = MEDIA_ROOT+ '/document/trangthaicuatram.xls'
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(u'Sheet3')
    num_rows = worksheet.nrows - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        Name_trangthai = read_excel_cell(worksheet, curr_row, 1)
        instance = TrangThaiCuaTram.objects.get_or_create(Name = Name_trangthai)
        print instance[0],instance[1]
def create_ca_truc():
    for ca_truc_name in ['Moto','Alu','Huawei','Sran']:
        instance = Catruc.objects.create(Name=ca_truc_name)
        instance.save()
import shutil
def remove_folder(path):
    shutil.rmtree(path)
if __name__ == '__main__':
    #import_doi_tac()
    #create_user
    #grant_permission_to_group()
    #create_TrangThaiCuaTram()
    #create_ca_truc()
    #instance_site = Table3g.objects.get(id=19)
    #tao_script_r6000_w12(instance_site)
    # create user
    #create_user(MEDIA_ROOT+ '/document/DanhSachEmail.xls')
    #grant_permission_to_group()
    #check_permission_of_group()
    '''
   
    
    
    #ALU
    
    path = MEDIA_ROOT+ '/document/Database_ALU lot 1-2 -3 den NGAY  5-8-2015.xls'
    print path
    workbook = xlrd.open_workbook(path)
    read_txt_database_alu(path)
    
    
    '''
    #Lenh
    '''
    path = MEDIA_ROOT+ '/document/LENH KHAI BÁO EAS BTS HUAWEI.xls'
    print path
    workbook = xlrd.open_workbook(path)
    read_txt_database_command()
    '''
     
    '''
    '''
    #path = MEDIA_ROOT+ '/document/Ericsson_Database_Ver_134.xlsx'
    #print path
    #workbook_main= xlrd.open_workbook(path)
    #Excel_3G(workbook = workbook_main)  #chay truoc
    #Excel_to_2g(workbook = workbook_main)
    #Excel_to_3g_location(workbook = workbook_main)
    #Excel_to_2g_config_SRAN(workbook = workbook_main)
    '''
    path = MEDIA_ROOT+ '/document/NSN_Database_version_4.xlsx'
    print path
    workbook_main= xlrd.open_workbook(path)
    Excel_NSM(workbook = workbook_main)
    
    path = MEDIA_ROOT+ '/document/Database_ALU lot 1-2 -3 den NGAY  5-8-2015 .xls'
    print path
    workbook_main= xlrd.open_workbook(path)
    Excel_ALU(workbook = workbook_main)
    '''
    #import_database_4_cai_new(['Excel_3G','Excel_to_2g','Excel_to_2g_config_SRAN','Excel_to_3g_location','Excel_NSM','Excel_ALU'] )
    import_database_4_cai_new(['Excel_3G','Excel_to_2g'] )
    #import_nguyen_nhan()
    #tao_script_r6000_w12('CM6167')
    #remove_folder('/home/ductu/workspace/forum/media/for_user_download_folder/4583703')