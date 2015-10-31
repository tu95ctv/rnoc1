from django.db import models
#from drivingtest.models import TrangThaiCuaTram
class TrangThaiCuaTram(models.Model):
    Name=models.CharField(max_length=30)
    Mota = models.CharField(max_length=1330)
    def __unicode__(self):
        return self.Name
class CommentForMLLt(models.Model):
    comment= models.CharField(max_length=128,null=True,blank=True,)# if bo blank=False mac dinh se la true chelp_text="add comment here",
    su_kien = models.ForeignKey(TrangThaiCuaTram,null=True,blank=True)

    def __unicode__(self):
        return self.comment