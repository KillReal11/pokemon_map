import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(
            pokemon=pokemon,
            appeared_at__lt=timezone.now(),
            disappeared_at__gt=timezone.now()
        )
        pokemon_img_url = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_img_url,
            'title_ru': pokemon.title_ru,
        })

        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                pokemon_img_url
            )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    current_pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon_img_url = request.build_absolute_uri(current_pokemon.photo.url) if current_pokemon.photo else None
    pokemons_on_page = {
        'pokemon_id': current_pokemon.id,
        'img_url': pokemon_img_url,
        'title_ru': current_pokemon.title_ru,
        'description': current_pokemon.description,
        'title_en': current_pokemon.title_en,
        'title_jp': current_pokemon.title_jp,
    }
    previous_evolution_pokemon = current_pokemon.evolved_from
    if previous_evolution_pokemon:
        previous_evolution_pokemon_img_url = (
            request.build_absolute_uri(previous_evolution_pokemon.photo.url)
            if previous_evolution_pokemon.photo
            else None
        )

        previous_evolution = {
                "title_ru": previous_evolution_pokemon,
                "pokemon_id": previous_evolution_pokemon.id,
                "img_url": previous_evolution_pokemon_img_url
        }
        pokemons_on_page['previous_evolution'] = previous_evolution

    next_evolution_pokemon = current_pokemon.evolved_to.first()
    if next_evolution_pokemon:
        next_evolution_pokemon_img_url = (
            request.build_absolute_uri(next_evolution_pokemon.photo.url)
            if next_evolution_pokemon.photo
            else None
        )

        next_evolution = {
                "title_ru": next_evolution_pokemon,
                "pokemon_id": next_evolution_pokemon.id,
                "img_url": next_evolution_pokemon_img_url
        }
        pokemons_on_page['next_evolution'] = next_evolution






    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_img_url = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None
        if current_pokemon.title_ru == pokemon.title_ru:
            pokemon_entities = PokemonEntity.objects.filter(
                pokemon=pokemon,
                appeared_at__lt=timezone.now(),
                disappeared_at__gt=timezone.now()
            )
            for pokemon_entity in pokemon_entities:
                add_pokemon(
                    folium_map, pokemon_entity.latitude,
                    pokemon_entity.longitude,
                    pokemon_img_url
                )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
