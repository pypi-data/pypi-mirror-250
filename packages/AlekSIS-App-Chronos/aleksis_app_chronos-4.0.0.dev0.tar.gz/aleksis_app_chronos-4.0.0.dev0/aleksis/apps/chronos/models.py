# flake8: noqa: DJ01

from __future__ import annotations

from collections.abc import Iterable, Iterator
from datetime import date, datetime, time, timedelta
from itertools import chain
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Max, Min, Q
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.forms import Media
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.functional import classproperty
from django.utils.translation import gettext_lazy as _

from cache_memoize import cache_memoize
from calendarweek.django import CalendarWeek, i18n_day_abbr_choices_lazy, i18n_day_name_choices_lazy
from colorfield.fields import ColorField
from model_utils import FieldTracker
from reversion.models import Revision, Version

from aleksis.apps.chronos.managers import (
    AbsenceQuerySet,
    BreakManager,
    EventManager,
    EventQuerySet,
    ExtraLessonManager,
    ExtraLessonQuerySet,
    GroupPropertiesMixin,
    HolidayQuerySet,
    LessonPeriodManager,
    LessonPeriodQuerySet,
    LessonSubstitutionManager,
    LessonSubstitutionQuerySet,
    SupervisionManager,
    SupervisionQuerySet,
    SupervisionSubstitutionManager,
    TeacherPropertiesMixin,
    ValidityRangeQuerySet,
)
from aleksis.apps.chronos.mixins import (
    ValidityRangeRelatedExtensibleModel,
    WeekAnnotationMixin,
    WeekRelatedMixin,
)
from aleksis.apps.chronos.util.change_tracker import _get_substitution_models, substitutions_changed
from aleksis.apps.chronos.util.date import get_current_year
from aleksis.apps.chronos.util.format import format_m2m
from aleksis.apps.resint.models import LiveDocument
from aleksis.core.managers import AlekSISBaseManagerWithoutMigrations
from aleksis.core.mixins import (
    ExtensibleModel,
    GlobalPermissionModel,
    SchoolTermRelatedExtensibleModel,
)
from aleksis.core.models import DashboardWidget, Group, Room, SchoolTerm
from aleksis.core.util.core_helpers import has_person


class ValidityRange(ExtensibleModel):
    """Validity range model.

    This is used to link data to a validity range.
    """

    objects = AlekSISBaseManagerWithoutMigrations.from_queryset(ValidityRangeQuerySet)()

    school_term = models.ForeignKey(
        SchoolTerm,
        on_delete=models.CASCADE,
        verbose_name=_("School term"),
        related_name="validity_ranges",
    )
    name = models.CharField(verbose_name=_("Name"), max_length=255, blank=True)

    date_start = models.DateField(verbose_name=_("Start date"))
    date_end = models.DateField(verbose_name=_("End date"))

    @classmethod
    @cache_memoize(3600)
    def get_current(cls, day: date | None = None):
        if not day:
            day = timezone.now().date()
        try:
            return cls.objects.on_day(day).first()
        except ValidityRange.DoesNotExist:
            return None

    @classproperty
    def current(cls):
        return cls.get_current()

    def clean(self):
        """Ensure there is only one validity range at each point of time."""
        if self.date_end < self.date_start:
            raise ValidationError(_("The start date must be earlier than the end date."))

        if self.school_term and (
            self.date_end > self.school_term.date_end
            or self.date_start < self.school_term.date_start
        ):
            raise ValidationError(_("The validity range must be within the school term."))

        qs = ValidityRange.objects.within_dates(self.date_start, self.date_end)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                _("There is already a validity range for this time or a part of this time.")
            )

    def __str__(self):
        return self.name or f"{date_format(self.date_start)}–{date_format(self.date_end)}"

    class Meta:
        verbose_name = _("Validity range")
        verbose_name_plural = _("Validity ranges")
        constraints = [
            models.UniqueConstraint(
                fields=["school_term", "date_start", "date_end"], name="unique_dates_per_term"
            ),
        ]
        indexes = [
            models.Index(fields=["date_start", "date_end"], name="validity_date_start_date_end")
        ]


