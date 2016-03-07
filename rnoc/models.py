# -*- coding: utf-8 -*-
print 'in model 2'
from django.db import models
from django.template.defaultfilters import default
from django.contrib.auth.models import User
from django import forms

#from drivingtest.forms import D4_DATETIME_FORMAT
D4_DATETIME_FORMAT = '%H:%M %d/%m/%Y'
        ##OMCKV2
class IPAddress_FieldNullable(models.IPAddressField):
    def get_db_prep_save(self,value,connection,prepared=False):
        return value or None   

class ThietBi(models.Model):
    Name = models.CharField(max_length=20,unique=True,null=True)
    ghi_chu_cho_thiet_bi = models.CharField(max_length=10000,blank=True)
    #tai_lieu_huong_dan = models.CharField(max_length=10000,blank=True)
    is_duoc_tao_truoc = models.BooleanField(default=False)
    def __unicode__(self):
        return self.Name  
class DoiTac(models.Model):
    First_name = models.CharField(max_length=20,null=True,blank=True)
    Full_name = models.CharField(max_length=80)
    Full_name_khong_dau = models.CharField(max_length=80,null=True)
    Don_vi  = models.CharField(max_length=80,null=True,blank=True)
    So_dien_thoai  = models.CharField(max_length=80,null=True,blank=True)
    Nam_sinh  = models.CharField(max_length=80,null=True,blank=True)
    dia_chi_email = models.EmailField(max_length=80,null=True,blank=True)
    Thong_tin_khac  = models.CharField(max_length=80,null=True,blank=True)
    
    def __unicode__(self):
        return self.Full_name    
class DuAn(models.Model):
    Name=models.CharField(max_length=150)
    Mota = models.CharField(max_length=1330,null=True,blank=True)
    type_2G_or_3G = models.CharField(max_length=2,blank=True)
    thoi_diem_bat_dau= models.DateTimeField(null=True,blank=True,verbose_name="thời điểm bắt đầu")#3
    thoi_diem_ket_thuc= models.DateTimeField(null=True,blank=True,verbose_name="thời điểm kết thúc")#3
    doi_tac_du_an = models.ManyToManyField(DoiTac,null=True,blank=True)
    is_duoc_tao_truoc = models.BooleanField(default = False)
    def __unicode__(self):
        return self.Name

