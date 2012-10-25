# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Event.name'
        db.alter_column('events_event', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Lecture.lecturer'
        db.alter_column('events_lecture', 'lecturer', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'School.city'
        db.alter_column('events_school', 'city', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'School.addr_name'
        db.alter_column('events_school', 'addr_name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'School.abbreviation'
        db.alter_column('events_school', 'abbreviation', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'School.street'
        db.alter_column('events_school', 'street', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'School.verbose_name'
        db.alter_column('events_school', 'verbose_name', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Event.name'
        db.alter_column('events_event', 'name', self.gf('django.db.models.fields.CharField')(max_length=u'47'))

        # Changing field 'Lecture.lecturer'
        db.alter_column('events_lecture', 'lecturer', self.gf('django.db.models.fields.CharField')(max_length=47))

        # Changing field 'School.city'
        db.alter_column('events_school', 'city', self.gf('django.db.models.fields.CharField')(max_length=47))

        # Changing field 'School.addr_name'
        db.alter_column('events_school', 'addr_name', self.gf('django.db.models.fields.CharField')(max_length=47))

        # Changing field 'School.abbreviation'
        db.alter_column('events_school', 'abbreviation', self.gf('django.db.models.fields.CharField')(max_length=23))

        # Changing field 'School.street'
        db.alter_column('events_school', 'street', self.gf('django.db.models.fields.CharField')(max_length=47))

        # Changing field 'School.verbose_name'
        db.alter_column('events_school', 'verbose_name', self.gf('django.db.models.fields.CharField')(max_length=47))

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        },
        'events.lecture': {
            'Meta': {'ordering': "(u'event', u'time')", 'object_name': 'Lecture'},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'lectures'", 'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecturer': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '147'}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'events.school': {
            'Meta': {'ordering': "(u'verbose_name',)", 'object_name': 'School'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'addr_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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