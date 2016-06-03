# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rnoc', '0003_auto_20160531_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='tinh',
            name='tong_so_tram',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='doitac',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 232315), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='duan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 233689), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='faultlibrary',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 243046), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='lenh',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 244157), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='mll',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 255571), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='nguyennhan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 3, 10, 3, 237840, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='suco',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 3, 10, 3, 236739, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thaotaclienquan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 241940), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thietbi',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 230749), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='tram',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 2, 3, 10, 3, 250990, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='trangthai',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 22, 10, 3, 240386), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
    ]
