from django.contrib import admin

from drivingtest.models import Table3g,Doitac, Mll, TrangThaiCuaTram, Duan,\
    UserProfile
from django.contrib.auth.models import Permission

class Tadmin(admin.ModelAdmin):
    search_fields = ['site_name_1','site_id_3g']
    
class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    #fields = ['name','codename']

admin.site.register(Permission, PermissionAdmin)
admin.site.register(Table3g,Tadmin)
admin.site.register(Doitac)
admin.site.register(Mll)
admin.site.register(TrangThaiCuaTram)
admin.site.register(Duan)
admin.site.register(UserProfile)
