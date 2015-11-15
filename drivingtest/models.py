# -*- coding: utf-8 -*-
print 'in model 2'
from django.db import models
from django.template.defaultfilters import default
from django.contrib.auth.models import User
from django import forms

#from drivingtest.forms import D4_DATETIME_FORMAT
D4_DATETIME_FORMAT = '%H:%M %d/%m/%Y'
postdict ={}
class PollManager(models.Manager):
    def with_counts(self):
        from django.db import connection
        cursor = connection.cursor()
        
        
        cursor.execute("""
            SELECT p.id, p.question, p.poll_date, COUNT(*)
            FROM polls_opinionpoll p, polls_response r
            WHERE p.id = r.poll_id
            GROUP BY p.id, p.question, p.poll_date
            ORDER BY p.poll_date DESC""")
        
        
        result_list = []
        model_name = self.model.__name__
        for row in cursor.fetchall():
            p = self.model(id=row[0], question=row[1], poll_date=row[2])
            p.num_responses = row[3]
            result_list.append(p)
        return result_list
class Category(models.Model):
    name= models.CharField(max_length=128, unique=True)
    children = models.ManyToManyField('self',symmetrical=False, null=True, blank=True)
    cate_encode_url= models.CharField(max_length=128, unique=True, blank=True)
    is_show_on_home_page = models.NullBooleanField(blank=True)
    is_show_on_main_nav = models.NullBooleanField(blank=True)
    arrange_order_display = models.IntegerField(null=True,blank=True)
    number_product_display_on_homepage = models.IntegerField(default=4,null=True,blank=True)
    is_parent_cate = models.NullBooleanField(default=False,blank=True)
    
    
    
    def __unicode__(self):
        return self.name
class Linhkien(models.Model):
    name= models.CharField(max_length=128, unique=True)
    linhkien_encode_url= models.CharField(max_length=128, unique=True, blank=True)
    category = models.ManyToManyField(Category, blank=True) 
    price = models.IntegerField()
    old_price = models.IntegerField(null=True)
    show_old_price = models.NullBooleanField()
    is_best_sale = models.IntegerField(null=True)
    is_promote_sale = models.IntegerField(null=True)
    arrange_order = models.IntegerField()
    description = models.CharField(max_length=8500)
    icon_picture = models.ImageField(upload_to='img/product/', blank=True)
    borrowed_icon_picture = models.URLField()
    picture = models.ImageField(upload_to='img/product/', blank=True,max_length=428)
    borrowed_picture = models.URLField(max_length=428)
    pub_date = models.DateTimeField(null=True)
    last_edited_date = models.DateTimeField(null=True)
    view_number = models.IntegerField(default=0)
    like_number = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
class thongbao(object):
    thongbao = 'chua co thong bao j'
    log = 'chua co log gi'
    #def __init__(self):        
class OwnContact(models.Model):
    dia_chi= models.CharField(max_length=128)
    ten= models.CharField(max_length=128)
    email= models.CharField(max_length=128)
    sodienthoai= models.CharField(max_length=128)  
    
    cn2_dia_chi= models.CharField(max_length=128,null=True,blank=True)
    cn2_ten= models.CharField(max_length=128,null=True,blank=True)
    cn2_email= models.CharField(max_length=128,null=True,blank=True)
    cn2_sodienthoai= models.CharField(max_length=128,null=True,blank=True) 
    cn2_google_map = models.CharField(max_length=900,null=True,blank=True)
    
    
    is_show_promote_product = models.NullBooleanField()
    is_best_sale_product = models.NullBooleanField()
    google_map = models.CharField(max_length=900,null=True)
    slogan = models.CharField(max_length=900,null=True)
    about_us = models.CharField(max_length=900,null=True)
    number_product_san_pham = models.IntegerField(default=6)
    number_product_promote = models.IntegerField(default=4)
    number_product_bestsell = models.IntegerField(default=4)
    base_title= models.CharField(max_length=128)
    banner_url = models.TextField(max_length=222)
    icon_path =  models.TextField(max_length=120)
    script_google_analytics = models.CharField(max_length=900,null=True)
    script_google_analytics_acc2 = models.CharField(max_length=900,null=True)
    webpage= models.CharField(max_length=80,null=True)
    facebook_page=models.CharField(max_length=80,null=True)
    mainheader_color = models.CharField(max_length=45,null=True)
    footer_custom_color = models.CharField(max_length=45,null=True,blank=True)
    mainheader_type = models.CharField(max_length=45,null=True)
    banner1_url = models.URLField(null=True)
    banner2_url = models.URLField(null=True)
    banner_height= models.IntegerField(default=200,null=True)
    
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
    def formfield(self, **kwargs):
        return super(UpcappedModelField, self).formfield(form_class=forms.CharField, 
                         label=self.verbose_name, **kwargs)
