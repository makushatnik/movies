from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from model_utils.models import TimeStampedModel


class Genre(TimeStampedModel):
    name = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')

    def __str__(self):
        return self.name


class FilmworkType(models.TextChoices):
    # MOVIE = 'movie', _('фильм')
    # TV_SHOW = 'tv_show', _('шоу')
    name = models.CharField(_('название'), max_length=255)

    class Meta:
        verbose_name = _('тип кинопроизведения')
        verbose_name_plural = _('типы кинопроизведений')

    def __str__(self):
        return self.name


class Filmwork(TimeStampedModel):
    title = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)
    creation_date = models.DateField(_('дата создания фильма'),
                                     blank=True)
    certificate = models.TextField(_('сертификат'), blank=True)
    file_path = models.FileField(_('файл'),
                                 upload_to='film_works/', blank=True)
    rating = models.FloatField(_('рейтинг'),
                               validators=[MinValueValidator(0)], blank=True)
    # type = models.CharField(_('тип'), max_length=20,
    #                         choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre)
    type = models.ForeignKey(
        FilmworkType,
        verbose_name=_("тип кинопроизведения"),
        related_name='films',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    birth_date = models.DateTimeField()


class Gender(models.TextChoices):
    MALE = 'male', _('мужской')
    FEMALE = 'female', _('женский')


class PersonRole:
    pass


class Person(models.Model):
    first_name = models.CharField(_('название'), max_length=255)
    last_name = models.CharField(_('название'), max_length=255)
    gender = models.TextField(_('пол'), choices=Gender.choices, null=True)


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('актёр')
    WRITER = 'writer', _('сценарист')
    DIRECTOR = 'director', _('режиссёр')


class PersonFilmWork(models.Model):
    person = models.ForeignKey(
        Person, verbose_name=_("human"), related_name='person_filmworks',
        on_delete=models.CASCADE, null=False
    )
    filmwork = models.ForeignKey(
        Filmwork, verbose_name=_("кинопроизведение"),
        related_name='person_filmworks', on_delete=models.CASCADE, null=False
    )
    profession = models.TextField(_('профессия'), choices=RoleType.choices, null=True)
    role = models.TextField(_('роль'), null=True)


class GenreFilmWork(models.Model):
    genre = models.ForeignKey(
        Genre, verbose_name=_("жанр"), related_name='genre_filmworks',
        on_delete=models.CASCADE, null=False
    )
    filmwork = models.ForeignKey(
        Filmwork, verbose_name=_("кинопроизведение"),
        related_name='genre_filmworks', on_delete=models.CASCADE, null=False
    )
