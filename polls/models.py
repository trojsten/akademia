# coding: utf-8
from __future__ import unicode_literals
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.safestring import mark_safe


class Poll(models.Model):
    name = models.CharField(max_length=147)

    def __unicode__(self):
        return self.name


class Question(models.Model):
    TEXT = 0
    STARS = 1
    TYPE_CHOICES = (
        (TEXT, "Text"),
        (STARS, "Hviezdičky"),
    )
    poll = models.ForeignKey(Poll, related_name="questions")
    question = models.CharField(max_length=247)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    STARS_CHOICES = tuple((i, "%d z 5 hviezdičiek" % (i,))
                          for i in range(1, 6))
    user = models.ForeignKey('auth.user')
    question = models.ForeignKey(Question, related_name="answers")
    object_id = models.IntegerField()
    content_type = models.ForeignKey('contenttypes.ContentType')
    target = generic.GenericForeignKey('content_type', 'object_id')
    value = models.TextField(blank=True)

    class Meta:
        unique_together = (('user', 'question', 'object_id', 'content_type'),)

    def __unicode__(self):
        return "%s -- %s -- %s: %s" % (self.user, self.target,
                                       self.question, self.value)

    def render_text(self):
        return mark_safe("<p>%s</p>" % (
            self.value.strip()
            .replace('\r\n', '\n').replace('\n\r', '\n')
            .replace('\r', '\n')
            .replace('\n\n', '</p><p>').replace('\n', '<br />'),
        ))
