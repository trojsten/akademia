# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'School'
        db.create_table('events_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=23, blank=True)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=47)),
            ('addr_name', self.gf('django.db.models.fields.CharField')(max_length=47, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=47, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=47, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
        ))
        db.send_create_signal('events', ['School'])

        # Adding model 'AdditionalUserDetails'
        db.create_table('events_additionaluserdetails', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['events.School'])),
            ('is_teacher', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('events', ['AdditionalUserDetails'])

        # Adding model 'Event'
        db.create_table('events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=u'47')),
            ('date', self.gf('django.db.models.fields.DateField')(unique=True)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')()),
            ('invitation', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('events', ['Event'])

        # Adding M2M table for field sites on 'Event'
        db.create_table('events_event_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['events.event'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('events_event_sites', ['event_id', 'site_id'])

        # Adding model 'Lecture'
        db.create_table('events_lecture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'lectures', to=orm['events.Event'])),
            ('lecturer', self.gf('django.db.models.fields.CharField')(max_length=47)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=147)),
            ('abstract', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('video_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('events', ['Lecture'])


    def backwards(self, orm):
        # Deleting model 'School'
        db.delete_table('events_school')

        # Deleting model 'AdditionalUserDetails'
        db.delete_table('events_additionaluserdetails')

        # Deleting model 'Event'
        db.delete_table('events_event')

        # Removing M2M table for field sites on 'Event'
        db.delete_table('events_event_sites')

        # Deleting model 'Lecture'
        db.delete_table('events_lecture')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.additionaluserdetails': {
            'Meta': {'object_name': 'AdditionalUserDetails'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_teacher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['events.School']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'events.event': {
            'Meta': {'ordering': "(u'-date',)", 'object_name': 'Event'},
            'date': ('django.db.models.fields.DateField', [], {'unique': 'True'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "u'47'"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        },
        'events.lecture': {
            'Meta': {'ordering': "(u'event', u'time')", 'object_name': 'Lecture'},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'lectures'", 'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecturer': ('django.db.models.fields.CharField', [], {'max_length': '47'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '147'}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'events.school': {
            'Meta': {'ordering': "(u'verbose_name',)", 'object_name': 'School'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '23', 'blank': 'True'}),
            'addr_name': ('django.db.models.fields.CharField', [], {'max_length': '47', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '47', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '47', 'blank': 'True'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '47'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['events']