class Doitac (models.Model):
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
class Duan(models.Model):
    Name=models.CharField(max_length=150)
    Mota = models.CharField(max_length=1330,null=True)
    type_2G_or_3G = models.CharField(max_length=2)
    thoi_diem_bat_dau= models.DateTimeField(null=True,blank=True,verbose_name="thời điểm bắt đầu")#3
    thoi_diem_ket_thuc= models.DateTimeField(null=True,blank=True,verbose_name="thời điểm kết thúc")#3
    doi_tac_du_an = models.ManyToManyField(Doitac,null=True,blank=True)
    def __unicode__(self):
        return self.Name
class Table3g(models.Model):
    License_60W_Power = models.NullBooleanField(blank = True) #1
    U900 = models.NullBooleanField(blank = True,null=True)#2
    site_id_3g= models.CharField(max_length=80,null=True,blank = True)#3
    Ngay_Phat_Song_2G = models.DateField(null=True,blank = True,verbose_name="Ngày phát sóng 2G")#5
    Ngay_Phat_Song_3G = models.DateField(null=True,blank = True,)#8
    site_name_1= models.CharField(max_length=80,null=True,blank = True,)
    site_name_2= models.CharField(max_length=80,null=True,blank = True,)
    BSC  = models.CharField(max_length=15,null=True,blank = True,)#9
    site_id_2g_E = models.CharField(max_length=80,null=True,blank = True,)#35
    Status = models.CharField(max_length=50,null=True,blank = True,)#10
    ProjectE = models.CharField(max_length=100,null=True,blank = True,)#10
    Trans= models.CharField(max_length=40,null=True,blank = True,)#11
    Cabinet = models.CharField(max_length=40,null=True,blank = True,)#12
    Port = models.CharField(max_length=40,null=True,blank = True,)#13
    RNC = models.CharField(max_length=40,null=True,blank = True,)#14
    IUB_VLAN_ID = models.CharField(max_length=4,null=True,blank = True,verbose_name="IUB_VLAN_ID")#15
    IUB_SUBNET_PREFIX = models.IPAddressField(max_length=40,null=True,blank = True,)#16
    IUB_DEFAULT_ROUTER = models.IPAddressField(max_length=40,null=True,blank = True,verbose_name="IUB_DEFAULT_ROUTER")#17
    IUB_HOST_IP = models.IPAddressField(null=True,blank = True,verbose_name="IUB_HOST_IP")#18
    MUB_VLAN_ID = models.CharField(max_length=4,null=True,blank = True,verbose_name="MUB_VLAN_ID")#19
    MUB_SUBNET_PREFIX = models.IPAddressField(max_length=40,null=True,blank = True,)#20
    MUB_DEFAULT_ROUTER = models.IPAddressField(max_length=40,null=True,blank = True,verbose_name="MUB_DEFAULT_ROUTER")#21
    MUB_HOST_IP = models.IPAddressField(max_length=40,null=True,blank = True,verbose_name="MUB_HOST_IP")#22
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
    dia_chi_2G = models.CharField(max_length=200,null=True,blank = True,)#35
    BSC_2G = models.CharField(max_length=30,null=True,blank = True,)#35
    site_ID_2G = models.CharField(max_length=80,null=True,blank = True,)#35
    LAC_2G = models.CharField(max_length=20,null=True,blank = True,)#35
    Nha_Tram = models.CharField(max_length=20,null=True,blank = True,)#35
    Ma_Tram_DHTT = models.CharField(max_length=20,null=True,blank = True,)#35
    Cell_ID_2G = models.CharField(max_length=20,null=True,blank = True,)#35
    cau_hinh_2G = models.CharField(max_length=20,null=True,blank = True,)#35
    nha_san_xuat_2G = models.CharField(max_length=40,null=True,blank = True,)#35
    TG = models.CharField(max_length=150,null=True,blank = True,)#35
    TRX_DEF = models.CharField(max_length=50,null=True,blank = True,)#35
    ntpServerIpAddressPrimary = models.CharField(max_length=20,null=True,blank = True,)
    ntpServerIpAddressSecondary = models.CharField(max_length=20,null=True,blank = True,)
    ntpServerIpAddress1 = models.CharField(max_length=20,null=True,blank = True,)
    ntpServerIpAddress2 = models.CharField(max_length=20,null=True,blank = True,)
    du_an = models.ManyToManyField(Duan,null=True,blank=True)
    def __unicode__(self):
        if self.site_name_1:
            return self.site_name_1
        else:
            return str(self.id)