class TimePeriod(ValidityRangeRelatedExtensibleModel):
    WEEKDAY_CHOICES = i18n_day_name_choices_lazy()
    WEEKDAY_CHOICES_SHORT = i18n_day_abbr_choices_lazy()

    weekday = models.PositiveSmallIntegerField(
        verbose_name=_("Week day"), choices=i18n_day_name_choices_lazy()
    )
    period = models.PositiveSmallIntegerField(verbose_name=_("Number of period"))

    time_start = models.TimeField(verbose_name=_("Start time"))
    time_end = models.TimeField(verbose_name=_("End time"))

    def __str__(self) -> str:
        return f"{self.get_weekday_display()}, {self.period}."

    @classmethod
    def get_times_dict(cls) -> dict[int, tuple[datetime, datetime]]:
        periods = {}
        for period in cls.objects.for_current_or_all().all():
            periods[period.period] = (period.time_start, period.time_end)

        return periods

    def get_date(self, week: CalendarWeek | None = None) -> date:
        if isinstance(week, CalendarWeek):
            wanted_week = week
        else:
            year = getattr(self, "_year", None) or date.today().year
            week_number = getattr(self, "_week", None) or CalendarWeek().week

            wanted_week = CalendarWeek(year=year, week=week_number)

        return wanted_week[self.weekday]

    def get_datetime_start(self, date_ref: CalendarWeek | int | date | None = None) -> datetime:
        """Get datetime of lesson start in a specific week."""
        day = date_ref if isinstance(date_ref, date) else self.get_date(date_ref)
        return datetime.combine(day, self.time_start)

    def get_datetime_end(self, date_ref: CalendarWeek | int | date | None = None) -> datetime:
        """Get datetime of lesson end in a specific week."""
        day = date_ref if isinstance(date_ref, date) else self.get_date(date_ref)
        return datetime.combine(day, self.time_end)

    @classmethod
    def get_next_relevant_day(
        cls, day: date | None = None, time: time | None = None, prev: bool = False
    ) -> date:
        """Return next (previous) day with lessons depending on date and time."""
        if day is None:
            day = timezone.now().date()

        if time is not None and cls.time_max and not prev and time > cls.time_max:
            day += timedelta(days=1)

        cw = CalendarWeek.from_date(day)

        if day.weekday() > cls.weekday_max:
            if prev:
                day = cw[cls.weekday_max]
            else:
                cw += 1
                day = cw[cls.weekday_min]
        elif day.weekday() < TimePeriod.weekday_min:
            if prev:
                cw -= 1
                day = cw[cls.weekday_max]
            else:
                day = cw[cls.weekday_min]

        return day

    @classmethod
    def get_relevant_week_from_datetime(cls, when: datetime | None = None) -> CalendarWeek:
        """Return currently relevant week depending on current date and time."""
        if not when:
            when = timezone.now()

        day = when.date()
        time = when.time()

        week = CalendarWeek.from_date(day)

        if (cls.weekday_max and day.weekday() > cls.weekday_max) or (
            cls.time_max and time > cls.time_max and day.weekday() == cls.weekday_max
        ):
            week += 1

        return week

    @classmethod
    def get_prev_next_by_day(cls, day: date, url: str) -> tuple[str, str]:
        """Build URLs for previous/next day."""
        day_prev = cls.get_next_relevant_day(day - timedelta(days=1), prev=True)
        day_next = cls.get_next_relevant_day(day + timedelta(days=1))

        url_prev = reverse(url, args=[day_prev.year, day_prev.month, day_prev.day])
        url_next = reverse(url, args=[day_next.year, day_next.month, day_next.day])

        return url_prev, url_next

    @classmethod
    def from_period(cls, period: int, day: date) -> TimePeriod:
        """Get `TimePeriod` object for a period on a specific date.

        This will respect the relation to validity ranges.
        """
        return cls.objects.on_day(day).filter(period=period, weekday=day.weekday()).first()

    @classproperty
    @cache_memoize(3600)
    def period_min(cls) -> int:
        return (
            cls.objects.for_current_or_all()
            .aggregate(period__min=Coalesce(Min("period"), 1))
            .get("period__min")
        )

    @classproperty
    @cache_memoize(3600)
    def period_max(cls) -> int:
        return (
            cls.objects.for_current_or_all()
            .aggregate(period__max=Coalesce(Max("period"), 7))
            .get("period__max")
        )

    @classproperty
    @cache_memoize(3600)
    def time_min(cls) -> time | None:
        return cls.objects.for_current_or_all().aggregate(Min("time_start")).get("time_start__min")

    @classproperty
    @cache_memoize(3600)
    def time_max(cls) -> time | None:
        return cls.objects.for_current_or_all().aggregate(Max("time_end")).get("time_end__max")

    @classproperty
    @cache_memoize(3600)
    def weekday_min(cls) -> int:
        return (
            cls.objects.for_current_or_all()
            .aggregate(weekday__min=Coalesce(Min("weekday"), 0))
            .get("weekday__min")
        )

    @classproperty
    @cache_memoize(3600)
    def weekday_max(cls) -> int:
        return (
            cls.objects.for_current_or_all()
            .aggregate(weekday__max=Coalesce(Max("weekday"), 6))
            .get("weekday__max")
        )

    @classproperty
    @cache_memoize(3600)
    def period_choices(cls) -> list[tuple[str | int, str]]:
        """Build choice list of periods for usage within Django."""
        time_periods = (
            cls.objects.filter(weekday=cls.weekday_min)
            .for_current_or_all()
            .values("period", "time_start", "time_end")
            .distinct()
        )

        period_choices = [("", "")] + [
            (period, f"{period}.") for period in time_periods.values_list("period", flat=True)
        ]

        return period_choices

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["weekday", "period", "validity"], name="unique_period_per_range"
            ),
        ]
        ordering = ["weekday", "period"]
        indexes = [models.Index(fields=["time_start", "time_end"])]
        verbose_name = _("Time period")
        verbose_name_plural = _("Time periods")


