import datetime
import pytest

from django.test.client import Client
from django.conf import settings
from django.urls import reverse
from news.models import News, Comment
from datetime import timedelta

PAGINATION_CONST = settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture(autouse=True)
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def not_auth_client(not_author):
    client = Client()
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
        date=datetime.date.today(),
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст заметки',
    )
    return comment


@pytest.fixture
def five_comments(author, news):
    comments = []
    for i in range(5):
        comments.append(Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст заметки{i}',
        ))
    return comments


@pytest.fixture
def news_11(author, news):
    news = []
    today = datetime.date.today()
    for i in range(PAGINATION_CONST + 1):
        news = News.objects.create(
            title=f'Заголовок{i}',
            text=f'Текст заметки{i}',
            date=today - timedelta(days=int(i)),
        )
    return news


@pytest.fixture
def form_data(author, news):
    form_data = {
        'news': news,
        'author': author,
        'text': 'Текст заметки',
    }
    return form_data


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def edit_redirect(login_url, edit_url):
    return f'{login_url}?next={edit_url}'


@pytest.fixture
def delete_redirect(login_url, delete_url):
    return f'{login_url}?next={delete_url}'