class Nguyennhan (models.Model):
    Name = models.CharField(max_length=150)
    Name_khong_dau = models.CharField(max_length=150)
    Ghi_chu = models.CharField(max_length=150) 
    def __unicode__(self):
        return self.Name
class Catruc(models.Model):
    Name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.Name
class TrangThaiCuaTram(models.Model):
    Name=models.CharField(max_length=30)
    Mota = models.CharField(max_length=1330,null=True,blank=True)
    def __unicode__(self):
        return self.Name

class Mll(models.Model):
    
    subject= models.CharField(max_length=50)
    site_name= models.CharField(max_length=50,null=True,blank=True)#3
    thiet_bi= models.CharField(max_length=50,null=True,blank=True,verbose_name="thiết bị")
    nguyen_nhan = models.ForeignKey(Nguyennhan,related_name="Mlls",null=True,blank=True,verbose_name="nguyên nhân")
    du_an = models.ForeignKey(Duan,related_name="Duans",null=True,blank=True,verbose_name="dự án")
    ung_cuu = models.BooleanField(verbose_name="ứng cứu")
    thanh_vien = models.ForeignKey(User,null=True,blank=True,)
    ca_truc = models.ForeignKey(Catruc,blank=True,null=True)
    #gio_nhap= models.DateTimeField(null=True,blank=True,verbose_name="giờ nhập")#3
    last_update_time= models.DateTimeField(null=True,blank=True,verbose_name="update_time")#3
    gio_mat= models.DateTimeField(null=True,blank=True,verbose_name="giờ mất")#3
    gio_tot= models.DateTimeField(null=True,blank=True,verbose_name="giờ tốt")#3
    #gio_bao_uc= models.DateTimeField(null=True,blank=True,verbose_name="giờ bao uc")#3
    trang_thai = models.ForeignKey(TrangThaiCuaTram,null=True,blank=True,verbose_name="trạng thái")
    specific_problem= models.CharField(max_length=1000,null=True,blank=True)#3
    #doi_tac = models.ForeignKey(Doitac,related_name="Mlls",null=True,blank=True,verbose_name="đối tác")
    #cac_buoc_xu_ly= models.CharField(max_length=1000,null=True,blank=True,verbose_name="các bước xử lý")#3
    giao_ca = models.BooleanField(verbose_name="giao ca")
    #comments = models.ManyToManyField(CommentForMLL,null=True,blank=True)
    def __unicode__(self):
        return self.thiet_bi

class CommentForMLL(models.Model):
    datetime= models.DateTimeField(blank=True,verbose_name="nhập giờ")
    doi_tac = models.ForeignKey(Doitac,related_name="CommentForMLLs",null=True,blank=True,verbose_name="đối tác")
    comment= models.CharField(max_length=128,null=True,blank=True,)# if bo blank=False mac dinh se la true chelp_text="add comment here",
    trang_thai = models.ForeignKey(TrangThaiCuaTram,blank=True,verbose_name="Trạng thái")
    thanh_vien = models.ForeignKey(User,blank=True,verbose_name="thành viên")
    mll = models.ForeignKey(Mll,related_name="comments",blank=True)
    def __unicode__(self):
        return self.comment
class SearchHistory(models.Model):
    query_string= models.CharField(max_length=200,null=True,blank=True)#3
    thanh_vien = models.CharField(max_length=40,null=True,blank=True)#3
    search_datetime= models.DateTimeField(null=True,blank=True)#3
    ghi_chu= models.CharField(max_length=400,null=True,blank=True)#3
