# -*- coding: utf-8 -*- 
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LearnDriving.settings')
from django.contrib.auth.models import User
from datetime import datetime
from LearnDriving.settings import TIME_ZONE

from rnoc.models import BCNOSS, SiteType, Tram,Mll



if __name__ == '__main__':
    #print datetime(2016,1,1,1,0,0)
    #print datetime.now()
    d2 =  datetime(2016,5,31,1,0,0)
    ist = Mll(object='abc',gio_mat = d2,ngay_gio_tao = datetime.now(),nguoi_tao = User.objects.get(username = 'ductu'))
    ist.save()
    print ist.gio_mat
    '''
    ist = Mll.objects.filter(object='abc').last()
    print ist.gio_mat
    '''
    ist = Mll.objects.filter(object='abc')[0]
    print ist.gio_mat