class Subject(ExtensibleModel):
    short_name = models.CharField(verbose_name=_("Short name"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Long name"), max_length=255)

    colour_fg = ColorField(verbose_name=_("Foreground colour"), blank=True)
    colour_bg = ColorField(verbose_name=_("Background colour"), blank=True)

    def __str__(self) -> str:
        return f"{self.short_name} ({self.name})"

    class Meta:
        ordering = ["name", "short_name"]
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")


class Lesson(ValidityRangeRelatedExtensibleModel, GroupPropertiesMixin, TeacherPropertiesMixin):
    subject = models.ForeignKey(
        "Subject",
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("Subject"),
    )
    teachers = models.ManyToManyField(
        "core.Person", related_name="lessons_as_teacher", verbose_name=_("Teachers")
    )
    periods = models.ManyToManyField(
        "TimePeriod",
        related_name="lessons",
        through="LessonPeriod",
        verbose_name=_("Periods"),
    )
    groups = models.ManyToManyField("core.Group", related_name="lessons", verbose_name=_("Groups"))

    def get_year(self, week: int) -> int:
        year = self.validity.date_start.year
        if week < int(self.validity.date_start.strftime("%V")):
            year += 1
        return year

    def get_calendar_week(self, week: int):
        year = self.get_year(week)

        return CalendarWeek(year=year, week=week)

    def get_teachers(self) -> models.query.QuerySet:
        """Get teachers relation."""
        return self.teachers

    @property
    def _equal_lessons(self):
        """Get all lesson periods with equal lessons in the whole school term."""

        qs = Lesson.objects.filter(
            subject=self.subject,
            validity__school_term=self.validity.school_term,
        )
        for group in self.groups.all():
            qs = qs.filter(groups=group)
        return qs

    def __str__(self):
        return f"{format_m2m(self.groups)}, {self.subject.short_name}, {format_m2m(self.teachers)}"

    class Meta:
        ordering = ["validity__date_start", "subject"]
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")


class LessonSubstitution(ExtensibleModel, TeacherPropertiesMixin, WeekRelatedMixin):
    objects = LessonSubstitutionManager.from_queryset(LessonSubstitutionQuerySet)()

    tracker = FieldTracker()

    week = models.IntegerField(verbose_name=_("Week"), default=CalendarWeek.current_week)
    year = models.IntegerField(verbose_name=_("Year"), default=get_current_year)

    lesson_period = models.ForeignKey(
        "LessonPeriod", models.CASCADE, "substitutions", verbose_name=_("Lesson period")
    )

    subject = models.ForeignKey(
        "Subject",
        on_delete=models.CASCADE,
        related_name="lesson_substitutions",
        null=True,
        blank=True,
        verbose_name=_("Subject"),
    )
    teachers = models.ManyToManyField(
        "core.Person",
        related_name="lesson_substitutions",
        blank=True,
        verbose_name=_("Teachers"),
    )
    room = models.ForeignKey(
        "core.Room", models.CASCADE, null=True, blank=True, verbose_name=_("Room")
    )

    cancelled = models.BooleanField(default=False, verbose_name=_("Cancelled?"))
    cancelled_for_teachers = models.BooleanField(
        default=False, verbose_name=_("Cancelled for teachers?")
    )

    comment = models.TextField(verbose_name=_("Comment"), blank=True)

    def clean(self) -> None:
        if self.subject and self.cancelled:
            raise ValidationError(_("Lessons can only be either substituted or cancelled."))

    @property
    def date(self):
        week = CalendarWeek(week=self.week, year=self.year)
        return week[self.lesson_period.period.weekday]

    @property
    def time_range(self) -> (timezone.datetime, timezone.datetime):
        """Get the time range of this substitution."""
        return timezone.datetime.combine(
            self.date, self.lesson_period.period.time_start
        ), timezone.datetime.combine(self.date, self.lesson_period.period.time_end)

    def get_teachers(self):
        return self.teachers

    def __str__(self):
        return f"{self.lesson_period}, {date_format(self.date)}"

    class Meta:
        ordering = [
            "year",
            "week",
            "lesson_period__period__weekday",
            "lesson_period__period__period",
        ]
        constraints = [
            models.CheckConstraint(
                check=~Q(cancelled=True, subject__isnull=False),
                name="either_substituted_or_cancelled",
            ),
            models.UniqueConstraint(
                fields=["lesson_period", "week", "year"], name="unique_period_per_week"
            ),
        ]
        indexes = [
            models.Index(fields=["week", "year"], name="substitution_week_year"),
            models.Index(fields=["lesson_period"], name="substitution_lesson_period"),
        ]
        verbose_name = _("Lesson substitution")
        verbose_name_plural = _("Lesson substitutions")


class LessonPeriod(WeekAnnotationMixin, TeacherPropertiesMixin, ExtensibleModel):
    label_ = "lesson_period"

    objects = LessonPeriodManager.from_queryset(LessonPeriodQuerySet)()

    lesson = models.ForeignKey(
        "Lesson",
        models.CASCADE,
        related_name="lesson_periods",
        verbose_name=_("Lesson"),
    )
    period = models.ForeignKey(
        "TimePeriod",
        models.CASCADE,
        related_name="lesson_periods",
        verbose_name=_("Time period"),
    )

    room = models.ForeignKey(
        "core.Room",
        models.CASCADE,
        null=True,
        related_name="lesson_periods",
        verbose_name=_("Room"),
    )

    def get_substitution(self, week: CalendarWeek | None = None) -> LessonSubstitution:
        wanted_week = week or self.week or CalendarWeek()

        # We iterate over all substitutions because this can make use of
        # prefetching when this model is loaded from outside, in contrast
        # to .filter()
        for substitution in self.substitutions.all():
            if substitution.week == wanted_week.week and substitution.year == wanted_week.year:
                return substitution
        return None

    def get_subject(self) -> Subject | None:
        sub = self.get_substitution()
        if sub and sub.subject:
            return sub.subject
        else:
            return self.lesson.subject

    def get_teachers(self) -> models.query.QuerySet:
        sub = self.get_substitution()
        if sub and sub.teachers.all():
            return sub.teachers
        else:
            return self.lesson.teachers

    def get_room(self) -> Room | None:
        if self.get_substitution() and self.get_substitution().room:
            return self.get_substitution().room
        else:
            return self.room

    def get_groups(self) -> models.query.QuerySet:
        return self.lesson.groups

    @property
    def group_names(self):
        """Get group names as joined string."""
        return self.lesson.group_names

    @property
    def group_short_names(self):
        """Get group short names as joined string."""
        return self.lesson.group_short_names

    def __str__(self) -> str:
        return f"{self.period}, {self.lesson}"

    @property
    def _equal_lesson_periods(self):
        """Get all lesson periods with equal lessons in the whole school term."""

        return LessonPeriod.objects.filter(lesson__in=self.lesson._equal_lessons)

    @property
    def next(self) -> LessonPeriod:  # noqa
        """Get next lesson period of this lesson.

        .. warning::
            To use this property,  the provided lesson period must be annotated with a week.
        """
        return self._equal_lesson_periods.next_lesson(self)

    @property
    def prev(self) -> LessonPeriod:
        """Get previous lesson period of this lesson.

        .. warning::
            To use this property,  the provided lesson period must be annotated with a week.
        """
        return self._equal_lesson_periods.next_lesson(self, -1)

    def is_replaced_by_event(
        self, events: Iterable[Event], groups: Iterable[Group] | None = None
    ) -> bool:
        """Check if this lesson period is replaced by an event."""
        groups_of_event = set(chain(*[event.groups.all() for event in events]))

        if groups:
            # If the current group is a part of the event,
            # there are no other lessons for the group.
            groups = set(groups)
            if groups.issubset(groups_of_event):
                return True
        else:
            groups_lesson_period = set(self.lesson.groups.all())

            # The lesson period isn't replacable if the lesson has no groups at all
            if not groups_lesson_period:
                return False

            # This lesson period is replaced by an event ...
            # ... if all groups of this lesson period are a part of the event ...
            if groups_lesson_period.issubset(groups_of_event):
                return True

            all_parent_groups = set(
                chain(*[group.parent_groups.all() for group in groups_lesson_period])
            )
            # ... or if all parent groups of this lesson period are a part of the event.
            if all_parent_groups.issubset(groups_of_event):
                return True

    class Meta:
        ordering = [
            "lesson__validity__date_start",
            "period__weekday",
            "period__period",
            "lesson__subject",
        ]
        indexes = [
            models.Index(fields=["lesson", "period"], name="lesson_period_lesson_period"),
            models.Index(fields=["room"], include=["lesson", "period"], name="lesson_period_room"),
        ]
        verbose_name = _("Lesson period")
        verbose_name_plural = _("Lesson periods")


class TimetableWidget(DashboardWidget):
    template = "chronos/widget.html"

    def get_context(self, request):
        from aleksis.apps.chronos.util.build import build_timetable  # noqa

        context = {"has_plan": True}
        wanted_day = TimePeriod.get_next_relevant_day(timezone.now().date(), datetime.now().time())

        if has_person(request.user):
            person = request.user.person
            type_ = person.timetable_type

            # Build timetable
            timetable = build_timetable("person", person, wanted_day)

            if type_ is None:
                # If no student or teacher, redirect to all timetables
                context["has_plan"] = False
            else:
                context["timetable"] = timetable
                context["holiday"] = Holiday.on_day(wanted_day)
                context["type"] = type_
                context["day"] = wanted_day
                context["periods"] = TimePeriod.get_times_dict()
                context["smart"] = True
        else:
            context["has_plan"] = False

        return context

    media = Media(css={"all": ("css/chronos/timetable.css",)})

    class Meta:
        proxy = True
        verbose_name = _("Timetable widget")
        verbose_name_plural = _("Timetable widgets")


class AbsenceReason(ExtensibleModel):
    short_name = models.CharField(verbose_name=_("Short name"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Name"), blank=True, max_length=255)

    def __str__(self):
        if self.name:
            return f"{self.short_name} ({self.name})"
        else:
            return self.short_name

    class Meta:
        verbose_name = _("Absence reason")
        verbose_name_plural = _("Absence reasons")


class Absence(SchoolTermRelatedExtensibleModel):
    objects = AlekSISBaseManagerWithoutMigrations.from_queryset(AbsenceQuerySet)()

    reason = models.ForeignKey(
        "AbsenceReason",
        on_delete=models.SET_NULL,
        related_name="absences",
        blank=True,
        null=True,
        verbose_name=_("Absence reason"),
    )

    teacher = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="absences",
        null=True,
        blank=True,
        verbose_name=_("Teacher"),
    )
    group = models.ForeignKey(
        "core.Group",
        on_delete=models.CASCADE,
        related_name="absences",
        null=True,
        blank=True,
        verbose_name=_("Group"),
    )
    room = models.ForeignKey(
        "core.Room",
        on_delete=models.CASCADE,
        related_name="absences",
        null=True,
        blank=True,
        verbose_name=_("Room"),
    )

    date_start = models.DateField(verbose_name=_("Start date"), null=True)
    date_end = models.DateField(verbose_name=_("End date"), null=True)
    period_from = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("Start period"),
        null=True,
        related_name="+",
    )
    period_to = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("End period"),
        null=True,
        related_name="+",
    )
    comment = models.TextField(verbose_name=_("Comment"), blank=True)

    def __str__(self):
        if self.teacher:
            return str(self.teacher)
        elif self.group:
            return str(self.group)
        elif self.room:
            return str(self.room)
        else:
            return _("Unknown absence")

    class Meta:
        ordering = ["date_start"]
        indexes = [models.Index(fields=["date_start", "date_end"])]
        verbose_name = _("Absence")
        verbose_name_plural = _("Absences")


class Exam(SchoolTermRelatedExtensibleModel):
    lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.CASCADE,
        related_name="exams",
        verbose_name=_("Lesson"),
    )

    date = models.DateField(verbose_name=_("Date of exam"))
    period_from = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("Start period"),
        related_name="+",
    )
    period_to = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("End period"),
        related_name="+",
    )

    title = models.CharField(verbose_name=_("Title"), max_length=255, blank=True)
    comment = models.TextField(verbose_name=_("Comment"), blank=True)

    class Meta:
        ordering = ["date"]
        indexes = [models.Index(fields=["date"])]
        verbose_name = _("Exam")
        verbose_name_plural = _("Exams")