class Tram(models.Model):
    License_60W_Power = models.NullBooleanField(blank = True) #1
    U900 = models.NullBooleanField(blank = True,null=True)#2
    Site_ID_3G= models.CharField(max_length=80,null=True,blank = True)#3
    Ngay_Phat_Song_2G = models.DateField(null=True,blank = True,verbose_name="Ngày phát sóng 2G")#5
    Ngay_Phat_Song_3G = models.DateField(null=True,blank = True,)#8
    Site_Name_1= models.CharField(max_length=80,null=True)
    Site_Name_2= models.CharField(max_length=80,null=True,blank = True)
    #BSC  = models.CharField(max_length=15,null=True,blank = True,)#9
    #Site_ID_2G_E = models.CharField(max_length=80,null=True,blank = True,)#35
    Status = models.CharField(max_length=50,null=True,blank = True,)#10
    Project_Text = models.CharField(max_length=100,null=True,blank = True,)#10
    Trans= models.CharField(max_length=40,null=True,blank = True,)#11
    Cabinet = models.ForeignKey(ThietBi,null=True,blank = True,related_name="Tramcuathietbis")#12
    Port = models.CharField(max_length=40,null=True,blank = True,)#13
    RNC = models.CharField(max_length=40,null=True,blank = True,)#14
    IUB_VLAN_ID = models.CharField(max_length=4,null=True,blank = True)#15
    IUB_SUBNET_PREFIX = IPAddress_FieldNullable(max_length=40,null=True,blank = True,)#16
    IUB_DEFAULT_ROUTER = IPAddress_FieldNullable(max_length=40,null=True,blank = True)#17
    IUB_HOST_IP = IPAddress_FieldNullable(null=True,blank = True)#18
    MUB_VLAN_ID = models.CharField(max_length=4,null=True,blank = True)#19
    MUB_SUBNET_PREFIX = IPAddress_FieldNullable(max_length=40,null=True,blank = True,)#20
    MUB_DEFAULT_ROUTER = IPAddress_FieldNullable(max_length=40,null=True,blank = True)#21
    MUB_HOST_IP = IPAddress_FieldNullable(max_length=40,null=True,blank = True)#22
    UPE = models.CharField(max_length=140,null=True,blank = True,)#23
    GHI_CHU = models.CharField(max_length=100,null=True,blank = True,)#24
    dia_chi_3G = models.CharField(max_length=200,null=True,blank = True,)#35
    Count_Province = models.CharField(max_length=40,null=True,blank = True,)#25
    Count_RNC = models.CharField(max_length=40,null=True,blank = True,)#26
    Cell_1_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#27
    Cell_2_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#28
    Cell_3_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#29
    Cell_4_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#30
    Cell_5_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#31
    Cell_6_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#32
    Cell_7_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#33
    Cell_8_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#34
    Cell_9_Site_remote = models.CharField(max_length=40,null=True,blank = True,)#35
    Cell_K_U900_PSI =  models.CharField(max_length=40,null=True,blank = True,)#35
    dia_chi_2G = models.CharField(max_length=200,null=True,blank = True,)#35
    BSC_2G = models.CharField(max_length=30,null=True,blank = True,)#35
    Site_ID_2G = models.CharField(max_length=80,null=True,blank = True,)#35
    LAC_2G = models.CharField(max_length=20,null=True,blank = True,)#35
    Nha_Tram = models.CharField(max_length=20,null=True,blank = True,)#35
    Ma_Tram_DHTT = models.CharField(max_length=20,null=True,blank = True,)#35
    Cell_ID_2G = models.CharField(max_length=20,null=True,blank = True,)#35
    cau_hinh_2G = models.CharField(max_length=20,null=True,blank = True,)#35
    nha_san_xuat_2G = models.ForeignKey(ThietBi,null=True,blank = True,)#35
    TG = models.CharField(max_length=150,null=True,blank = True,)#35
    TRX_DEF = models.CharField(max_length=50,null=True,blank = True,)#35
    ntpServerIpAddressPrimary = models.CharField(max_length=20,null=True,blank = True,)
    ntpServerIpAddressSecondary = models.CharField(max_length=20,null=True,blank = True,)
    ntpServerIpAddress1 = models.CharField(max_length=20,null=True,blank = True,)
    ntpServerIpAddress2 = models.CharField(max_length=20,null=True,blank = True,)
    du_an = models.ManyToManyField(DuAn,null=True,blank=True)
    eNodeB_Name = models.CharField(max_length=40,null=True,blank = True,)#35
    eNodeB_ID_DEC = models.CharField(max_length=6,null=True,blank = True)
    eNodeB_Type = models.ForeignKey(ThietBi,null=True,blank = True,related_name='ThietBi_of_eNodeB')#12
    def __unicode__(self):
        if self.Site_Name_1:
            return self.Site_Name_1
        else:
            return str(self.id)
class EditHistory(models.Model):
    modal_name = models.CharField(max_length=50)
    edited_object_id = models.IntegerField()
    thanh_vien = models.ForeignKey(User,null=True,blank=True,verbose_name="Thành viên sửa")
    ly_do_sua = models.CharField(max_length=250)
    edit_datetime= models.DateTimeField(null=True,blank=True)#3
class Nguyennhan (models.Model):
    Name = models.CharField(max_length=150,unique=True)
    #Name_khong_dau = models.CharField(max_length=150)
    Ghi_chu = models.CharField(max_length=10000,null=True,blank=True)
    #stylecss_name = models.CharField(max_length=100,null=True,blank=True)
    #color_code = models.CharField(max_length=15,null=True,blank=True)
    ngay_gio_tao= models.DateTimeField(null=True,blank=True)#3
    def __unicode__(self):
        return self.Name
class CaTruc(models.Model):
    Name = models.CharField(max_length=30,unique=True)
    ghi_chu = models.CharField(max_length=10000,null=True,blank=True)
    def __unicode__(self):
        return self.Name
class TrangThai(models.Model):
    Name = models.CharField(max_length=100,unique=True)
    ghi_chu = models.CharField(max_length=10000,null=True,blank=True)
    stylecss_name = models.CharField(max_length=100,null=True,blank=True)
    color_code = models.CharField(max_length=15,null=True,blank=True)
    is_cap_nhap_gio_tot =models.BooleanField()
    def __unicode__(self):
        return self.Name
