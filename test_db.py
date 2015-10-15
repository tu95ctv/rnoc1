import os
from xu_ly_db_3g import read_line
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')

from drivingtest.forms import Mllform

from django.db.models import CharField
from drivingtest.models import Ulnew , ForumTable, PostLog, Table3g,CommentForMLL,Mll
instance_site = Table3g.objects.get(site_id_3g="CM6167")
a= instance_site.site_id_3g
ntpServerIpAddressPrimary = '10.213.227.98'
ntpServerIpAddressSecondary = '10.213.227.102'
sector = 0
for i in range(9):
    fname = u'Cell_%s_Site_remote'%(i+1)
    val = getattr(instance_site,fname)
    if val:
        sector = sector +1
print fname,val,sector

print a[-4:]
paths1_f1 = '/home/ductu/Documents/CM6167/CM6167_IUB_W12_3.mo'
paths2_f1 = '/home/ductu/Documents/KG5901/KG5901_IUB_W12_3.mo'
paths4_f1 = '/home/ductu/workspace/forum/media/for_user_download_folder/5484692/KG5901_IUB_W12_3.mo'
paths3_f1 = '/home/ductu/Documents/CT5144_3000/CT5144_Iub_FullIP_RBS3000_3.mo'

paths1_f2 = '/home/ductu/Documents/CM6167/CM6167_OAM_W12_1.xml'
paths2_f2 = '/home/ductu/Documents/KG5901/KG5901_OAM_W12_1.xml'
paths4_f2 = '/home/ductu/workspace/forum/media/for_user_download_folder/5484692/KG5901_OAM_W12_1.xml'


paths1_f3 = '/home/ductu/Documents/CM6167/CM6167_SE-2carriers_2.xml'
paths2_f3 = '/home/ductu/Documents/KG5901/KG5901_SE-2carriers_2.xml'
paths4_f3 = '/home/ductu/workspace/forum/media/for_user_download_folder/5484692/CM6167_SE-2carriers_2.xml'


s1f1 = '/home/ductu/Documents/d4/AG4226_3000_port quang_fullIP/AG4226_Iub_FullIP_RBS3000_3.mo'
s1f2 = '/home/ductu/Documents/d4/AG4226_3000_port quang_fullIP/AG4226_OAM_FullIP_RBS3000_1.xml'
s1f3 = '/home/ductu/Documents/d4/AG4226_3000_port quang_fullIP/AG4226_SE_RBS3000_2.xml'


s2f1 = '/home/ductu/Documents/d4/AG4218_3000_portE/AG4218_Iub_FullIP_RBS3000_3.mo'
s2f2 = '/home/ductu/Documents/d4/AG4218_3000_portE/AG4218_OAM_FullIP_RBS3000_1.xml'
s2f3 = '/home/ductu/Documents/d4/AG4218_3000_portE/AG4218_SE_RBS3000_2.xml'

s3f1 = '/home/ductu/Documents/d4/vt2766/VT2766_Iub_FullIP_RBS3000_3.mo'
s3f2 = '/home/ductu/Documents/d4/vt2766/VT2766_OAM_FullIP_RBS3000_1.xml'
s3f3 = '/home/ductu/Documents/d4/vt2766/VT2766_SE_RBS3000_2.xml'

s3900f1 = '/home/ductu/Documents/d4/vt2766_u900_w12/VT2766_IUB_W12_3.mo'
s3900f2 = '/home/ductu/Documents/d4/vt2766_u900_w12/VT2766_OAM_W12_1.xml'
s3900f3 = '/home/ductu/Documents/d4/vt2766_u900_w12/VT2766_SE_U900_W13_2.xml'

site4file1='/home/ductu/Documents/d5/6000_site1_w11_dien/HC2276_IUB_W11_3.mo'
site5file1='/home/ductu/Documents/d5/6000_s2_w11_portquang/BD3166_IUB_W11_3.mo'

site4file2='/home/ductu/Documents/d5/6000_site1_w11_dien/HC2276_OAM_W11_1.xml'
site5file2='/home/ductu/Documents/d5/6000_s2_w11_portquang/BD3166_OAM_W11_1.xml'

site4file3='/home/ductu/Documents/d5/6000_site1_w11_dien/HC2276_SE-2carriers_2.xml'
site5file3='/home/ductu/Documents/d5/6000_s2_w11_portquang/BD3166_SE-2carriers_2.xml'

sitedownloadf1 = '/home/ductu/workspace/forum/media/for_user_download_folder/5484692/AG4301_Iub_FullIP_RBS3000_3.mo'
sitedownloadf2 = '/home/ductu/workspace/forum/media/for_user_download_folder/5484692/AG4301_OAM_FullIP_RBS3000_1.xml'
sitedownloadf3 = '/home/ductu/workspace/forum/media/for_user_download_folder/5484692/AG4301_SE_RBS3000_2.xml'

siteU900f1='/home/ductu/Documents/d5/U900_6000_site1_portdien/HC2352_IUB_W12_3.mo'
siteU900f2='/home/ductu/Documents/d5/U900_6000_site1_portdien/HC2352_OAM_W12_1.xml'
siteU900f3='/home/ductu/Documents/d5/U900_6000_site1_portdien/HC2352_SE_U900_W13_2.xml'

siteU900_2f1='/home/ductu/Documents/d5/U900_6000_site2_portquagn_TNB/BD3184_IUB_W12_3.mo'
siteU900_2f2='/home/ductu/Documents/d5/U900_6000_site2_portquagn_TNB/BD3184_OAM_W12_1.xml'
siteU900_2f3='/home/ductu/Documents/d5/U900_6000_site2_portquagn_TNB/BD3184_SE_U900_W13_2.xml'

s1_3000_f1 = '/home/ductu/Documents/d5/3000_s1_fo_7/AG4301_Iub_FullIP_RBS3000_3.mo'
s1_3000_f2 = '/home/ductu/Documents/d5/3000_s1_fo_7/AG4301_OAM_FullIP_RBS3000_1.xml'
s1_3000_f3 = '/home/ductu/Documents/d5/3000_s1_fo_7/AG4301_SE_RBS3000_2.xml'

s2_3000_f1 = '/home/ductu/Documents/d5/3000_s2_dien_6/VT2666_Iub_FullIP_RBS3000_3.mo'
s2_3000_f2 = '/home/ductu/Documents/d5/3000_s2_dien_6/VT2666_OAM_FullIP_RBS3000_1.xml'
s2_3000_f3 = '/home/ductu/Documents/d5/3000_s2_dien_6/VT2666_SE_RBS3000_2.xml'

#fo = open(paths1_f1,'r')
a = read_line(sitedownloadf3,'\r\n')
b = read_line(s1_3000_f3,'\r\n')
zipab = zip(a,b)
for c,x in enumerate(zipab):
    if x[0]!=x[1]:
        print 'line%s'%(c+1),x
