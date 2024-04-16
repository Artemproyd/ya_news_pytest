from django.urls import reverse
from pytest_django.asserts import assertFormError
from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_user_can_create_comment(author_client, author, news, form_data):
    count_comment = Comment.objects.count()
    url = reverse('news:detail', args=(news.pk,))
    author_client.post(url, data=form_data)
    assert Comment.objects.count() == count_comment + 1
    new_comment = Comment.objects.last()
    assert new_comment.news == form_data['news']
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_anonymous_user_cant_create_comment(client, news, form_data):
    count_comment = Comment.objects.count()
    url = reverse('news:detail', args=(news.pk,))
    client.post(url, data=form_data)
    assert Comment.objects.count() == count_comment


def test_author_can_edit_comment(author_client, form_data, comment, news):
    old_comment = comment
    url = reverse('news:edit', args=(comment.pk,))
    new_form_data = form_data
    new_form_data['text'] = BAD_WORDS[0]
    response = author_client.post(url, form_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    new_form_data['text'] = '111'
    author_client.post(url, new_form_data)
    new_comment = Comment.objects.get()
    assert new_comment.text != old_comment.text
    assert new_comment.news == old_comment.news
    assert new_comment.author == old_comment.author
    assert new_comment.created == old_comment.created


def test_other_user_cant_edit_comment(not_author_client,
                                      form_data, comment, news):
    old_comment = comment
    url = reverse('news:edit', args=(comment.pk,))
    new_form_data = form_data
    new_form_data['text'] = '111'
    not_author_client.post(url, form_data)
    new_comment = Comment.objects.get()
    assert new_comment == old_comment


def test_other_user_cant_delete_comment(not_author_client,
                                        form_data, comment, news):
    count_comment = Comment.objects.count()
    url = reverse('news:delete', args=(comment.pk,))
    not_author_client.post(url)
    assert Comment.objects.count() == count_comment


def test_author_can_delete_comment(author_client, form_data, comment, news):
    count_comment = Comment.objects.count()
    url = reverse('news:delete', args=(comment.pk,))
    author_client.post(url)
    assert Comment.objects.count() == count_comment - 1
