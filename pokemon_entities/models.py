from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to="pokemon", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    evolved_from = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    latitude = models.FloatField(null=True, blank=True, verbose_name='широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='долгота')

    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='покемон',
        on_delete=models.CASCADE)
    

    
    def __str__(self):
        return f'{self.pokemon} {self.id}'
    
    appeared_at = models.DateTimeField(default=timezone.now, verbose_name='время появления')
    disappeared_at = models.DateTimeField(verbose_name='время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='здоровье')
    offense = models.IntegerField(null=True, blank=True, verbose_name='атака')
    defense = models.IntegerField(null=True, blank=True, verbose_name='защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='выносливость')

