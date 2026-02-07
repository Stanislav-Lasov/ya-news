from http import HTTPStatus

from pytest_django.asserts import assertFormError

from news.forms import WARNING
from news.models import Comment
from news.pytest_tests.conftest import FORM_DATA, FORM_BAD_DATA


def test_user_create_comment(client, auth_user_client, url_paths):
    """Тестирование возможности написать комментарий."""
    url = url_paths['detail']
    before_comment_count = Comment.objects.count()
    client.post(url, data=FORM_DATA)
    assert Comment.objects.count() == before_comment_count
    before_comment_count = Comment.objects.count()
    auth_user_client.post(url, data=FORM_DATA)
    assert Comment.objects.count() > before_comment_count


def test_bad_words_in_comment(auth_user_client, url_paths):
    """Тест на недопустимые слова в фоме комментария."""
    before_comment_count = Comment.objects.count()
    response = auth_user_client.post(url_paths['detail'], data=FORM_BAD_DATA)
    assert 'form' in response.context
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == before_comment_count


def test_edit_and_delete_comments_for_author(
        author_client, comment, url_paths
):
    """Проверка редактирования и удаления комментария его автором."""
    # Проверка редактирования.
    comment_pk = comment.pk
    before_comment_count = Comment.objects.count()
    author_client.post(url_paths['edit'], data=FORM_DATA)
    edited_comment = Comment.objects.get(pk=comment_pk)
    assert Comment.objects.count() == before_comment_count
    assert edited_comment.text == FORM_DATA['text']
    # Проверка удаления.
    before_comment_count = Comment.objects.count()
    response = author_client.delete(url_paths['delete'])
    assert Comment.objects.count() == before_comment_count - 1
    assert response.status_code == HTTPStatus.FOUND


def test_edit_and_delete_comments_for_other_user(
        auth_user_client, comment, url_paths
):
    """Проверка редактирования и удаления комментария другим пользователем."""
    # Проверка редактирования.
    comment_pk = comment.pk
    original_comment_data = {
        'text': comment.text,
        'author': comment.author,
        'news': comment.news,
        'created': comment.created,
    }
    before_comment_count = Comment.objects.count()
    auth_user_client.post(url_paths['edit'], data=FORM_DATA)
    edited_comment = Comment.objects.get(pk=comment_pk)
    assert Comment.objects.count() == before_comment_count
    assert edited_comment.text != FORM_DATA['text']
    # Проверка удаления.
    before_comment_count = Comment.objects.count()
    response = auth_user_client.delete(url_paths['delete'])
    assert Comment.objects.count() == before_comment_count
    assert response.status_code == HTTPStatus.NOT_FOUND
    unchanged_comment = Comment.objects.get(pk=comment_pk)
    assert unchanged_comment.text == original_comment_data['text']
    assert unchanged_comment.author == original_comment_data['author']
    assert unchanged_comment.news == original_comment_data['news']
    assert unchanged_comment.created == original_comment_data['created']
