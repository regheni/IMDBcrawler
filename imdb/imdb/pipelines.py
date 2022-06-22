from itemadapter import ItemAdapter
import json
import sqlite3
from imdb.items import Movie, Actor, ActorsAndMovies
import ipdb


class ImdbPipeline:
    def process_item(self, item, spider):
        return item


class SimpleStoragePipeline:
    def open_spider(self, spider):
        self.movie = open("imdb_movie.json", "w")
        self.actor = open("imdb_actor.json", "w")
        self.actor_movie = open("imdb_actor_movie.json", "w")
        # open 1 file for each type
        # connect to db

    def process_item(self, item, spider):
        # if type of item = Movie insert into movie
        if isinstance(item, Movie):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.movie.write(line)
            return item
        elif isinstance(item, Actor):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.actor.write(line)
            return item
        elif isinstance(item, ActorsAndMovies):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.actor_movie.write(line)
            return item

    def close_spider(self, spider):
        self.movie.close()
        self.actor.close()
        self.actor_movie.close()