class Holiday(ExtensibleModel):
    objects = AlekSISBaseManagerWithoutMigrations.from_queryset(HolidayQuerySet)()

    title = models.CharField(verbose_name=_("Title"), max_length=255)
    date_start = models.DateField(verbose_name=_("Start date"), null=True)
    date_end = models.DateField(verbose_name=_("End date"), null=True)
    comments = models.TextField(verbose_name=_("Comments"), blank=True)

    def get_days(self) -> Iterator[date]:
        delta = self.date_end - self.date_start
        for i in range(delta.days + 1):
            yield self.date_start + timedelta(days=i)

    @classmethod
    def on_day(cls, day: date) -> Holiday | None:
        holidays = cls.objects.on_day(day)
        if holidays.exists():
            return holidays[0]
        else:
            return None

    @classmethod
    def in_week(cls, week: CalendarWeek) -> dict[int, Holiday | None]:
        per_weekday = {}
        holidays = Holiday.objects.in_week(week)

        for weekday in range(TimePeriod.weekday_min, TimePeriod.weekday_max + 1):
            holiday_date = week[weekday]
            filtered_holidays = list(
                filter(
                    lambda h: holiday_date >= h.date_start and holiday_date <= h.date_end,
                    holidays,
                )
            )
            if filtered_holidays:
                per_weekday[weekday] = filtered_holidays[0]

        return per_weekday

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["date_start"]
        indexes = [models.Index(fields=["date_start", "date_end"])]
        verbose_name = _("Holiday")
        verbose_name_plural = _("Holidays")


