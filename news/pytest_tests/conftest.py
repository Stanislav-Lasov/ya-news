from datetime import datetime, timedelta

from django.test.client import Client
from django.urls import reverse
import pytest

from news.forms import BAD_WORDS
from news.models import News, Comment


FORM_DATA = {'text': 'Новый текст комментария'}
FORM_BAD_DATA = {'text': BAD_WORDS[0]}


@pytest.fixture(autouse=True)
def enable_db(db):
    pass


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def auth_user(django_user_model):
    return django_user_model.objects.create(username='Пользователь')


@pytest.fixture
def auth_user_client(auth_user):
    client = Client()
    client.force_login(auth_user)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст'
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        text='Текст комментария',
        news=news,
        author=author
    )


@pytest.fixture
def url_paths(news, comment):
    return {
        'home': reverse('news:home'),
        'detail': reverse('news:detail', args=(news.id,)),
        'delete': reverse('news:delete', args=(comment.id,)),
        'edit': reverse('news:edit', args=(comment.id,)),
        'logout': reverse('users:logout'),
        'login': reverse('users:login'),
        'signup': reverse('users:signup'),
    }


@pytest.fixture
def many_news():
    all_news = [
        News(
            title=f'Новость {index}',
            text=f'Текст {index}',
            date=datetime.today() - timedelta(days=index)
        ) for index in range(11)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def many_comments(news, author):
    all_comments = [
        Comment(
            text=f'Текст комментария {index}',
            news=news,
            author=author,
            created=datetime.today() - timedelta(days=index)
        ) for index in range(5)
    ]
    Comment.objects.bulk_create(all_comments)
