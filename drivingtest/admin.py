from django.contrib import admin

from drivingtest.models import Table3g,Doitac, Mll
class Tadmin(admin.ModelAdmin):
    search_fields = ['site_name_1','site_id_3g']
admin.site.register(Table3g,Tadmin)
admin.site.register(Doitac)
admin.site.register(Mll)