class SupervisionArea(ExtensibleModel):
    short_name = models.CharField(verbose_name=_("Short name"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Long name"), max_length=255)
    colour_fg = ColorField(default="#000000")
    colour_bg = ColorField()

    def __str__(self):
        return f"{self.name} ({self.short_name})"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Supervision area")
        verbose_name_plural = _("Supervision areas")


class Break(ValidityRangeRelatedExtensibleModel):
    objects = BreakManager()

    short_name = models.CharField(verbose_name=_("Short name"), max_length=255)
    name = models.CharField(verbose_name=_("Long name"), max_length=255)

    after_period = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("Time period after break starts"),
        related_name="break_after",
        blank=True,
        null=True,
    )
    before_period = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("Time period before break ends"),
        related_name="break_before",
        blank=True,
        null=True,
    )

    @property
    def weekday(self):
        return self.after_period.weekday if self.after_period else self.before_period.weekday

    @property
    def after_period_number(self):
        return self.after_period.period if self.after_period else self.before_period.period - 1

    @property
    def before_period_number(self):
        return self.before_period.period if self.before_period else self.after_period.period + 1

    @property
    def time_start(self):
        return self.after_period.time_end if self.after_period else None

    @property
    def time_end(self):
        return self.before_period.time_start if self.before_period else None

    @classmethod
    def get_breaks_dict(cls) -> dict[int, tuple[datetime, datetime]]:
        breaks = {}
        for break_ in cls.objects.all():
            breaks[break_.before_period_number] = break_

        return breaks

    def __str__(self):
        return f"{self.name} ({self.short_name})"

    class Meta:
        ordering = ["after_period"]
        indexes = [models.Index(fields=["after_period", "before_period"])]
        verbose_name = _("Break")
        verbose_name_plural = _("Breaks")
        constraints = [
            models.UniqueConstraint(
                fields=["validity", "short_name"], name="unique_short_name_per_validity_break"
            ),
        ]


