# coding: utf-8
from __future__ import unicode_literals
import datetime
import os.path

from django.db import models
from django.contrib.sites.models import Site, get_current_site
from django.utils.datastructures import SortedDict
from django.utils.timezone import now

from events.utils import slugify


# In which grade does a high school student graduate?
GRADUATION_GRADE = 4


class School(models.Model):
    abbreviation = models.CharField(max_length=100,
                                    blank=True,
                                    verbose_name="skratka",
                                    help_text="Sktatka názvu školy.")
    verbose_name = models.CharField(max_length=100,
                                    verbose_name="celý názov")
    addr_name = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "škola"
        verbose_name_plural = "školy"
        ordering = ("city", "street", "verbose_name")

    def __unicode__(self):
        result = ""
        if self.abbreviation:
            result += self.abbreviation + ", "
        result += self.verbose_name
        if self.street:
            result += ", " + self.street
        if self.city or self.zip_code:
            result += ", "
        if self.zip_code:
            result += self.zip_code
        if self.city:
            result += " " + self.city
        return result


class AdditionalUserDetails(models.Model):
    user = models.OneToOneField('auth.User',
                                related_name='additional_events_details')
    school = models.ForeignKey(School, default=1, verbose_name="škola",
                               help_text='Do políčka napíšte skratku, '
                               'časť názvu alebo adresy školy a následne '
                               'vyberte správnu možnosť zo zoznamu. '
                               'Pokiaľ vaša škola nie je '
                               'v&nbsp;zozname, vyberte "Gymnázium iné" '
                               'a&nbsp;pošlite nám e-mail.')
    is_teacher = models.BooleanField(verbose_name="som učiteľ",
                                     help_text='Učitelia vedia hromadne '
                                     'prihlasovať školy na akcie.')
    graduation = models.IntegerField(blank=True, null=True,
                                     verbose_name="rok maturity",
                                     help_text="Povinné pre žiakov.")
    want_news = models.BooleanField(verbose_name="pozvánky e-mailom",
                                    help_text="Mám záujem dostávať "
                                    "e-mailom pozvánky na ďalšie akcie.")

    class Meta:
        verbose_name = "dodatočné údaje o užívateľoch"
        verbose_name_plural = "dodatočné údaje o užívateľoch"

    def __unicode__(self):
        return "%s" % (self.user,)

    def get_grade(self, date=None):
        """
        Returns the school grade based on graduation_year and the provided
        date. If no date is provided, today is used.
        """
        if self.graduation is None:
            return None
        if date is None:
            date = datetime.date.today()
        # Normalize the given date's year to the one in which the closest
        # following graduation happens.
        # For simplicity, we assume graduation happens every year on the
        # first day of July.
        if date.month >= 7:
            date = date.replace(year=date.year + 1)
        years_to_graduation = self.graduation - date.year
        return GRADUATION_GRADE - years_to_graduation


def choose_invitation_filename(instance, original):
    return "%s/invitation-%s.pdf" % (instance.date.isoformat(),
                                     slugify(unicode(instance))[:74])


class Event(models.Model):
    name = models.CharField(max_length=100,
                            help_text="Názov akcie, napr. Klub Trojstenu "
                            "po Náboji FKS")
    date = models.DateField(unique=True)
    deadline = models.DateTimeField(help_text="Deadline na prihlasovanie")
    invitation = models.FileField(upload_to=choose_invitation_filename,
                                  blank=True,
                                  help_text="PDF s pozvánkou, keď bude "
                                  "hotová.")
    sites = models.ManyToManyField(Site)
    poll_begin = models.DateTimeField(blank=True, null=True,
                                      help_text="Spustenie ankety")
    poll_end = models.DateTimeField(blank=True, null=True,
                                    help_text="Ukončenie ankety")
    poll = models.ForeignKey('polls.Poll', blank=True, null=True,
                             related_name="events",
                             help_text="Anketa")

    class Meta:
        verbose_name = "akcia"
        verbose_name_plural = "akcie"
        ordering = ("-date",)

    def __unicode__(self):
        return "%s %s" % (self.name, self.date.year)

    @models.permalink
    def get_absolute_url(self):
        # We need to check if the event is the latest for this page and we
        # don't have access to the request to just call get_latest_event.
        if Event.objects.filter(sites__id__in=self.sites.all(),
                               date__gt=self.date).count() > 0:
            # There are newer relevant events, generate a general URL.
            return ("event_detail", (), {
                        'year': self.date.strftime('%Y'),
                        'month': self.date.strftime('%m'),
                        'day': self.date.strftime('%d'),
                    })
        # Else just return the link to the latest event.
        return ("event_latest",)

    @models.permalink
    def get_attendance_url(self):
        return ("event_attendance", (), {
                    'year': self.date.strftime('%Y'),
                    'month': self.date.strftime('%m'),
                    'day': self.date.strftime('%d'),
                })

    def get_grouped_lectures(self):
        """
        Returns the lectures for this event in a SortedDict mapping times
        to lists of lectures sorted by their rooms.
        """
        try:
            return self._grouped_lectures_cache
        except AttributeError:
            result = SortedDict()
            for lecture in self.lectures.order_by("time", "room"):
                result.setdefault(lecture.time, []).append(lecture)
            self._grouped_lectures_cache = result
            return result

    def is_in_future(self):
        return now().date() <= self.date

    def signup_period_open(self):
        return now() < self.deadline

    def poll_is_active(self):
        now_ = now()
        return (self.poll and self.poll_begin and
                self.poll_begin <= now_ and
                (not self.poll_end or self.poll_end >= now_))


