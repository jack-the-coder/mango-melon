import datetime
import os
from urllib.parse import urlparse, uses_netloc
import smtplib
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from email.mime.text import MIMEText

DB = Proxy()


class User(UserMixin, Model):
    username = CharField(max_length=10, unique=True)
    email = TextField(unique=True)
    first_name = TextField()
    last_name = TextField()
    password = TextField()
    avatar = TextField(default='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw0PDRANDQ0PDQ0NDQ0PDQ0NDw8O'
                               'Dg0NFRIWFhURExYYHTQgGBolGxUVLTEhJS03LjouFyAzODUsNygtLisBCgoKBQUFDgUFDisZExkrKysrKysrKys'
                               'rKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAKAAoAMBIgACEQEDEQH/xAAbAA'
                               'EAAgMBAQAAAAAAAAAAAAAAAgMBBQYHBP/EADIQAAMAAQEGAwYFBQEAAAAAAAABAgMRBAUGITFBElFSImFxgZGxE'
                               'zJicqEjNELB0TP/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMR'
                               'AD8A9ZAAAAAADIGDI0MpAYB821bxwYuV5JT9K9qvojXZOJsK/LjyX73pIG6Boo4nxa88NpeaqaNlse9MGblF+16'
                               'K9mvl5gfWYJaGNAMAyYAAAAAAAAAGQABnQykSSA+TeG2xgjx3z7TK62/JHJbdvjPm1TpxHohtL5vuS4g2t5dopf'
                               '44tYlfDq/r9jWgAAAAAG72PiPLEqckLLpy8TpzTXv5czo9h2uM2NZI6Pk0+s0uqZwJv+EM7WTJib5XCpL9Uv8A4'
                               '/4A6bQwTaItARBkwAAAAAyAJJGETSAJE1y5+XMJFinXl58gPMXWrbfVtt/FmDLWnLum0/kYAAAAAABt+Fv7uf2X'
                               '9jUG94PjXam/Tit/ykB1rRBovaK2gKmjBNoi0BEGTAAkjBlASSJyiKRZKAlKLJRiUSttTTXVTTXxSA833viUbTm'
                               'ldFlvT5vX/Z8hmrdN1T1qm6p+bfNmAAAAAAAdDwU1+PkXd4eXv0panPH07t2l4s+PIn+W5198t6NfQD0ikV0i+k'
                               'V0gKKRBotpFbAgzBJkQMokjCJSBOSyUQktkCcomlry8+RiSaA8puHLcvrLcv4p6EToOJdy5pz3lx46vFkbtuFr4'
                               'K7po58AAAAAAF2x4/Hmxwv8skL60ik6bhTcuX8Wdoyw4xwtcark7p9Hp5AdhRXSLWV0BTSK6LaRXQFbIkmRAyic'
                               'kETkCyS2SuSyQLJLEQkmgDWq08zydzo2vJtfQ9ZPM99bJeHackUtNbq4faobbTQHwgAAAAPr3TiV7Thilqqyxqv'
                               'Na66Hp7OD4Q3fWTaFm00x4dW3521ylfU7wCLK6LGQoCmiui2iqgK2QZNkWAROSCJyBbJbJTJbIFsk0QkmgMnC8V'
                               'b3jPX4U4//AByUlm8Wrrs0lp01+x0XEm9ls+FzL/rZE1CXWV3p/A89AAAAAAOo4c4gjHOLZaxeFOtPxVfLxU+rW'
                               'n+zsjyVnoXDe9ltGFTVf1saStPrS7WviBtmQomyugK6KqLaKqAroiyTIMDKJIgj59q3lgxcsmRJ+le1X0QH3yTv'
                               'LMT4rpTK61TSRym2cUV0wY/D+vJzfynsaLadpyZa8WW6t9vE+S+C7Addt3FeGOWGXmr1flhfPqzntt37teXrlcT'
                               '6cXsL+OZrAA9/d9X5gAAAAAAAD3910fkABsti37tWHpldz6cvtr+eZ0Ow8VYb5ZpeGvUvah/PqjjAB6ZGWbnxRS'
                               'qX0qWmiNHnezbTkxPxYrqH38L5P4rubzY+KK6Z8fi/Xj5P5yB0jIs+bZd5YMvLHkTfpfs19GfSwOX33vi6usWKn'
                               'MS3NVL52+/PsjRksn5q/dX3IgAAAAAAAAAAAAAAAAAAAAAA3m5N8XNTiy14opqZqnzh9ufdGjJY/wA0/un7gYfU'
                               'wAAAAAAAAAAAAAAAAAAAAAAADK6mAB//2Q==')
    joined_at = DateTimeField(default=datetime.datetime.now)
    bio = TextField(default='This person has not set a bio, yet. )
    default_view = CharField(default='popular')

    def __str__(self):
        return self.username

    @classmethod
    def create_user(cls, username, email, first_name, last_name, password):
        user = cls.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=generate_password_hash(password)
        )



    class Meta:
        database = DB
        order_by = ('-joined_at',)


class Post(Model):
    user = ForeignKeyField(User, related_name='posts')
    data = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return str(self.id)

    class Meta:
        database = DB
        order_by = ('-created_at',)


class Comment(Model):
    user = ForeignKeyField(User, related_name='user_comments')
    post = ForeignKeyField(Post, related_name='comments')
    data = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        database = DB
        order_by = ('-created_at',)




if 'HEROKU' in os.environ:
    uses_netloc.append('postgres')
    url = urlparse(os.environ["DATABASE_URL"])
    db_sql = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,
                                port=url.port)
    DB.initialize(db_sql)
else:
    db_sql = SqliteDatabase('DB')
    DB.initialize(db_sql)






def del_post():
    post_id = int(input('Post id to delete: '))
    Post.get(Post.id == post_id).delete_instance()

DB.connect()
DB.create_tables([User, Post], safe=True)