class Supervision(ValidityRangeRelatedExtensibleModel, WeekAnnotationMixin):
    objects = SupervisionManager.from_queryset(SupervisionQuerySet)()

    area = models.ForeignKey(
        SupervisionArea,
        models.CASCADE,
        verbose_name=_("Supervision area"),
        related_name="supervisions",
    )
    break_item = models.ForeignKey(
        Break, models.CASCADE, verbose_name=_("Break"), related_name="supervisions"
    )
    teacher = models.ForeignKey(
        "core.Person",
        models.CASCADE,
        related_name="supervisions",
        verbose_name=_("Teacher"),
    )

    def get_year(self, week: int) -> int:
        year = self.validity.date_start.year
        if week < int(self.validity.date_start.strftime("%V")):
            year += 1
        return year

    def get_calendar_week(self, week: int):
        year = self.get_year(week)

        return CalendarWeek(year=year, week=week)

    def get_substitution(self, week: CalendarWeek | None = None) -> SupervisionSubstitution | None:
        wanted_week = week or self.week or CalendarWeek()
        # We iterate over all substitutions because this can make use of
        # prefetching when this model is loaded from outside, in contrast
        # to .filter()
        for substitution in self.substitutions.all():
            for weekday in range(0, 7):
                if substitution.date == wanted_week[weekday]:
                    return substitution
        return None

    @property
    def teachers(self):
        return [self.teacher]

    def __str__(self):
        return f"{self.break_item}, {self.area}, {self.teacher}"

    class Meta:
        ordering = ["area", "break_item"]
        verbose_name = _("Supervision")
        verbose_name_plural = _("Supervisions")


class SupervisionSubstitution(ExtensibleModel):
    objects = SupervisionSubstitutionManager()

    tracker = FieldTracker()

    date = models.DateField(verbose_name=_("Date"))
    supervision = models.ForeignKey(
        Supervision,
        models.CASCADE,
        verbose_name=_("Supervision"),
        related_name="substitutions",
    )
    teacher = models.ForeignKey(
        "core.Person",
        models.CASCADE,
        related_name="substituted_supervisions",
        verbose_name=_("Teacher"),
    )

    @property
    def teachers(self):
        return [self.teacher]

    @property
    def time_range(self) -> (timezone.datetime, timezone.datetime):
        """Get the time range of this supervision substitution."""
        return timezone.datetime.combine(
            self.date,
            self.supervision.break_item.time_start or self.supervision.break_item.time_end,
        ), timezone.datetime.combine(
            self.date,
            self.supervision.break_item.time_end or self.supervision.break_item.time_start,
        )

    def __str__(self):
        return f"{self.supervision}, {date_format(self.date)}"

    class Meta:
        ordering = ["date", "supervision"]
        verbose_name = _("Supervision substitution")
        verbose_name_plural = _("Supervision substitutions")