def choose_lecture_materials_filename(instance, original):
    extension = os.path.splitext(original)[1]
    lecture_slug = slugify(unicode(instance))[:74]
    return "%s/%s%s" % (instance.event.date.isoformat(),
                        lecture_slug, extension)


class Lecture(models.Model):
    event = models.ForeignKey(Event, verbose_name="akcia",
                              related_name="lectures")
    lecturer = models.CharField(max_length=100, blank=True,
                                verbose_name="prednášajúci")
    title = models.CharField(max_length=147, verbose_name="názov prednášky")
    abstract = models.TextField(blank=True, verbose_name="abstrakt")
    room = models.CharField(max_length=20, verbose_name="miestnosť")
    time = models.TimeField(verbose_name="čas")
    field = models.CharField(max_length=47, blank=True,
                             verbose_name="odbor")
    video_url = models.URLField(blank=True, verbose_name="URL videa")
    materials = models.FileField(upload_to=choose_lecture_materials_filename,
                                 blank=True,
                                 verbose_name="materiály",
                                 help_text="Materiály od prednášajúceho, "
                                 "napr. slidy v PDF alebo ZIP obsahujúci "
                                 "všetky obrázky a videá.")
    poll = models.ForeignKey('polls.Poll', blank=True, null=True,
                             related_name="lectures",
                             help_text="Anketa")

    class Meta:
        verbose_name = "bod programu"
        verbose_name_plural = "body programu"
        ordering = ("event", "time")

    def __unicode__(self):
        return "%s: %s" % (self.lecturer, self.title)


def get_latest_event(request):
    """
    Returns the latest event relevant for the current site.
    """
    site = get_current_site(request)
    return Event.objects.filter(sites__id__exact=site.pk).order_by('-date')[0]


class IndividualSignup(models.Model):
    event = models.ForeignKey(Event, verbose_name="akcia",
                              related_name="individual_signups")
    user = models.ForeignKey('auth.User')
    lunch = models.BooleanField(verbose_name="obed",
                                help_text="Mám záujem o obed po akcii")

    class Meta:
        verbose_name = "prihláška jednotlivca"
        verbose_name_plural = "prihlášky jednotlivcov"

    def __unicode__(self):
        return "%s, %s" % (self.user, self.event)


class IndividualOvernightSignup(IndividualSignup):
    sleepover = models.BooleanField(verbose_name="chcem prespať",
                                    help_text="Prespávanie bude v lodenici "
                                    "alebo v telocvični za poplatok, ktorý "
                                    "určí na mieste doc. Potočný. Viac v "
                                    '<a href="/instructions/">organizačných'
                                    " pokynoch</a>.")
    sleeping_bag = models.BooleanField(verbose_name="spacák",
                                       help_text="Mám záujem požičať si "
                                       "spacák. Spacákov je obmedzené "
                                       "množstvo, takže pokiaľ môžete, "
                                       "radšej si doneste vlastné.")
    sleeping_pad = models.BooleanField(verbose_name="karimatka",
                                       help_text="Mám záujem požičať si "
                                       "karimatku. Karimatiek je obmedzené "
                                       "množstvo, takže pokiaľ môžete, "
                                       "radšej si doneste vlastné.")
    game_participation = models.BooleanField(verbose_name="zúčastním sa hry")


class SchoolSignup(models.Model):
    event = models.ForeignKey(Event, verbose_name="akcia",
                              related_name="school_signups")
    user = models.ForeignKey('auth.User')
    students1 = models.PositiveSmallIntegerField(default=0,
                                                 verbose_name="počet prvákov")
    students2 = models.PositiveSmallIntegerField(default=0,
                                                 verbose_name="počet druhákov")
    students3 = models.PositiveSmallIntegerField(default=0,
                                                 verbose_name="počet tretiakov")
    students4 = models.PositiveSmallIntegerField(default=0,
                                                 verbose_name="počet štvrtákov")
    lunches = models.PositiveSmallIntegerField(default=0,
                                               verbose_name="počet obedov")

    def get_total_students(self):
        return self.students1 + self.students2 + self.students3 + self.students4


def get_signup_model(request):
    """
    Returns the signup model relevant to current site and the logged in
    user's settings.
    """
    try:
        return request._akademia_events_signup_model
    except AttributeError:
        if get_current_site(request).domain == 'akademia.trojsten.sk':
            if request.user.additional_events_details.is_teacher:
                model = SchoolSignup
            else:
                model = IndividualSignup
        else:
            model = IndividualOvernightSignup
        request._akademia_events_signup_model = model
        return model
