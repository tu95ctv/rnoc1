from django.contrib import admin

from models import Tram,DoiTac, Mll, TrangThai, DuAn,\
    UserProfile
from django.contrib.auth.models import Permission
from django.db.models.fields import CharField

class Tadmin(admin.ModelAdmin):
    search_fields = ['site_name_1','site_id_3g']
    
class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    #fields = ['name','codename']
class TramAdmin(admin.ModelAdmin):
    list_display=('site_name_1','site_id_3g','Ngay_Phat_Song_3G')
    search_fields = ('site_name_1','site_id_3g')
    list_filter = ('Cabinet','RNC')
    date_hierarchy = 'Ngay_Phat_Song_3G'
    ordering = ('Ngay_Phat_Song_3G','-site_name_1')
    filter_horizontal = ('du_an',)
    raw_id_fields = ('Cabinet',)
class UserProfileAdmin(admin.ModelAdmin):
    fields = [f.name for f in UserProfile._meta.fields]
    list_display = fields
    search_fields = fields
class MllAdmin(admin.ModelAdmin):
    fields = [f.name for f in Mll._meta.fields ]
    char_fields = [f.name for f in Mll._meta.fields if isinstance(f, CharField)]
    list_display = fields
    search_fields = char_fields

admin.site.register(Permission, PermissionAdmin)
admin.site.register(Tram,TramAdmin)
admin.site.register(DoiTac)
admin.site.register(Mll,MllAdmin)
admin.site.register(TrangThai)
admin.site.register(DuAn)
admin.site.register(UserProfile,UserProfileAdmin)
