# -*- coding: utf-8 -*- 
import os
import xlrd,datetime
from django.core.exceptions import MultipleObjectsReturned
from unidecode import unidecode
from random import randint
import tempfile
import zipfile
SETTINGS_DIR = os.path.dirname(__file__)
MEDIA_ROOT = os.path.join(SETTINGS_DIR, 'media')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from drivingtest.models import Table3g, Command3g, Mll, Doitac, Nguyennhan,\
    Catruc, UserProfile, TrangThaiCuaTram



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
    
from django.template import Context,Template 
def tao_script_r6000_w12a(instance_site,ntpServerIpAddressPrimary = '10.213.227.98',ntpServerIpAddressSecondary = '10.213.227.102',\
                         ntpServerIpAddress1="10.213.235.134",ntpServerIpAddress2="10.213.235.135"):
    #save_type = 'save_to_disk_3_file'# 'save to disk 1 achive file',' temp 1 achive file'
    save_type = 'save to disk 1 achive file'
    #save_type = 'temp 1 achive file'
    
    now = datetime.datetime.now()
    site_id_3g= instance_site.site_id_3g
    instance_site.now = now
    return_file_lists = []
    achive_path=None
    #if save_type == 'temp 1 achive file':
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
            #print output
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
        #sum_w11w12__archive.writestr(arcname,achive_path.read())
        return return_file_lists,sum_w11w12_temp
def tao_script_r6000_w12(instance_site,ntpServerIpAddressPrimary = '10.213.227.98',ntpServerIpAddressSecondary = '10.213.227.102',\
                         ntpServerIpAddress1="10.213.235.134",ntpServerIpAddress2="10.213.235.135"):
    #save_type = 'save_to_disk_3_file'# 'save to disk 1 achive file',' temp 1 achive file'
    #save_type = 'save to disk 1 achive file'
    Cabinet = instance_site.Cabinet
    luu_o_cung = True
    save_type = 'temp 1 achive file'
    now = datetime.datetime.now()
    site_id_3g= instance_site.site_id_3g
    instance_site.now = now
    return_file_lists = []
    achive_path=None
    #if save_type == 'temp 1 achive file':
    #sum_w11w12_temp = tempfile.TemporaryFile() # this time achive_path is template object file
    #sum_w11w12__archive = zipfile.ZipFile(sum_w11w12_temp, 'w', zipfile.ZIP_DEFLATED)

    instance_site.id_n =  site_id_3g[-4:]
    instance_site.ntpServerIpAddressPrimary = ntpServerIpAddressPrimary
    instance_site.ntpServerIpAddressSecondary = ntpServerIpAddressSecondary
    instance_site.ntpServerIpAddress1 = ntpServerIpAddress1
    instance_site.ntpServerIpAddress2 = ntpServerIpAddress2
    
    #template_files = ['CM6167_IUB_W12_3.mo','CM6167_OAM_W12_1.xml','CM6167_SE-2carriers_2.xml']
    
    #template_files2 = ['IUB_W11_3.mo','OAM_W11_1.xml','SE-W11_2carriers_2.xml']
    #wversion_templates = [template_files]
    
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
    create_TrangThaiCuaTram()
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
    path = MEDIA_ROOT+ '/document/3G Database_Full_115.xlsx'
    print path
    workbook = xlrd.open_workbook(path)
    read_txt_database_2G(workbook)
    #import_database_4_cai(workbook)
    '''
    #import_doi_tac()
    
    #import_nguyen_nhan()
    #tao_script_r6000_w12('CM6167')
    #remove_folder('/home/ductu/workspace/forum/media/for_user_download_folder/4583703')