class FaultLibrary(models.Model):
    Name=models.CharField(max_length=100,unique=True)
    diversity = models.CharField(max_length=10,blank=True,null=True)
    ghi_chu =models.CharField(max_length=10000,blank=True)
    ngay_gio_tao= models.DateTimeField(blank=True,verbose_name="ngày giờ tạo")#3
    def __unicode__(self):
        return self.Name
class Mll(models.Model):
    subject= models.CharField(max_length=50)
    site_name= models.CharField(max_length=50,null=True,blank=True)#3
    thiet_bi= models.ForeignKey(ThietBi,null=True,blank = True)#12
    nguyen_nhan = models.ForeignKey(Nguyennhan,related_name="Mlls",null=True,blank=True,verbose_name="nguyên nhân")
    du_an = models.ForeignKey(DuAn,related_name="DuAns",null=True,blank=True,verbose_name="dự án")
    ung_cuu = models.BooleanField(verbose_name="ư/c")
    thanh_vien = models.ForeignKey(User,null=True,blank=True,verbose_name="Thành viên tạo")
    ca_truc = models.ForeignKey(CaTruc,blank=True,null=True)
    last_edit_member = models.ForeignKey(User,null=True,blank=True,related_name = 'mll_set_of_last_edit_member')
    last_update_time= models.DateTimeField(null=True,blank=True,verbose_name="update_time")#3
    gio_mat= models.DateTimeField(blank=True,verbose_name="giờ mất")#3
    gio_tot= models.DateTimeField(null=True,blank=True,verbose_name="giờ tốt")#3
    trang_thai = models.ForeignKey(TrangThai,null=True,blank=True,verbose_name="trạng thái")
    specific_problem= models.CharField(max_length=1000,null=True,blank=True)#3
    giao_ca = models.BooleanField(verbose_name="g/ca")
    nghiem_trong = models.BooleanField(verbose_name="N/trọng")
    def __unicode__(self):
        return self.subject
class SpecificProblem(models.Model):
    fault = models.ForeignKey(FaultLibrary,null=True,blank=True)
    object_name = models.CharField(max_length=200,null=True,blank=True)
    mll = models.ForeignKey(Mll,related_name ='specific_problems')
    def __unicode__(self):
        return ((self.fault.Name  + '**' ) if self.fault else '')  + self.object_name
    
class ThaoTacLienQuan(models.Model):
    name = models.CharField(unique=True,max_length=100)
    def __unicode__(self):
        return self.name
        
class Comment(models.Model):
    datetime= models.DateTimeField(blank=True,verbose_name="nhập giờ")
    doi_tac = models.ForeignKey(DoiTac,related_name="Comments",null=True,blank=True,verbose_name="đối tác")
    comment= models.CharField(max_length=128,null=True,blank=True,)# if bo blank=False mac dinh se la true chelp_text="add comment here",
    trang_thai = models.ForeignKey(TrangThai,blank=True,verbose_name="Trạng thái")
    thao_tac_lien_quan = models.ManyToManyField(ThaoTacLienQuan,blank=True,null=True)
    thanh_vien = models.ForeignKey(User,blank=True,verbose_name="thành viên")
    mll = models.ForeignKey(Mll,related_name="comments",blank=True)
    def __unicode__(self):
        return self.comment
class SearchHistory(models.Model):
    query_string= models.CharField(max_length=200,null=True,blank=True)#3
    #thanh_vien = models.CharField(max_length=40,null=True,blank=True)#3
    thanh_vien = models.ForeignKey(User,null=True,blank=True)#3
    search_datetime= models.DateTimeField(null=True,blank=True)#3
    ghi_chu= models.CharField(max_length=400,null=True,blank=True)#3
class Lenh(models.Model):
    command= models.CharField(max_length=200,unique=True)#3
    ten_lenh= models.CharField(max_length=200,null=True,blank=True)#3
    mo_ta= models.CharField(max_length=200,null=True,blank=True)#3
    def __unicode__(self):
        return self.command
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    ca_truc= models.ForeignKey(CaTruc,null=True,)
    so_dien_thoai = models.CharField(max_length=20)
    config_ca_filter_in_mll_table = models.ManyToManyField(CaTruc,related_name='userprofile_ca_filter',blank=True,null=True)
    color_code = models.CharField(max_length=15,null=True,blank=True)
    def __unicode__(self):
        return self.user.username


from django.db.models import CharField
H_Field = [f.name for f in SearchHistory._meta.fields if isinstance(f, CharField) ]
