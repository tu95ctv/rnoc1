# -*- coding: utf-8 -*- 
import os
import xlrd,datetime
from django.core.exceptions import MultipleObjectsReturned
from unidecode import unidecode
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from drivingtest.models import Table3g, Command3g, Mll, Doitac



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


        
def read_excel_cell(worksheet,curr_row,curr_cell):
    
    cell_value = worksheet.cell_value(curr_row, curr_cell)
    #print curr_cell, cell_value
    return cell_value      
global workbook   
def read_txt_database_3G(workbook):
    
    

    #datemodebook = workbook.datemode
    #print 'datemodebook',datemodebook
    worksheet = workbook.sheet_by_name(u'Ericsson 3G')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        print 'Row:', curr_row
        new_instance = Table3g.objects.get_or_create (
                                         site_id_3g= read_excel_cell(worksheet, curr_row,4)
                                        )[0]

        new_instance.License_60W_Power = read_excel_cell(worksheet, curr_row, 1) 
        new_instance.U900 = read_excel_cell(worksheet, curr_row, 2) 
        new_instance.site_id_2g_E= read_excel_cell(worksheet, curr_row, 5) 
        Ngay_Phat_Song_2G = read_excel_cell(worksheet, curr_row, 6) 

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
        
        new_instance.site_name_1= read_excel_cell(worksheet, curr_row, 7).replace("3G_","") 
        new_instance.site_name_2= read_excel_cell(worksheet, curr_row, 8).replace("3G_","")
        Ngay_Phat_Song_3G = read_excel_cell(worksheet, curr_row, 9)
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
        new_instance.BSC  = read_excel_cell(worksheet, curr_row, 10) 
        new_instance.Status = read_excel_cell(worksheet, curr_row, 11) 
        new_instance.Trans= read_excel_cell(worksheet, curr_row, 12) 
        new_instance.Cabinet = read_excel_cell(worksheet, curr_row, 13) 
        new_instance.Port = read_excel_cell(worksheet, curr_row, 14) 
        new_instance.RNC = read_excel_cell(worksheet, curr_row, 15) 
        try:
            new_instance.IUB_VLAN_ID = int(read_excel_cell(worksheet, curr_row, 16))
        except: 
            new_instance.IUB_VLAN_ID = read_excel_cell(worksheet, curr_row, 16)
        new_instance.IUB_SUBNET_PREFIX = read_excel_cell(worksheet, curr_row, 17) 
        new_instance.IUB_DEFAULT_ROUTER = read_excel_cell(worksheet, curr_row, 18) 
        new_instance.IUB_HOST_IP = read_excel_cell(worksheet, curr_row, 19)
        try: 
            new_instance.MUB_VLAN_ID = int(read_excel_cell(worksheet, curr_row, 20))
        except:
            new_instance.MUB_VLAN_ID = read_excel_cell(worksheet, curr_row, 20)
         
        new_instance.MUB_SUBNET_PREFIX = read_excel_cell(worksheet, curr_row, 21) 
        new_instance.MUB_DEFAULT_ROUTER = read_excel_cell(worksheet, curr_row, 22) 
        new_instance.MUB_HOST_IP = read_excel_cell(worksheet, curr_row, 23) 
        new_instance.UPE = read_excel_cell(worksheet, curr_row, 24) 
        new_instance.GHI_CHU = read_excel_cell(worksheet, curr_row, 25) 
        new_instance.Count_Province = read_excel_cell(worksheet, curr_row, 26) 
        new_instance.Count_RNC = read_excel_cell(worksheet, curr_row, 27) 
        new_instance.Cell_1_Site_remote = read_excel_cell(worksheet, curr_row, 28) 
        new_instance.Cell_2_Site_remote = read_excel_cell(worksheet, curr_row, 29) 
        new_instance.Cell_3_Site_remote = read_excel_cell(worksheet, curr_row, 30) 
        new_instance.Cell_4_Site_remote = read_excel_cell(worksheet, curr_row, 31) 
        new_instance.Cell_5_Site_remote = read_excel_cell(worksheet, curr_row, 32) 
        new_instance.Cell_6_Site_remote = read_excel_cell(worksheet, curr_row, 33) 
        new_instance.Cell_7_Site_remote = read_excel_cell(worksheet, curr_row, 34) 
        new_instance.Cell_8_Site_remote = read_excel_cell(worksheet, curr_row, 35) 
        new_instance.Cell_9_Site_remote = read_excel_cell(worksheet, curr_row, 36) 
        new_instance.save()

def read_txt_database_2G(workbook):
    #workbook = xlrd.open_workbook(path)

    worksheet = workbook.sheet_by_name(u'Database 2G')
    num_rows = worksheet.nrows - 1
    curr_row = 0
    while curr_row < num_rows:
        curr_row += 1
        print 'Row:', curr_row
        try:
            new_instance = Table3g.objects.get_or_create (
                                             site_name_1= read_excel_cell(worksheet, curr_row, 2).replace("2G_","")
                  
    
                                            )[0]
        except MultipleObjectsReturned:
            continue
            
        
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
        groupname =   read_excel_cell(worksheet, curr_row, 7)
        user = User.objects.get_or_create (
                                        username = username,

                                        )[0]
        group = Group.objects.get_or_create (name = groupname)[0]
        group.user_set.add(user)
        
        
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
if __name__ == '__main__':
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
    path = MEDIA_ROOT+ '/document/3G Database_Full_115.xlsx'
    print path
    workbook = xlrd.open_workbook(path)
    import_database_4_cai(workbook)
    import_doi_tac()