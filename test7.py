models.py:

     class WMS(models.Model):
         alias = models.SlugField(max_length=50)
         date_created = models.DateTimeField(auto_now_add=True)
         date_updated = models.DateTimeField(auto_now=True)
         url = models.URLField()

forms.py:

     class WMSListTable(tables.Table):
         alias = tables.LinkColumn('editWMS', args=[A('pk')])
         name = tables.Column()
         type = tables.Column()
         version = tables.Column()
         valid = tables.BooleanColumn()

         class Meta:
             model = WMS
             fields = ('alias', 'url', 'date_created', 'date_updated')

views.py:

     from owslib.wms import WebMapService

     def listWMS(request):
         wms_list = WMS.objects.all()
         for wms in wms_list:
             try:
                 instance = WebMapService(wms.url)
                 wms.name = instance.identification.title
                 wms.type = instance.identification.type
                 wms.version = instance.identification.version
                 wms.valid = True
             except:
                 wms.valid = False

         wms_table = WMSListTable(wms_list)
         RequestConfig(request).configure(wms_table)
         return render(request,"basqui/manage_layer_wms_list.html",
{'wms_list':wms_table},context_instance=RequestContext(request))
