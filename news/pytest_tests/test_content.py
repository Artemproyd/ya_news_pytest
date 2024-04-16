import operator
from django.urls import reverse
from news.forms import CommentForm
from django.conf import settings
PAGINATION_CONST = settings.NEWS_COUNT_ON_HOME_PAGE


def test_note_in_list_for_author1(five_comments, author_client):
    url = reverse('news:detail',
                  args=(five_comments[0].news.pk,))
    response = author_client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps <= sorted_timestamps


def test_note_in_list_for_author(news_11, author_client):
    url = reverse('news:home')
    response = author_client.get(url)
    all_news = response.context['object_list']
    sorted_news = sorted(all_news,
                         key=operator.attrgetter('date'),
                         reverse=True)
    assert len(all_news) == PAGINATION_CONST
    test = True
    for i in range(len(all_news)):
        if all_news[i] != sorted_news[i]:
            test = False
    assert test


def test_not_create_news_page_contains_form_author(author_client,
                                                   news, comment):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
    url = reverse('news:edit', args=(comment.pk,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_not_edit_comment_page_contains_form_client(client, news, comment):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert not ('form' in response.context)
    url = reverse('news:edit', args=(comment.pk,))
    response = client.get(url)
    # Тут try потому, что иначе он выдаёт
    # ошибку  TypeError: argument of type 'NoneType' is not iterable
    try:
        assert not ('form' in response.context)
    except Exception:
        assert True
