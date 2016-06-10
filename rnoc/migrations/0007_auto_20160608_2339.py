# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rnoc', '0006_auto_20160602_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='bscrnc',
            name='so_luong_tram',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doitac',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 521330), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='duan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 522658), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='faultlibrary',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 531806), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='lenh',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 532925), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='mll',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 544259), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='nguyennhan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 16, 39, 28, 526562, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='suco',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 16, 39, 28, 525396, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thaotaclienquan',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 530434), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='thietbi',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 520083), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='tram',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 16, 39, 28, 539834, tzinfo=utc), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
        migrations.AlterField(
            model_name='tram',
            name='tinh',
            field=models.ForeignKey(related_name='tinh_dot_tram_set', verbose_name='T\u1ec9nh', blank=True, to='rnoc.Tinh', null=True),
        ),
        migrations.AlterField(
            model_name='trangthai',
            name='ngay_gio_tao',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 8, 23, 39, 28, 528635), verbose_name='Ng\xe0y gi\u1edd t\u1ea1o', blank=True),
        ),
    ]