class Event(SchoolTermRelatedExtensibleModel, GroupPropertiesMixin, TeacherPropertiesMixin):
    label_ = "event"

    tracker = FieldTracker()

    objects = EventManager.from_queryset(EventQuerySet)()

    title = models.CharField(verbose_name=_("Title"), max_length=255, blank=True)

    date_start = models.DateField(verbose_name=_("Start date"), null=True)
    date_end = models.DateField(verbose_name=_("End date"), null=True)

    period_from = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("Start time period"),
        related_name="+",
    )
    period_to = models.ForeignKey(
        "TimePeriod",
        on_delete=models.CASCADE,
        verbose_name=_("End time period"),
        related_name="+",
    )

    groups = models.ManyToManyField("core.Group", related_name="events", verbose_name=_("Groups"))
    rooms = models.ManyToManyField("core.Room", related_name="events", verbose_name=_("Rooms"))
    teachers = models.ManyToManyField(
        "core.Person", related_name="events", verbose_name=_("Teachers")
    )

    def __str__(self):
        if self.title:
            return self.title
        else:
            return _("Event {pk}").format(pk=self.pk)

    def get_period_min(self, day) -> int:
        return (
            TimePeriod.objects.on_day(day)
            .aggregate(period__min=Coalesce(Min("period"), 1))
            .get("period__min")
        )

    def get_period_max(self, day) -> int:
        return (
            TimePeriod.objects.on_day(day)
            .aggregate(period__max=Coalesce(Max("period"), 7))
            .get("period__max")
        )

    @property
    def raw_period_from_on_day(self) -> TimePeriod:
        """Get start period on the annotated day (as TimePeriod object).

        If there is no date annotated, it will use the current date.
        """
        day = getattr(self, "_date", timezone.now().date())
        if day != self.date_start:
            return TimePeriod.from_period(self.get_period_min(day), day)
        else:
            return self.period_from

    @property
    def raw_period_to_on_day(self) -> TimePeriod:
        """Get end period on the annotated day (as TimePeriod object).

        If there is no date annotated, it will use the current date.
        """
        day = getattr(self, "_date", timezone.now().date())
        if day != self.date_end:
            return TimePeriod.from_period(self.get_period_max(day), day)
        else:
            return self.period_to

    @property
    def period_from_on_day(self) -> int:
        """Get start period on the annotated day (as period number).

        If there is no date annotated, it will use the current date.
        """
        return self.raw_period_from_on_day.period

    @property
    def period_to_on_day(self) -> int:
        """Get end period on the annotated day (as period number).

        If there is no date annotated, it will use the current date.
        """
        return self.raw_period_to_on_day.period

    def get_start_weekday(self, week: CalendarWeek) -> int:
        """Get start date of an event in a specific week."""
        if self.date_start < week[TimePeriod.weekday_min]:
            return TimePeriod.weekday_min
        else:
            return self.date_start.weekday()

    def get_end_weekday(self, week: CalendarWeek) -> int:
        """Get end date of an event in a specific week."""
        if self.date_end > week[TimePeriod.weekday_max]:
            return TimePeriod.weekday_max
        else:
            return self.date_end.weekday()

    def annotate_day(self, day: date):
        """Annotate event with the provided date."""
        self._date = day

    def get_groups(self) -> models.query.QuerySet:
        """Get groups relation."""
        return self.groups

    def get_teachers(self) -> models.query.QuerySet:
        """Get teachers relation."""
        return self.teachers

    @property
    def time_range(self) -> (timezone.datetime, timezone.datetime):
        """Get the time range of this event."""
        return timezone.datetime.combine(
            self.date_start, self.period_from.time_start
        ), timezone.datetime.combine(self.date_end, self.period_to.time_end)

    class Meta:
        ordering = ["date_start"]
        indexes = [
            models.Index(
                fields=["date_start", "date_end"],
                include=["period_from", "period_to"],
                name="event_date_start_date_end",
            )
        ]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


