import scrapy
import re
import ipdb
from imdb.items import Movie, Actor, ActorsAndMovies
from datetime import date
import json


class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["www.imdb.com", "www.amazon.com"]

    def start_requests(self):
        yield scrapy.Request(url="https://www.imdb.com/user/ur24609396/watchlist", callback=self.parse_watchlist)

    def parse_watchlist(self, response):
        movie_link_pattern = re.compile(r"[^t]const.{3}tt\d{7}")
        movie_urls = re.findall(movie_link_pattern, response.text)
        movie_urls = [x.replace('"const":"', "https://www.imdb.com/title/") for x in movie_urls]

        for movie_url in movie_urls[:1]:
            yield scrapy.Request(url=movie_url, callback=self.parse_movie_page)
            # print(movie_url)

    def parse_movie_page(self, response):
        # ipdb.set_trace()
        movie = Movie()
        actors_and_movies = ActorsAndMovies()
        movie["title"] = response.xpath("//*[contains(@data-testid, 'hero-title-block__title')]/text()").get()
        movie["release_year"] = response.xpath("//*[contains(@href, 'releaseinfo')]/text()").get()
        movie["directors"] = response.xpath("//*[contains(@href, 'tt_cl_dr')]/text()").getall()
        movie["rating"] = response.xpath("//div/span[contains(@class, '')]/text()").get()
        # movie["genres"] = response.xpath("//*[contains(@href, 'tt_ov_in')]/text()").getall()
        movie["genres"] = response.xpath(
            "//div[@class='sc-16ede01-8 hXeKyz sc-910a7330-11 GYbFb']//li[@class='ipc-inline-list__item ipc-chip__text']/text()"
        ).getall()
        movie["date_of_scraping"] = str(date.today())
        movie["top_cast"] = response.xpath("//*[contains(@data-testid, 'title-cast-item')]/text()").getall()
        movie["url"] = response.url
        uid = response.url
        movie["uid"] = uid[27 : len(uid) - 1]
        # movie["poster_url"] = response.xpath("//*[contains(@class, 'poster')]/text()").get()
        movie["poster_url"] = response.xpath(
            "//div[@class='ipc-media ipc-media--poster-27x40 ipc-image-media-ratio--poster-27x40 ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img']/img[@class='ipc-image']/@src"
        ).getall()
        # images = scrapy.Field()

        actor_link_pattern = re.compile(r"[^t]characters.nm\d{7}")
        actor_urls = re.findall(actor_link_pattern, response.text)
        actor_urls = [x.replace("characters/", "name/") for x in actor_urls]
        # http_urls = [response.urljoin(url) for url in actor_urls]
        # actor_urls = [x.replace("name/", "https://www.imdb.com/name/") for x in actor_urls]
        # ipdb.set_trace()

        yield movie

        for actor_url in actor_urls:
            # ipdb.set_trace()
            actors_and_movies["movie_uid"] = movie["uid"]
            actors_and_movies["actor_uid"] = actor_url
            yield scrapy.Request(response.urljoin(actor_url), callback=self.parse_actor_page)
            yield actors_and_movies
            # print(actor_url)

    def parse_actor_page(self, response):
        # ipdb.set_trace()
        actor = Actor()
        actor["name"] = response.xpath("//h1/span[contains(@class, 'itemprop')]/text()").get()
        actor["url"] = response.url
        uid = response.url
        actor["uid"] = uid[26 : len(uid) - 1]
        # actor["filmography_movie_url"] = response.xpath("//div/span/b[contains(@href, 'nm_flmg')]/text()").getall()
        actor["filmography_movie_title"] = response.xpath("//div/b/a[contains(@href, 'nm_flmg_act')]/text()").getall()
        actor["filmography_movie_url"] = response.xpath("//div/b/a[contains(@href, 'nm_flmg_act')]/@href").getall()
        actor["filmography_movie_url"] = [
            x.replace("/title/", "https://www.imdb.com/title/") for x in actor["filmography_movie_url"]
        ]

        yield actor

    actor_uid = scrapy.Field()
    movie_uid = scrapy.Field()

    # f = open("urls_of_movies.html", "w")
    # f.write(str(movie_urls))
    # f.close()
