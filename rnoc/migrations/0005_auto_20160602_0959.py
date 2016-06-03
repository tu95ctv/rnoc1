# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rnoc', '0004_auto_20160601_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doitac',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 561403), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='duan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 562614), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='faultlibrary',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 570790), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='lenh',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 571865), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='mll',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 582778), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='nguyennhan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 14, 58, 55, 566396, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='suco',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 14, 58, 55, 565278, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thaotaclienquan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 569713), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thietbi',
            name='Name',
            field=models.CharField(unique=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='thietbi',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 560227), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='tram',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 14, 58, 55, 578469, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='trangthai',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 9, 58, 55, 568574), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
    ]
