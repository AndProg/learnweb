from datetime import datetime

from sqlalchemy.orm import relationship

from webapp.db import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)


# параметр "ondelete='CASCADE'" означает, что при удалении новости
# связанные с ней комментарии также будут удалены
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    # виртуальные поля / первый аргумент: ссылка на модели User и News
    # второй аргумент отвечает за создаваемые виртуальные поля в 
    # моделях User и News
    news = relationship('News', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return "<Comment {}>".format(self.id)

"""

// __repr__ - "магический" метод python, который
вызывается сам в определенных случаях

>> например, при вызове функции print(obj)

// (self) означает, что идет обращение к конкретному
экземпляру класса (конкретной новости), который сейчас активен

"""
