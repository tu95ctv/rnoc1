# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rnoc', '0002_auto_20160531_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='tinh',
            name='so_luong_tram_2G',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tinh',
            name='so_luong_tram_3G',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='doitac',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 588345), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='duan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 589613), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='faultlibrary',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 597946), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='lenh',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 599058), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='mll',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 610198), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='nguyennhan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 4, 27, 7, 593435, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='suco',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 4, 27, 7, 592354, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thaotaclienquan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 596878), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thietbi',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 587114), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='tram',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 4, 27, 7, 605863, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='trangthai',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 31, 23, 27, 7, 595447), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
    ]
