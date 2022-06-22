# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie(scrapy.Item):
    genres = scrapy.Field()
    date_of_scraping = scrapy.Field()
    directors = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    release_year = scrapy.Field()
    top_cast = scrapy.Field()
    url = scrapy.Field()
    uid = scrapy.Field()
    poster_url = scrapy.Field()
    images = scrapy.Field()
    top_cast_urls = scrapy.Field()


class Actor(scrapy.Item):
    name = scrapy.Field()
    uid = scrapy.Field()
    url = scrapy.Field()
    filmography_movie_url = scrapy.Field()
    filmography_movie_title = scrapy.Field()


class ActorsAndMovies(scrapy.Item):
    actor_uid = scrapy.Field()
    movie_uid = scrapy.Field()
