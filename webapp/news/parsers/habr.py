from datetime import datetime, timedelta
import locale
import platform

from bs4 import BeautifulSoup

from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')


# поле Дата в БД должно быть в формате datetime. 
# в таком случае фильтрации и процие операции с датами будут работать корректно
def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()    


# комменты по функции есть в файле python_org_news.py
def get_news_snippets():
    html = get_html('https://habr.com/ru/search/?target_type=posts&q=python&order')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_='content-list_posts').findAll('li', class_='content-list__item_post')

        for news in all_news:
            title = news.find('a', class_='post__title_link').text
            url = news.find('a', class_='post__title_link')['href']
            published = news.find('span', class_='post__time').text
            published = parse_habr_date(published)
            save_news(title, url, published)


def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # .decode_contents() позволяет получить на вызоде htmL, что находится внутри, 
            news_text = soup.find('div', class_='post__text').decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()