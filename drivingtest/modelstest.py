from django.db import models
from drivingtest.models import TrangThaiCuaTram
class CommentForMLLt(models.Model):
    comment= models.CharField(max_length=128,null=True,blank=True,)# if bo blank=False mac dinh se la true chelp_text="add comment here",
    #su_kien = models.ForeignKey(TrangThaiCuaTram,null=True,blank=True)

    def __unicode__(self):
        return self.comment