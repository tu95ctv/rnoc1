# -*- coding: utf-8 -*- 
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from django.contrib.auth.models import User
from datetime import datetime
from LearnDriving.settings import TIME_ZONE

from rnoc.models import BCNOSS, SiteType, Tram



if __name__ == '__main__':
    #t = Tram.objects.get(Site_ID_3G__icontains = '3G_STR041E_STG')[0]
    #print t.Site_Name_1
    #print t.RNC
    #bsc_instance = BSCRNC.objects.get(Name__icontains ='KGRNC14')[0]
    #print bsc_instance.Name
    gio_mat_for_filter = datetime(2016, 5, 19, 0, 0)
    #peoples = BCNOSS.objects.filter(gio_mat__gte = gio_mat_for_filter).raw("SELECT id,vnp_comment  FROM rnoc_bcnoss WHERE ")
    sql_raw = u'''SELECT COUNT(id)
  FROM rnoc_bcnoss WHERE code_loi = '1' '''
    '''
    osss = BCNOSS.objects.filter(gio_mat__gte = gio_mat_for_filter).extra(select={'day': "date( gio_mat  AT TIME ZONE '{0}')".format(TIME_ZONE)}).values('day').extra(select={'maloi1_count':sql_raw})
    print type(osss)
    print len(osss)
    for p in osss:
        print p['day'],p.maloi1_count
        
    '''
    sql_raw = u'''select * from rnoc_bcnoss where gio_mat  >= '2016-05-20 00:00:00 +7'
        '''
    
    osss = BCNOSS.objects.raw(sql_raw)
    for count,x in enumerate(osss):
        print x.object,count,x.gio_mat.strftime("%H:%M:%S %d:%m:%Y")
    '''
    site_type = SiteType.objects.first()
    ist = Tram(Site_Name_1 = 'abc',nguoi_tao = User.objects.first(),ngay_gio_tao = datetime(2016, 5, 19, 0, 0),Site_type=site_type)
    ist.save()
    print ist.ngay_gio_tao
    '''