class ExtraLesson(
    GroupPropertiesMixin, TeacherPropertiesMixin, WeekRelatedMixin, SchoolTermRelatedExtensibleModel
):
    label_ = "extra_lesson"

    tracker = FieldTracker()

    objects = ExtraLessonManager.from_queryset(ExtraLessonQuerySet)()

    week = models.IntegerField(verbose_name=_("Week"), default=CalendarWeek.current_week)
    year = models.IntegerField(verbose_name=_("Year"), default=get_current_year)
    period = models.ForeignKey(
        "TimePeriod",
        models.CASCADE,
        related_name="extra_lessons",
        verbose_name=_("Time period"),
    )

    subject = models.ForeignKey(
        "Subject",
        on_delete=models.CASCADE,
        related_name="extra_lessons",
        verbose_name=_("Subject"),
    )
    groups = models.ManyToManyField(
        "core.Group", related_name="extra_lessons", verbose_name=_("Groups")
    )
    teachers = models.ManyToManyField(
        "core.Person",
        related_name="extra_lessons_as_teacher",
        verbose_name=_("Teachers"),
    )
    room = models.ForeignKey(
        "core.Room",
        models.CASCADE,
        null=True,
        related_name="extra_lessons",
        verbose_name=_("Room"),
    )

    comment = models.CharField(verbose_name=_("Comment"), blank=True, max_length=255)

    exam = models.ForeignKey(
        "Exam",
        on_delete=models.CASCADE,
        verbose_name=_("Related exam"),
        related_name="extra_lessons",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.week}, {self.period}, {self.subject}"

    def get_groups(self) -> models.query.QuerySet:
        """Get groups relation."""
        return self.groups

    def get_teachers(self) -> models.query.QuerySet:
        """Get teachers relation."""
        return self.teachers

    def get_subject(self) -> Subject:
        """Get subject."""
        return self.subject

    @property
    def time_range(self) -> (timezone.datetime, timezone.datetime):
        """Get the time range of this extra lesson."""
        return timezone.datetime.combine(
            self.date, self.period.time_start
        ), timezone.datetime.combine(self.date, self.period.time_end)

    class Meta:
        verbose_name = _("Extra lesson")
        verbose_name_plural = _("Extra lessons")
        indexes = [models.Index(fields=["week", "year"], name="extra_lesson_week_year")]


class AutomaticPlan(LiveDocument):
    """Model for configuring automatically updated PDF substitution plans."""

    template = "chronos/substitutions_print.html"

    number_of_days = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Number of days shown in the plan"),
    )
    show_header_box = models.BooleanField(
        default=True,
        verbose_name=_("Show header box"),
        help_text=_("The header box shows affected teachers/groups."),
    )
    last_substitutions_revision = models.ForeignKey(
        to=Revision,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Revision which triggered the last update"),
        editable=False,
    )

    @property
    def current_start_day(self) -> date:
        """Get first day which should be shown in the PDF."""
        return TimePeriod.get_next_relevant_day(timezone.now().date(), datetime.now().time())

    @property
    def current_end_day(self) -> date:
        """Get last day which should be shown in the PDF."""
        return self.current_start_day + timedelta(days=self.number_of_days - 1)

    def get_context_data(self) -> dict[str, Any]:
        """Get context data for generating the substitutions PDF."""
        from aleksis.apps.chronos.util.chronos_helpers import get_substitutions_context_data  # noqa

        context = get_substitutions_context_data(
            request=None,
            is_print=True,
            number_of_days=self.number_of_days,
            show_header_box=self.show_header_box,
        )

        return context

    def check_update(self, revision: Revision):
        """Check if the PDF file has to be updated and do the update then."""
        if not self.last_substitutions_revision or (
            self.last_substitutions_revision != revision
            and revision.date_created > self.last_substitutions_revision.date_created
        ):
            content_types = ContentType.objects.get_for_models(*_get_substitution_models()).values()
            versions = Version.objects.filter(content_type__in=content_types)
            if self.last_substitutions_revision:
                versions = versions.filter(
                    revision__date_created__gt=self.last_substitutions_revision.date_created
                )
            update = False
            for version in versions:
                if not version.object:
                    # Object exists no longer, so we can skip this
                    continue

                # Check if the changed object is relevant for the time period of the PDF file
                if isinstance(version.object, Event):
                    date_start = version.object.date_start
                    date_end = version.object.date_end
                else:
                    date_start = date_end = version.object.date
                if date_start <= self.current_end_day and date_end >= self.current_start_day:
                    update = True
                    break

            if update:
                self.update(triggered_manually=False)
                self.last_substitutions_revision = revision
                self.save()

    class Meta:
        verbose_name = _("Automatic plan")
        verbose_name_plural = _("Automatic plans")


@receiver(substitutions_changed)
def automatic_plan_signal_receiver(sender: Revision, versions: Iterable[Version], **kwargs):
    """Check all automatic plans for updates after substitutions changed."""
    for automatic_plan in AutomaticPlan.objects.all():
        automatic_plan.check_update(sender)


class ChronosGlobalPermissions(GlobalPermissionModel):
    class Meta:
        managed = False
        permissions = (
            ("view_all_room_timetables", _("Can view all room timetables")),
            ("view_all_group_timetables", _("Can view all group timetables")),
            ("view_all_person_timetables", _("Can view all person timetables")),
            ("view_timetable_overview", _("Can view timetable overview")),
            ("view_lessons_day", _("Can view all lessons per day")),
            ("view_supervisions_day", _("Can view all supervisions per day")),
        )
