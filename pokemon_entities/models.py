from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="pokemon", null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    latitude = models.FloatField(null=True, blank=True, verbose_name='широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='долгота')

    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='покемон',
        on_delete=models.CASCADE)
    
    appeared_at = models.DateTimeField(default=timezone.now, verbose_name='время появления')
    disappeared_at = models.DateTimeField(verbose_name='время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='здоровье')
    offense = models.IntegerField(null=True, blank=True, verbose_name='атака')
    defense =  models.IntegerField(null=True, blank=True, verbose_name='защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='выносливость')

