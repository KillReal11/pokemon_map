from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='Имя на русском')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Имя на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Имя на японском')
    photo = models.ImageField(upload_to="pokemon", null=True, blank=True, verbose_name='Фото покемона')
    description = models.TextField(blank=True, verbose_name='Описание')

    evolved_from = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='evolved_to',
        on_delete=models.SET_NULL,
        verbose_name='Из кого эволюционировал'
    )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name='широта')
    longitude = models.FloatField(verbose_name='долгота')

    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='покемон',
        related_name='entities',
        on_delete=models.CASCADE)

    appeared_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='время появления',
    )

    disappeared_at = models.DateTimeField(verbose_name='время исчезновения')

    level = models.IntegerField(null=True, blank=True, verbose_name='уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='здоровье')
    offense = models.IntegerField(null=True, blank=True, verbose_name='атака')
    defense = models.IntegerField(null=True, blank=True, verbose_name='защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='выносливость')

    def __str__(self):
        return f'{self.pokemon} {self.id}'
