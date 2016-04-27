# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalUserDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('is_teacher', models.BooleanField(help_text='Učitelia vedia hromadne prihlasovať školy na akcie.', verbose_name='som učiteľ')),
                ('graduation', models.IntegerField(help_text='Povinné pre žiakov.', null=True, blank=True, verbose_name='rok maturity')),
                ('want_news', models.BooleanField(help_text='Mám záujem dostávať e-mailom pozvánky na ďalšie akcie.', verbose_name='pozvánky e-mailom')),
            ],
            options={
                'verbose_name_plural': 'dodatočné údaje o užívateľoch',
                'verbose_name': 'dodatočné údaje o užívateľoch',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(help_text='Názov akcie, napr. Klub Trojstenu po Náboji FKS', max_length=100)),
                ('date', models.DateField(unique=True)),
                ('deadline', models.DateTimeField(help_text='Deadline na prihlasovanie')),
                ('invitation', models.FileField(help_text='PDF s pozvánkou, keď bude hotová.', upload_to=events.models.choose_invitation_filename, blank=True)),
                ('poll_begin', models.DateTimeField(help_text='Spustenie ankety', null=True, blank=True)),
                ('poll_end', models.DateTimeField(help_text='Ukončenie ankety', null=True, blank=True)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name_plural': 'akcie',
                'verbose_name': 'akcia',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndividualSignup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('lunch', models.BooleanField(help_text='Mám záujem o obed po akcii', verbose_name='obed')),
            ],
            options={
                'verbose_name_plural': 'prihlášky jednotlivcov',
                'verbose_name': 'prihláška jednotlivca',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndividualOvernightSignup',
            fields=[
                ('individualsignup_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='events.IndividualSignup')),
                ('sleepover', models.BooleanField(help_text='Prespávanie bude v lodenici alebo v telocvični za poplatok, ktorý určí na mieste doc. Potočný. Viac v <a href="/instructions/">organizačných pokynoch</a>.', verbose_name='chcem prespať')),
                ('sleeping_bag', models.BooleanField(help_text='Mám záujem požičať si spacák. Spacákov je obmedzené množstvo, takže pokiaľ môžete, radšej si doneste vlastné.', verbose_name='spacák')),
                ('sleeping_pad', models.BooleanField(help_text='Mám záujem požičať si karimatku. Karimatiek je obmedzené množstvo, takže pokiaľ môžete, radšej si doneste vlastné.', verbose_name='karimatka')),
                ('game_participation', models.BooleanField(help_text='Pre viac detailov o\xa0tom, kedy sa bude konať hra, sledujte novinky.', verbose_name='zúčastním sa hry')),
            ],
            options={
                'verbose_name_plural': 'prihlášky jednotlivcov s\xa0možnosťou prespať',
                'verbose_name': 'prihláška jednotlivca s\xa0možnosťou prespať',
            },
            bases=('events.individualsignup',),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('lecturer', models.CharField(max_length=100, blank=True, verbose_name='prednášajúci')),
                ('title', models.CharField(max_length=147, verbose_name='názov prednášky')),
                ('abstract', models.TextField(blank=True, verbose_name='abstrakt')),
                ('room', models.CharField(max_length=20, verbose_name='miestnosť')),
                ('time', models.TimeField(verbose_name='čas')),
                ('field', models.CharField(max_length=47, blank=True, verbose_name='odbor')),
                ('video_url', models.URLField(blank=True, verbose_name='URL videa')),
                ('materials', models.FileField(help_text='Materiály od prednášajúceho, napr. slidy v PDF alebo ZIP obsahujúci všetky obrázky a videá.', upload_to=events.models.choose_lecture_materials_filename, blank=True, verbose_name='materiály')),
                ('event', models.ForeignKey(related_name='lectures', to='events.Event', verbose_name='akcia')),
            ],
            options={
                'ordering': ('event', 'time'),
                'verbose_name_plural': 'body programu (napr. prednášky)',
                'verbose_name': 'bod programu (napr. prednáška)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('abbreviation', models.CharField(help_text='Sktatka názvu školy.', max_length=100, blank=True, verbose_name='skratka')),
                ('verbose_name', models.CharField(max_length=100, verbose_name='celý názov')),
                ('addr_name', models.CharField(max_length=100, blank=True)),
                ('street', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=100, blank=True)),
                ('zip_code', models.CharField(max_length=10, blank=True)),
            ],
            options={
                'ordering': ('city', 'street', 'verbose_name'),
                'verbose_name_plural': 'školy',
                'verbose_name': 'škola',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SchoolSignup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('students1', models.PositiveSmallIntegerField(default=0, verbose_name='počet prvákov')),
                ('students2', models.PositiveSmallIntegerField(default=0, verbose_name='počet druhákov')),
                ('students3', models.PositiveSmallIntegerField(default=0, verbose_name='počet tretiakov')),
                ('students4', models.PositiveSmallIntegerField(default=0, verbose_name='počet štvrtákov')),
                ('lunches', models.PositiveSmallIntegerField(default=0, verbose_name='počet obedov')),
                ('event', models.ForeignKey(related_name='school_signups', to='events.Event', verbose_name='akcia')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'hromadné prihlášky',
                'verbose_name': 'hromadná prihláška',
            },
            bases=(models.Model,),
        ),
    ]
