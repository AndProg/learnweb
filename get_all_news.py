# файл можно удалить, поскольку его функционал реализован в tasks.py


from webapp import create_app
from webapp.news.parsers import habr 
# << импортировать можно целый .py файл, чтобы не прописывать в дальнейшем каждый def в отдельности

app = create_app()
with app.app_context():
    #habr.get_news_snippets()
    habr.get_news_content()

