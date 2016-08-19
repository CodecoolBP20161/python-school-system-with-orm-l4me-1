from peewee import *
import sys

db = PostgresqlDatabase('school_system')


def connect_to_db():
    try:
        db.connect()
    except:
        print("'school_system' database needed. Please create database first")
        sys.exit()


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db
