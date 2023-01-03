# Generated by Django 4.0.8 on 2022-12-27 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Album name', max_length=50, unique=True, verbose_name='name')),
                ('description', models.CharField(help_text='Album description', max_length=200, verbose_name='description')),
                ('owner', models.ForeignKey(help_text='Album owner', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'album',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Banknote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(help_text='Banknote country (e.g. Venezuela)', max_length=100, verbose_name='country')),
                ('denomination', models.CharField(help_text='Banknote denomination (e.g. 100)', max_length=30, verbose_name='denomination')),
                ('currency', models.CharField(help_text='Banknote currency (e.g. Bolívares)', max_length=25, verbose_name='currency')),
                ('pick_number', models.CharField(blank=True, help_text='Pick number code (e.g. 59a)', max_length=7, verbose_name='pick number')),
                ('issued_date', models.CharField(blank=True, help_text='Issued date of the banknote, ND stands for No Date in the banknote (e.g. ND(1980))', max_length=30, verbose_name='issued date')),
                ('year', models.IntegerField(help_text='Enter 4 digits year (e.g. 1980)', verbose_name='year')),
                ('description_front', models.CharField(blank=True, help_text='Banknote front description (e.g. Mausoleo de Bolívar. Simón Bolívar.)', max_length=200, verbose_name='front description')),
                ('description_back', models.CharField(blank=True, help_text='Banknote back description (e.g. Expedición de Los Cayos.)', max_length=200, verbose_name='back description')),
                ('serial_number', models.CharField(blank=True, help_text='Banknote serial (e.g. A09084450)', max_length=20, verbose_name='serial number')),
                ('size', models.CharField(blank=True, help_text='Banknote dimensions (e.g. 157x69mm)', max_length=10, verbose_name='size')),
                ('observations', models.TextField(blank=True, help_text='Enter your observations about the banknote (e.g. two pinholes)', verbose_name='observations')),
                ('image_front', models.ImageField(blank=True, help_text='Select an image for the banknote front', upload_to='banknotes', verbose_name='front image')),
                ('image_back', models.ImageField(blank=True, help_text='Select an image for the banknote back', upload_to='banknotes', verbose_name='back image')),
                ('commemorative', models.BooleanField(blank=True, verbose_name='commemorative')),
                ('polymer', models.BooleanField(blank=True, verbose_name='polymer')),
                ('overprint', models.BooleanField(blank=True, verbose_name='overprint')),
                ('specimen', models.BooleanField(blank=True, verbose_name='specimen')),
                ('notgeld', models.BooleanField(blank=True)),
                ('grading', models.CharField(blank=True, choices=[('UNC', 'Uncirculated'), ('AU', 'About Uncirculated'), ('XF', 'Extremely Fine'), ('VF', 'Very Fine'), ('F', 'Fine'), ('VG', 'Very Good'), ('G', 'Good'), ('PR', 'Poor')], help_text='Grading based on the IBNS Grading Standards', max_length=3, verbose_name='grading')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('album', models.ManyToManyField(blank=True, help_text='Select the album(s) to add the banknote to', related_name='my_album', to='collector.album', verbose_name='album')),
                ('owner', models.ForeignKey(help_text='Banknote owner', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'banknote',
                'ordering': ('country', 'pick_number', 'serial_number'),
            },
        ),
    ]