class Command3g(models.Model):
    command= models.CharField(max_length=200,unique=True)#3
    ten_lenh= models.CharField(max_length=200,null=True,blank=True)#3
    mo_ta= models.CharField(max_length=200,null=True,blank=True)#3
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    ca_truc= models.ForeignKey(Catruc,null=True,)
    so_dien_thoai = models.CharField(max_length=20)
    def __unicode__(self):
        return self.user.username




   
class Ulnew(models.Model):
    title= models.CharField(max_length=200,unique=True,verbose_name='model verbose name')#3
    category= models.CharField(max_length=200)#3
    description= models.CharField(max_length=50000,null=True,blank=True)#3
    date = models.DateTimeField(auto_now_add=True, blank=True)
    
    rg= models.CharField(max_length=2000,null=True,blank=True)#3
    ul= models.CharField(max_length=2000,null=True,blank=True)#3
    up= models.CharField(max_length=2000,null=True,blank=True)#3
    
    myrg= models.CharField(max_length=2000,null=True,blank=True)#3
    myul= models.CharField(max_length=2000,null=True,blank=True)#3
    myup= models.CharField(max_length=2000,null=True,blank=True)#3
    def __unicode__(self):
        return self.title
class UlDaPost(models.Model):
    title= models.CharField(max_length=200,unique=True)#3
    posted_forum = models.ManyToManyField('ForumTable', through='PostLogDaPost',related_name='Uldapost_back')
class ForumTable(models.Model):
    url= models.CharField(max_length=100,null=True,blank=True)#3
    postedLog_dat_tenJ_cungduoc_link = models.ManyToManyField('Ulnew', through='PostLog',related_name='forumback')
    uname= models.CharField(max_length=100,null=True,blank=True)#3
    passwd= models.CharField(max_length=100,null=True,blank=True)#3
    newthread_url= models.CharField(max_length=100,null=True,blank=True)#3
    music= models.CharField(max_length=100,null=True,blank=True)#3
    tv_show = models.CharField(max_length=100,null=True,blank=True)#3
    movie= models.CharField(max_length=100,null=True,blank=True)#3
    HDmovie= models.CharField(max_length=100,null=True,blank=True)#3
    software= models.CharField(max_length=100,null=True,blank=True)#3
    game= models.CharField(max_length=100,null=True,blank=True)#3
    anime= models.CharField(max_length=100,null=True,blank=True)#3
    mobile= models.CharField(max_length=100,null=True,blank=True)#3
    ebook= models.CharField(max_length=100,null=True,blank=True)#3
    def __unicode__(self):
        return self.url
class AdminUl (models.Model):
    ul_order = models.IntegerField(default=1)
    rg_order = models.IntegerField(default=2)
    up_order = models.IntegerField(default=3)
    show_not_my_link = models.BooleanField (default=True)
class PostLog(models.Model):
    forum =models.ForeignKey(ForumTable,related_name='postLog')
    Ulnew =models.ForeignKey(Ulnew,related_name='postLog')
    pested_link = models.CharField(max_length=100,null=True,blank=True)
    posted_datetime =  models.DateTimeField(auto_now_add=True, blank=True)
    
class PostLogDaPost(models.Model):
    forum =models.ForeignKey(ForumTable,related_name='PostLogDaPost')
    UlDaPost =models.ForeignKey(UlDaPost,related_name='PostLogDaPost')
    posted_link = models.CharField(max_length=100,null=True,blank=True)
    posted_datetime =  models.DateTimeField(auto_now_add=True, blank=True)
class LeechSite (models.Model):
    url= models.CharField(max_length=100,null=True,blank=True)#3
    music= models.CharField(max_length=100,null=True,blank=True)#3
    tv_show = models.CharField(max_length=100,null=True,blank=True)#3
    movie= models.CharField(max_length=100,null=True,blank=True)#3
    HDmovie= models.CharField(max_length=100,null=True,blank=True)#3
    software= models.CharField(max_length=100,null=True,blank=True)#3
    game= models.CharField(max_length=100,null=True,blank=True)#3
    anime= models.CharField(max_length=100,null=True,blank=True)#3
    mobile= models.CharField(max_length=100,null=True,blank=True)#3
    ebook= models.CharField(max_length=100,null=True,blank=True)#3
print 'ban lai vo model module'
from django.db.models import CharField,IPAddressField

FNAME = [f.name for f in Table3g._meta.fields]
H_Field = [f.name for f in SearchHistory._meta.fields if isinstance(f, CharField) ]
