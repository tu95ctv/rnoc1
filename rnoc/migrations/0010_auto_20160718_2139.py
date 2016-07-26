# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rnoc', '0009_auto_20160625_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doitac',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 70000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='duan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 71000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='faultlibrary',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 78000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='lenh',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 79000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='mll',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 89000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='nguyennhan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 14, 39, 43, 74000, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='suco',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 14, 39, 43, 73000, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thaotaclienquan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 77000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thietbi',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 69000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='tinh',
            name='so_luong_tram_2G',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tram',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 14, 39, 43, 85000, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='trangthai',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 18, 21, 39, 43, 76000), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
    ]
