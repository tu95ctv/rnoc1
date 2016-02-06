from django.contrib import admin

from drivingtest.models import Table3g,Doitac, Mll, TrangThaiCuaTram, Duan,\
    UserProfile
from django.contrib.auth.models import Permission

class Tadmin(admin.ModelAdmin):
    search_fields = ['site_name_1','site_id_3g']
    
class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    #fields = ['name','codename']
class Table3gAdmin(admin.ModelAdmin):
    list_display=('site_name_1','site_id_3g','Ngay_Phat_Song_3G')
    search_fields = ('site_name_1','site_id_3g')
    list_filter = ('Cabinet','RNC')
    date_hierarchy = 'Ngay_Phat_Song_3G'
    ordering = ('Ngay_Phat_Song_3G','-site_name_1')
    filter_horizontal = ('du_an',)
    raw_id_fields = ('Cabinet',)
    #dfields =('site_name_1','site_id_3g','Ngay_Phat_Song_3G')
    #fields = ['name','codename']
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Table3g,Table3gAdmin)
admin.site.register(Doitac)
admin.site.register(Mll)
admin.site.register(TrangThaiCuaTram)
admin.site.register(Duan)
admin.site.register(UserProfile)
